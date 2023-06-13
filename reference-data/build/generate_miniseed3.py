#!/usr/bin/env python3
#
# Generate a miniSEED V3 record with specified header values and
# pre-prepared data payloads.

import sys
import struct
import argparse
import crcmod.predefined
import base64
import json


def main():

    parser = argparse.ArgumentParser(description='Generate a miniSEED V3 record.')

    parser.add_argument('-Y', '--year', dest='year', default=2022, type=int,
                        help='Set the start year')
    parser.add_argument('-D', '--day', dest='day', default=156, type=int,
                        help='Set the start day-of-year')
    parser.add_argument('-H', '--hour', dest='hour', default=20, type=int,
                        help='Set the start hour')
    parser.add_argument('-M', '--minute', dest='minute', default=32, type=int,
                        help='Set the start minute')
    parser.add_argument('-S', '--second', dest='second', default=38, type=int,
                        help='Set the start second')
    parser.add_argument('-N', '--nanosecond', dest='nanosecond', default=123456789, type=int,
                        help='Set the start nanosecond')
    parser.add_argument('-V', '--pubversion', dest='pub_version', default=1, type=int,
                        help='Set the publication version')
    parser.add_argument('-f', '--flags', dest='flags', default='00000000',
                        help='Set bit flags (8-bit mask, default "00000000")')
    parser.add_argument('-s', '--samplerateperiod', dest='sample_rate_period', default=0.0, type=float,
                        help='Set the sample rate/period')
    parser.add_argument('-i', '--identifier', dest='identifier', default='FDSN:XX_TEST__B_S_P',
                        help='Set the source identifier (default FDSN:XX_TEST__B_S_P)')
    parser.add_argument('-e', '--extraheader', dest='extraheader', default=None,
                        help='Select JSON extra header file to inject (default is none)')
    parser.add_argument('-p', '--payload', dest='payload', default='nopayload',
                        help='Select desired payload (text, int16, int32, float32, float64, steim1, steim2)')

    args = parser.parse_args()


    length_identifier = len(args.identifier)
    format_version = 3

    # Convert binary bit mask string "00000000" to an integer flags value
    flags = int(args.flags, 2)

    # Load extra header file and create compact version
    extra_header = b''
    if args.extraheader is not None:
        with open(args.extraheader) as fp:
            extra_header = json.load(fp)
            extra_header = json.dumps(extra_header, separators=(',', ':'))
            extra_header = extra_header.encode('utf-8')

    length_extra_header = len(extra_header)

    # Configure payload details
    (payload, encoding, number_samples) = set_payload (args.payload)

    if payload is None:
        print(f"Payload value '{args.payload}' is not recognized", file=sys.stderr)
        exit(1)

    # Set sample rate to something other than zero for non-text payloads
    if args.payload != 'text' and args.sample_rate_period == 0.0:
        args.sample_rate_period = 1.0

    length_payload = len(payload)


    # miniSEED 3 Fixed Section of Data Header
    # 40 bytes, plus length of identifier, plus length of extra headers
    #
    # #  FIELD                   TYPE       OFFSET
    # 1  record indicator        char[2]       0
    # 2  format version          uint8_t       2
    # 3  flags                   uint8_t       3
    # 4a nanosecond              uint32_t      4
    # 4b year                    uint16_t      8
    # 4c day                     uint16_t     10
    # 4d hour                    uint8_t      12
    # 4e min                     uint8_t      13
    # 4f sec                     uint8_t      14
    # 5  data encoding           uint8_t      15
    # 6  sample rate/period      float64      16
    # 7  number of samples       uint32_t     24
    # 8  CRC of record           uint32_t     28
    # 9  publication version     uint8_t      32
    # 10 length of identifer     uint8_t      33
    # 11 length of extra headers uint16_t     34
    # 12 length of data payload  uint32_t     36
    # 13 source identifier       char         40
    # 14 extra headers           char         40 + field 10
    # 15 data payload            encoded      40 + field 10 + field 11

    # Python struct codes:
    # < = little endian
    # s = char[]
    # B = unsigned char (8 bits)
    # H = unsigned short (16 bits)
    # L = unsigned long (32 bits)
    # d = double (64 bits)

    # Pack record header, little-endian binary values
    ms3record0 = (struct.pack('<2sBBLHHBBBBdLLBBHL',
                              b'MS',
                              format_version,
                              flags,
                              args.nanosecond,
                              args.year,
                              args.day,
                              args.hour,
                              args.minute,
                              args.second,
                              encoding,
                              args.sample_rate_period,
                              number_samples,
                              0, # Initial CRC is 0
                              args.pub_version,
                              length_identifier,
                              length_extra_header,
                              length_payload) +
                  args.identifier.encode("ascii") +
                  extra_header +
                  payload)

    # Calculate CRC32C of record
    crc32c_func = crcmod.predefined.mkCrcFun('crc-32c')
    crc_value = crc32c_func(ms3record0)

    # Reconstruct the record, replacing the calculated CRC
    ms3record = (ms3record0[:28] +
                 struct.pack ('<L', crc_value) +
                 ms3record0[32:])

    # Write binary record to stdout
    sys.stdout.buffer.write (ms3record)


# Return (payload, encoding, number_samples) for specified choice
def set_payload(choice):
    return {
        'nopayload': (b'', 0, 0),
        'text': (data_text, 0, len(data_text)),
        'int16': (base64.b64decode(data_int16le_220), 1, 220),
        'int32': (base64.b64decode(data_int32le_500), 3, 500),
        'float32': (base64.b64decode(data_float32le_500), 4, 500),
        'float64': (base64.b64decode(data_float64le_500), 5, 500),
        'steim1': (base64.b64decode(data_steim1_500), 10, 500),
        'steim2': (base64.b64decode(data_steim2_499), 11, 499),
    }.get(choice, (None, None, None)) # Default is all None


# Below are data payloads of different encodings
# Non-text data samples are that of an expanding sinusoid.

# text data
data_text = "I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, like tears...in...rain. Time to die.".encode('utf-8')

# 400 sample sinusoid, 16-bit integer, little-endian (Base64)
data_int16le_220 = b'AAAGAAoACgAGAAAA+f/0//T/+P8AAAgADgAPAAkAAAD2/+//7v/1/wAADQAVABUADQAAAPD/5v/m//D/AQATAB8AHwATAP//6f/b/9v/6f8CABwALQAtABsA/v/e/8r/yv/g/wMAKQBBAEEAJgD7/87/sf+y/9L/BgA9AF8AXgA3APj/tv+N/4//v/8LAFoAigCHAE4A8v+T/1n/Xv+k/xMAhADJAMIAbgDo/2D/Dv8X/33/HwDBACMBGAGcANn/Fv+h/rD+R/8yABwBpgGSAdwAwf+p/gT+Hf76/k8AoAFkAkMCNwGc/wn+H/1K/Y7+fQBhAncDQAO4AWP/H/3U+xv89v3EAHwDBQWrBGwCC//I+/X5aPog/TIBGgVGB7QGagOD/tT5P/f39/P72QF4B4kKoQnPBLT99/ZT83b0TPraAu0KQQ/TDcQGd/zJ8qXtcO/792EE+w8XFtgTgQmV+q3sbOU66Lz0sgZdF/ofexxYDbr3weOI2eLdMvA2CiYiSC7dKLcSZ/O41lPIDs/Z6YcP5jH6Qp46Nxrf7LDDb6/MufzgjRflSOhgEVSuJAbj6Kdwi1Wbo9Q='

# 500 sample sinusoid, 32-bit integer, little-endian (Base64)
data_int32le_500 = b'AAAAAAYAAAAKAAAACgAAAAYAAAAAAAAA+f////T////0////+P///wAAAAAIAAAADgAAAA8AAAAJAAAAAAAAAPb////v////7v////X///8AAAAADQAAABUAAAAVAAAADQAAAAAAAADw////5v///+b////w////AQAAABMAAAAfAAAAHwAAABMAAAD/////6f///9v////b////6f///wIAAAAcAAAALQAAAC0AAAAbAAAA/v///97////K////yv///+D///8DAAAAKQAAAEEAAABBAAAAJgAAAPv////O////sf///7L////S////BgAAAD0AAABfAAAAXgAAADcAAAD4////tv///43///+P////v////wsAAABaAAAAigAAAIcAAABOAAAA8v///5P///9Z////Xv///6T///8TAAAAhAAAAMkAAADCAAAAbgAAAOj///9g////Dv///xf///99////HwAAAMEAAAAjAQAAGAEAAJwAAADZ////Fv///6H+//+w/v//R////zIAAAAcAQAApgEAAJIBAADcAAAAwf///6n+//8E/v//Hf7///r+//9PAAAAoAEAAGQCAABDAgAANwEAAJz///8J/v//H/3//0r9//+O/v//fQAAAGECAAB3AwAAQAMAALgBAABj////H/3//9T7//8b/P//9v3//8QAAAB8AwAABQUAAKsEAABsAgAAC////8j7///1+f//aPr//yD9//8yAQAAGgUAAEYHAAC0BgAAagMAAIP+///U+f//P/f///f3///z+///2QEAAHgHAACJCgAAoQkAAM8EAAC0/f//9/b//1Pz//929P//TPr//9oCAADtCgAAQQ8AANMNAADEBgAAd/z//8ny//+l7f//cO////v3//9hBAAA+w8AABcWAADYEwAAgQkAAJX6//+t7P//bOX//zro//+89P//sgYAAF0XAAD6HwAAexwAAFgNAAC69///weP//4jZ///i3f//MvD//zYKAAAmIgAASC4AAN0oAAC3EgAAZ/P//7jW//9TyP//Ds///9np//+HDwAA5jEAAPpCAACeOgAANxoAAN/s//+ww///b6///8y5///84P//jRcAAOVIAADoYAAAEVQAAK4kAAAG4///6Kf//3CL//9Vm///o9T//6MjAAB1agAAMowAAIp4AABAMwAANNT//1x///9jV///rW///3PD///ONQAAb5sAAMnKAADLrAAAhEcAAPC9//8zRP//IQz//yMx//+Sq///FFEAAOTiAABFJQEApPcAAKRjAACKnP//5+3+/1af/v+R1/7/dIr///Z5AAAcSwEAEagBANJiAQCcigAAg2r//wxw/v8ZAv7/UVf+/59c//8ntwAAFuMBABhlAgBF/AEAfMAAAK8f//+KuP3/3R79/7yf/f9UHf//oBIBAKbAAgA+dgMA5dcCAM4KAQDnr/7/C638/4jW+/8Cmfz/H8b+/zGbAQCXAwQA4gAFACgSBAAQcQEAGgn+/zEn+/81/Pn/HyH7/0pO/v/bZgIAMdoFAPY6BwC30wUAY/0BAH8Q/f8l7/j/E0/3/30H+f8Zqv3/P5YDANGHCABWcgoAo1YIAFq9AgBYnvv/pLP1/5px8/+2Bvb/2sn8/71ZBQCCbgwAXRcPANbtCwARwwMAw3f5/2v+8P/W3O3/vrvx/7OY+///+AcA5hwSACXMFQCmDxEAgyYFAJJF9v9wI+r/EM7l/zWZ6/8h+/n/Ed4LAHxiGgCJeh8A7mQYACYHBwDFhvH/dSjg/28s2v9w1eL/Pc33/9WlEQANbSYA03MtAIfeIgDYjQkAnnzq/46h0f/mYsn/0lDW/63g9P8tOBoAbPM3AGqeQQDe0zEA+u4MAEEN4P+Zfbz/YCmx/1ZxxP9/+vD/o+smAJhzUQCjt14Aci5HAJFsEQB1mND/Ybud/8k1jv+o7qr/KdHr/+q5OQDvjHYAi7KIALinZQACWBcA57e5/+b8cP9Eylv/XYiG/0EL5f8qjVUAM4OsAG1AxQAUIZEApBIfAHPhl/+A6S//UxET/xedUv/3P9z/r7F+AL38+gB2lRwB1yDPAMcLKQA13WX/uEjR/vAxqv6DlQj/K/vQ/yx9uwCWFm0BvoOaAdSDJwG+uTUAyfob/561R/7k+xL+yBCf/jPIwv+MRBUBNPUSAswSUAJmeaUBAIpFAELnrv4UvH/98P44/Ua4CP5+SLH/LMWZAQQKBAMQylUDKOlYArPBWABi9w3+TBxd/DjL/vuUlTL9gV6c/3A3XQIIX2IEyPzOBCRuWAPoQ28AqKQg/aDStvoA/Tn6mLYB/IZ6hP/EWX0D4F5fBkiI7gbgJcQEaiyIAJDdwvuoVVH4YIyt97jVT/oCH2v/0OclBbDDQglwpv0JwKrJBtAjoQC4nL/5UDzW9KCeAfTgneb3rb5T/9gnlweApXQNsL1lDkC2qQn1QbUAsPnI9qAiyO/gwbfuAPd49BIqRf9whi8LYA6MEwB9vhQAGcANuDu7AFCGbPJAG3HooAIa5+CLme874Ev/4Kx5ECAdZBygJOIdAACPE9BzogAAQQLsgD7J3UCZItwAZK3oRcR9/+AlQRgApzopwK0KK2DhzhtaTU4AoJeT4kDIUc7A9ljMQPfY3gAAAAA='

# 500 sample sinusoid, float32, little-endian (Base64)
data_float32le_500 = b'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'

# 500 sample sinusoid, float64, little-endian (Base64)
data_float64le_500 = b'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'

# 500 sample sinusoid, Steim-1 (Base64)
data_steim1_500 = b'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'

# 499 sample sinusoid, Steim-2 (Base64)
data_steim2_499 = b'A///VQAAAADe2PdAgGQMqXYCIQZDq9s/TragGDPDYAoRSMA0LKsgDhlpEC4jgsAWIyYYAOXV0+MBIDQ3Iv/ZwRVqqqq+1wIwTE8w/cekocYFRm9xxF/nrPet467AkZiiyiGL9fhM9z34sDyXzrOoiv7NKuXujWwZzdVVUcxPfvQqqqqq5lm3FsK1Ee/eRFvJvzx9q77efrWAI4HbgWcCuIDE/6a+4Pyfvl7+LYA5griCCQPogRZ/br5bexm9qP1rKqqqqoBcA/yC8wWfgYj/GL2XeOW8ofxcgJGF1oRHCBOCKn6SvHj1s7spetyA5YiLhjMLmoMOfcG61PEUuQx4vyqqqqqBZwyCiPsQq4RO/IG4bupitgP1x4ItElCNAhfwhhF6lbTtYLCxqPGbg12ay5LXIl+Iinekr8zSqKto678qqqqqhS6nMJtIsViMAfMpf//QnX//vliicWOIh/K5TkAATwBAAEbSkN7sWH//urZ//6D0f/+rKKwDmEpAAFPGKqqqqkAAcltAAGWhl61iAn//mrl//3Zsf/+GQ6P3JQJAAHpvQAClgkAAkdBAAEJhf//SX3//bAB//zjmf/9RXSqqqqp//7FvQAA4O0AAsuNAAO+CQADRJkAAXPV//7rBf/8nyn/+3+d//wWJf/+SDUAAVThAAQVOQAFaiEABK+8qqqqqQACCAn//ly1//sQ3f/5fM3/+mNt//2ZTQACA30ABfZhAAfVMQAGuBkAAtZh//2Gnf/4y6X/9pRl//f0kKqqqqn//KX1AAMJ6QAItHUAC1RJAAmhmQAD9S3//EUZ//V7of/yYCn/9Hhd//tUEQAEk6kADLStABBiRQANzViqqqqpAAWDFf/6YwX/8Kax/+xMcf/vepn/+X+5AAbhqQASinEAF7CZABPGSQAHqhX/95E1/+ma3f/jg/n/6FUwqqqqqf/299kAClRxABsMkQAiP40AHFMVAAqjbf/zWeX/31Tt/9bSyf/eGqH/83mtAA97oQAnc9UAMYExACiPnKqqqqkADrz9/+0OBf/QW3X/xHw9/893ef/uqoEAFyyVADmHsQBHi8EAOhGtABRgNf/jqZX/uojh/6n+ff+6hsCqqqqp/+gP6QAipAUAU981AGdiYQBTHOEAHBsZ/9Wq0f+avUX/g7sZ/5yTwf/fBWEAM7exAHo/bQCVXgEAduz8qqqqqQAmq/n/wNXR/2xscf9MeR3/ccFh/9KvHQBNH9kAsiSlANfEkQCqH9UANRAt/6HbPf8o+H3+/K+R/zSLsKqqqqn/wemhAHLjfQEDigUBN6MFAPNMFQBIlnH/c9S1/sbBKf6Jf5X+3RP9/6s1eQCq+GUBeguRAcIHpQFb2CSqqqqpAGL06f8vgp3+N8ZB/eM7Pf5gIDX/jJ9NAP4vEQImi4ECicbhAfEsOQCGYuX+yi2F/WerwfzzRbn9ra4Mqqqqqf9jpOEBeY5NAyGWoQOqCAUCxmWpALW0of40AFn8ONep+5kELfyu61X/LRkZAjBTkQSO3a0FSfFlA/bCoKqqqqkA9HZh/VWaafqAQmn5pXUJ+0NTSf7lC3EDPuVZBqJA4Qeh8rkFqRNhAUcAMfwMfGH3/2It9tTWvfk8k6iqqqqp/oa7sQTPKXEJpyO1CwNjvQgUnmEBsncB+iXFcfRbVxHyxYMB9li34f4MqYEHHuZhDgsPuQ/jfPkLiBRwqqqqqQI8paH3VnZh7xAaKezqxJnyOeBh/XDa4QqJJWEUbSUpFusjORBzb4EC64sB8zARQedd5EHkeeOh7Fp+YKqqqqn8rYlBD5P9AR20gzUhDaStF3X2oQPEYMHtD+JB3C4u1dhO3u3j/KPB+759ARcE1IErMMxJL6lxeSFyH8CqqqqpBMm6geQGcAHL7IrhxsUqYdgSU8H6o52BIf4lAT7JUW1EtzKVL6nBAQX4HgHWs22BtE3PQa1/NMHHG/YAqqqqAfllawEyKysBW0GBFWMNhm1D5gSBB0AbAcMQzoGR/a/piRUpGa74woH4HLoBSgACAAAAAAAAAAAAAAAAA'

if __name__ == '__main__':
    main()
