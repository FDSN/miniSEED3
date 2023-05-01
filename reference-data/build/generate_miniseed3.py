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
        'int16': (base64.b64decode(data_int16le_400), 1, 400),
        'int32': (base64.b64decode(data_int32le_500), 3, 500),
        'float32': (base64.b64decode(data_float32le_500), 4, 500),
        'float64': (base64.b64decode(data_float64le_500), 5, 500),
        'steim1': (base64.b64decode(data_steim1_500), 10, 500),
        'steim2': (base64.b64decode(data_steim2_500), 11, 500),
    }.get(choice, (None, None, None)) # Default is all None


# Below are data payloads of different encodings
# Non-text data samples are that of an expanding sinusoid.

# ASCII text
data_text = "I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, like tears...in...rain. Time to die.".encode('utf-8')

# 400 sample sinusoid, 16-bit integer, little-endian (Base64)
data_int16le_400 = b'AAACAAQABQAHAAkACgALAAsACwALAAoACAAGAAQAAQAAAP3/+v/4//X/8//y//H/8P/x//L/8//1//j/+////wIABgAJAA0AEAASABQAFQAWABUAEwARAA4ACgAFAAAA/P/3//L/7f/p/+b/4//i/+L/4//m/+r/7v/0//v/AQAIAA8AFgAcACEAJgAoACkAKQAnACMAHQAWAA4ABQD8//L/6P/f/9f/0P/L/8j/x//I/8z/0v/a/+X/8P/9/woAFwAlADEAPABEAEsATgBOAEsARQA8ADAAIQARAAAA7f/a/8j/uP+q/5//mP+U/5X/mv+k/7L/xP/Z//D/CAAiADsAUwBpAHsAiQCSAJUAkgCJAHoAZQBLAC0ADADq/8f/pP+E/2j/Uf9A/zb/NP86/0n/YP9//6T/zv/9/ywAXQCLALYA2wD5AA0BGAEXAQsB8wDQAKQAbgAyAPP/sP9u/y//9v7G/qD+iP5+/oT+mf6+/vL+M/+A/9T/LQCJAOMANwGCAcEB7wELAhICBALgAacBWgH8AJAAGQCd/x//pf40/tL9g/1K/Sz9Kv1G/YD91/1I/s/+af8PALsAZwEMAqECIQOGA8kD5wPeA6sDUAPOAioCZwGOAKf/uf7P/fL8LPyH+wn7u/qh+r76FPui+2P8Uv1n/pj/2gAgAl4DhQSJBV0G+AZPB10HHgeRBroFnQREA7sBDwBS/pP85vpc+Qn4+/ZB9ub18fVn9kf3i/gs+hv8R/6cAAMDZQWmB68JaAu7DJYN6g2wDeQMhwujCUUHggRzATT+5vqq96T09fG+7xruIu3m7HDtw+7a8KbzEvf/+kv/ywNTCLQMvRBAFBQXEhkeGiIaExnyFsgTrQ/BCjEFMP/3+Mfy4OyE5/LiYd8B3fnbYNxD3p3hWuZW7GHzO/uZAyoMlhSCHJYjfinwLa4wiDFiMDMtByj/IFEYSQ5AA6H33+t04N3VkcwBxY2/hrwkvIm+uMOXy/LVdOKw8CQAORBOILkv0T3ySYpTGVo4XaRcO1gDUCpECDUXI/gOafk540/NkrjrpTKWLIo='

# 500 sample sinusoid, 32-bit integer, little-endian (Base64)
data_int32le_500 = b'AAAAAAIAAAAEAAAABQAAAAcAAAAJAAAACgAAAAsAAAALAAAACwAAAAsAAAAKAAAACAAAAAYAAAAEAAAAAQAAAAAAAAD9////+v////j////1////8/////L////x////8P////H////y////8/////X////4////+/////////8CAAAABgAAAAkAAAANAAAAEAAAABIAAAAUAAAAFQAAABYAAAAVAAAAEwAAABEAAAAOAAAACgAAAAUAAAAAAAAA/P////f////y////7f///+n////m////4////+L////i////4////+b////q////7v////T////7////AQAAAAgAAAAPAAAAFgAAABwAAAAhAAAAJgAAACgAAAApAAAAKQAAACcAAAAjAAAAHQAAABYAAAAOAAAABQAAAPz////y////6P///9/////X////0P///8v////I////x////8j////M////0v///9r////l////8P////3///8KAAAAFwAAACUAAAAxAAAAPAAAAEQAAABLAAAATgAAAE4AAABLAAAARQAAADwAAAAwAAAAIQAAABEAAAAAAAAA7f///9r////I////uP///6r///+f////mP///5T///+V////mv///6T///+y////xP///9n////w////CAAAACIAAAA7AAAAUwAAAGkAAAB7AAAAiQAAAJIAAACVAAAAkgAAAIkAAAB6AAAAZQAAAEsAAAAtAAAADAAAAOr////H////pP///4T///9o////Uf///0D///82////NP///zr///9J////YP///3////+k////zv////3///8sAAAAXQAAAIsAAAC2AAAA2wAAAPkAAAANAQAAGAEAABcBAAALAQAA8wAAANAAAACkAAAAbgAAADIAAADz////sP///27///8v////9v7//8b+//+g/v//iP7//37+//+E/v//mf7//77+///y/v//M////4D////U////LQAAAIkAAADjAAAANwEAAIIBAADBAQAA7wEAAAsCAAASAgAABAIAAOABAACnAQAAWgEAAPwAAACQAAAAGQAAAJ3///8f////pf7//zT+///S/f//g/3//0r9//8s/f//Kv3//0b9//+A/f//1/3//0j+///P/v//af///w8AAAC7AAAAZwEAAAwCAAChAgAAIQMAAIYDAADJAwAA5wMAAN4DAACrAwAAUAMAAM4CAAAqAgAAZwEAAI4AAACn////uf7//8/9///y/P//LPz//4f7//8J+///u/r//6H6//+++v//FPv//6L7//9j/P//Uv3//2f+//+Y////2gAAACACAABeAwAAhQQAAIkFAABdBgAA+AYAAE8HAABdBwAAHgcAAJEGAAC6BQAAnQQAAEQDAAC7AQAADwAAAFL+//+T/P//5vr//1z5//8J+P//+/b//0H2///m9f//8fX//2f2//9H9///i/j//yz6//8b/P//R/7//5wAAAADAwAAZQUAAKYHAACvCQAAaAsAALsMAACWDQAA6g0AALANAADkDAAAhwsAAKMJAABFBwAAggQAAHMBAAA0/v//5vr//6r3//+k9P//9fH//77v//8a7v//Iu3//+bs//9w7f//w+7//9rw//+m8///Evf////6//9L////ywMAAFMIAAC0DAAAvRAAAEAUAAAUFwAAEhkAAB4aAAAiGgAAExkAAPIWAADIEwAArQ8AAMEKAAAxBQAAMP////f4///H8v//4Oz//4Tn///y4v//Yd///wHd///52///YNz//0Pe//+d4f//Wub//1bs//9h8///O/v//5kDAAAqDAAAlhQAAIIcAACWIwAAfikAAPAtAACuMAAAiDEAAGIwAAAzLQAABygAAP8gAABRGAAASQ4AAEADAACh9///3+v//3Tg///d1f//kcz//wHF//+Nv///hrz//yS8//+Jvv//uMP//5fL///y1f//dOL//7Dw//8kAAAAORAAAE4gAAC5LwAA0T0AAPJJAACKUwAAGVoAADhdAACkXAAAO1gAAANQAAAqRAAACDUAABcjAAD4DgAAafn//znj//9Pzf//krj//+ul//8ylv//LIr//3+C//+pf////IH//5WJ//9clv//Aqj///+9//+b1///7/P//+sRAABoMAAAKk4AAPBpAACAggAAt5YAAJGlAAA6rgAAFrAAAMiqAAA+ngAArooAAJ5wAADZUAAAciwAALcEAAAo2///ZbH//yWJ//8eZP//+EP//zkq//80GP//9w7//0AP//9xGf//iC3//xlL//9Rcf//+p7//4LS//8HCgAAbkMAAG18AACpsgAAyuMAAJQNAQAELgEAYEMBAFRMAQD+RwEAADYBAIUWAQBN6gAAoLIAAFFxAACoKAAAVdv//1OM///QPv//C/b+/zS1/v9Jf/7/9Vb+/24+/v9fN/7/yUL+//dg/v9zkf7//9L+/54j//+egP//sOb//wFSAABhvgAAZicBAJyIAQCx3QEApiICAP1TAgDdbgIAQXECAAtaAgAiKQIAet8BABR/AQD2CgEAFYcAADj4///IY///pc/+/+hB/v+pwP3/ulH9/2z6/P9Qv/z//KP8/9+q/P8c1fz/aSL9/wyR/f8='

# 500 sample sinusoid, float32, little-endian (Base64)
data_float32le_500 = b'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'

# 500 sample sinusoid, float64, little-endian (Base64)
data_float64le_500 = b'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'

# 500 sample sinusoid, Steim-1 (Base64)
data_steim1_500 = b'AVVVVQAAAAD//ZEMAAICAQICAQEAAAD//v7+/f/9/f79/v///wEBAQIDAwQDBAMEAwICAQH//v79/Pv7/Pv7+xVVVVX8/f3/AAEDBAQGBwYHBwcGBQUCAQD+/Pr5+Pf39vb3+Pn7/f8BBAYICwsNDQ0ODAsIBwMA/fr39PHw7+0VVVVV7e7w8vX5/AEFCg4SFRcYGhkYFhIOCQP99/Hr5uLf3t3d4OTp7/b+Bg8XHyUqLy8xLislHhQL//To3dTKFVVVqsTBvb7Bx9Da6PYGFSU0QU1UWVxaVEs/LhwH8tzHs6KUiYSCho+escfi/hw6AFcAcQCHAJoApgCsAKwApSaqmqoAlQCAZUMe9//N/6X/fv9c/z3/J/8Z/xL/Fv8j/zr/W4Ky5h0AVgCOAMEA7wEVATEBQgFGAT4BJwEEANQqqqqqAJsAVwAO/8H/c/8p/uP+p/53/lT+Q/5B/lP+dv6t/vL/Rv+lAAsAdgDgAUQBoQHvAiwCVQJnAmICQQIJKqqqqgG5AVMA2wBU/8b/NP6j/hz9ov09/PH8wfyy/MT8+v1R/cn+XP8I/8QAigFTAhcCzANsA+0ETASABIgEYSqqqqoECQODAtQB/gEMAAT+8f3f/Nb75fsU+nD5//nH+dD6Gfqk+278b/2g/vgAZwHjA1oEvQX8BwsH2gheCJEqqqqqCGwH7AcUBegEcgK+ANr+2vzR+tT4+PdS9fj09/Rh9D70lfVp9rT4cPqM/Pn/ngJlBS8H3wpbDIIOPA90KqqqqhAVEBUPaw4YDCEJmAaPAx//bPuX98j0J/De7g/r4epx6dDqFutD7VnwR/P6+FP9KgJTB5kMxxGmFf0ZnCqqqqocVB38Hn0dwhvGGJAUNw7aCKkB3Pqy83bscOXw4DvbmdhF1nHWPdfA2vnf2uZB7fv2wwBJCjEUFx2RJjgqqqqqLakziDeFOWc4/zY8MSEpyiBwFVwI9Puq7gLghdPIyFO+sbdXsq2w/rJ9tzu/KcoV16znefjxC2oeLjB8Kqqv/0GMUJ9dAGYSa1FsYGkFYTZVFUT1MVca4AJk6MrPF7ZYn5qL4v//fB///3Ej//9rkP//a93//3JD//9+wSqAAACREaiyxOTkrAbjKj1NTW6jAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='

# 500 sample sinusoid, Steim-2 (Base64)
data_steim2_500 = b'A////wAAAAD//ZEMgCISIYEAD+6O393tjv/xEYIzQ0OEMiEfju3LvIu7zd+AE0Rnhnd2VYIQ7Klxe9rXiJvfFD//9dVMha2tWuYtB0YO6vQxwvttLsMteTwEUo4SVXYaGWFkjgkP3fHr5uLf3t3d4CSm/b4GDxcfJSovLzEuKyU1VVVaHlC/9Ojd1MrEwb2+wcfQ2uj2BhUlNEFNVFlcWlRLPy4cB/Lcx7OilImEgoaPnrHH4v4cOsVxxIfJopisKaqqqsrClJXIAZRDHvfNpfftcz3yfGcS8WyPOvW+C7L+YHRWyOME79FUxULUZPkn0ENQm8VwO8H3PKbj6nneVCqqqqrkOQZT52q28vRulAvHY4FEgNCB74EWAlWBM4JigSCCCduVTNvFTxs0v1H+HL7RfT2+ePzBvll8xL59fVEqqqqqvuT+XPCPEIqAqYIXgWYDbIH2hEyCQASIgjCECYHBgtTf5DAEv3j9375re+W9inpwvP/5x7zoehm9UntuKqqqqr43/aDvgZ3jga0EvYL+BwuD7QhehEiIbIP2BxSC9ARygV8A2r9tfNG9anj4u6l1+Lp79GG6H3SVurT2tCqqqqq8OHqMvnz/noEyhS+D74pbhkEOPIe6EBWICo9rhwwMIYTMBo+Bj/9svcv3yLoT8N63B+vhtTjp0LULa0MqqqqqtqzwR7n9eFO+lQJTg8yMx4jTFf2MzhxUjv4efY7hG8aMSBQ3h20IqYDuerK5u2xwsvhgO63M2EWrONY9KqqqqqvgWvmv7WZBtv32w4AkijGKC52RkxwtqZnEN4Wcs7j/mx4xIZTlIHCKrgj0vdVuArBC08h//8hTf/++sSqqqqp//7dXf/+yrX//sP5//7J9f/+3O3//vymlCtess7z48YW1Hi5AADB8QABBjEAAUJ9AAF0AQABmEkAAa1EqqqqqQABsYEAAaQVAAGE2QABVFUAARPWYq5rggTJoyn//zxd//7ZYf/+fmn//i+J//3wff/9xI3//a5B//2vdKqqAAH//ckN//37Bf/+REX//qLKicmSsg3GqPUAATU1AAG6jAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='


if __name__ == '__main__':
    main()
