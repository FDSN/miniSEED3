#!/bin/bash
#
# Build reference data using record generator and converters.
#
# The records are built in this directory, when ready they can be copied
# to the parent directory where the reference data are located.
#
# The mseed3-json and mseeed3-text converters are available from:
# https://github.com/iris-edu/mseed3-utils

# Event detection, extra headers only
echo Building reference-detectiononly.mseed3
./generate_miniseed3.py -s 0 -Y 2004 -D 210 -H 20 -M 28 -S 9 -N 0 -e ../../extra-headers/Example-ExtraHeaders-FDSN-Detection.json -V 2 -i FDSN:XX_TEST__L_H_Z > reference-detectiononly.mseed3
mseed3-json -d reference-detectiononly.mseed3 > reference-detectiononly.json
mseed3-text -d reference-detectiononly.mseed3 > reference-detectiononly.txt

# Text data
echo Building reference-text.mseed3
./generate_miniseed3.py -p text -i FDSN:XX_TEST__L_O_G > reference-text.mseed3
mseed3-json -d reference-text.mseed3 > reference-text.json
mseed3-text -d reference-text.mseed3 > reference-text.txt

# 16-bit integer data
echo Building reference-sinusoid-int16.mseed3
./generate_miniseed3.py -p int16 -i FDSN:XX_TEST__L_H_Z -s 1 -f 00000100 > reference-sinusoid-int16.mseed3
mseed3-json -d reference-sinusoid-int16.mseed3 > reference-sinusoid-int16.json
mseed3-text -d reference-sinusoid-int16.mseed3 > reference-sinusoid-int16.txt

# 32-bit integer data
echo Building reference-sinusoid-int32.mseed3
./generate_miniseed3.py -p int32 -i FDSN:XX_TEST__V_H_Z -s -10 -f 00000100 > reference-sinusoid-int32.mseed3
mseed3-json -d reference-sinusoid-int32.mseed3 > reference-sinusoid-int32.json
mseed3-text -d reference-sinusoid-int32.mseed3 > reference-sinusoid-int32.txt

# 32-bit float data
echo Building reference-sinusoid-float32.mseed3
./generate_miniseed3.py -p float32 -i FDSN:XX_TEST__B_H_Z -s 20 > reference-sinusoid-float32.mseed3
mseed3-json -d reference-sinusoid-float32.mseed3 > reference-sinusoid-float32.json
mseed3-text -d reference-sinusoid-float32.mseed3 > reference-sinusoid-float32.txt

# 64-bit float data
echo Building reference-sinusoid-float64.mseed3
./generate_miniseed3.py -p float64 -i FDSN:XX_TEST__H_H_Z -s 100 > reference-sinusoid-float64.mseed3
mseed3-json -d reference-sinusoid-float64.mseed3 > reference-sinusoid-float64.json
mseed3-text -d reference-sinusoid-float64.mseed3 > reference-sinusoid-float64.txt

# Steim-1 compressed data
echo Building reference-sinusoid-steim1.mseed3
./generate_miniseed3.py -p steim1 -i FDSN:XX_TEST__L_H_Z -s 1 -f 00000100 > reference-sinusoid-steim1.mseed3
mseed3-json -d reference-sinusoid-steim1.mseed3 > reference-sinusoid-steim1.json
mseed3-text -d reference-sinusoid-steim1.mseed3 > reference-sinusoid-steim1.txt

# Steim-2 compressed data
echo Building reference-sinusoid-steim2.mseed3
./generate_miniseed3.py -p steim2 -i FDSN:XX_TEST__M_H_Z -s 5 -f 00000100 > reference-sinusoid-steim2.mseed3
mseed3-json -d reference-sinusoid-steim2.mseed3 > reference-sinusoid-steim2.json
mseed3-text -d reference-sinusoid-steim2.mseed3 > reference-sinusoid-steim2.txt

# Steim-2 compressed data, with time quality, correction, and event detections
echo Building reference-sinusoid-TQ-TC-ED.mseed3
./generate_miniseed3.py -p steim2 -i FDSN:XX_TEST__L_H_Z -s 1 -N 123000000 -f 00000100 -e ../../extra-headers/Example-ExtraHeaders-FDSN-TQ-ED.json > reference-sinusoid-TQ-TC-ED.mseed3
mseed3-json -d reference-sinusoid-TQ-TC-ED.mseed3 > reference-sinusoid-TQ-TC-ED.json
mseed3-text -d reference-sinusoid-TQ-TC-ED.mseed3 > reference-sinusoid-TQ-TC-ED.txt

# Steim-2 compressed data, with FDSN and non-FDSN extra headers
echo Building reference-sinusoid-FDSN-Other.mseed3
./generate_miniseed3.py -p steim2 -i FDSN:XX_TEST__L_H_Z -s 1 -N 123000000 -f 00000100 -e ../../extra-headers/Example-ExtraHeaders-FDSN-Other.json > reference-sinusoid-FDSN-Other.mseed3
mseed3-json -d reference-sinusoid-FDSN-Other.mseed3 > reference-sinusoid-FDSN-Other.json
mseed3-text -d reference-sinusoid-FDSN-Other.mseed3 > reference-sinusoid-FDSN-Other.txt

# Steim-2 compressed data, with all FDSN extra headers
echo Building reference-sinusoid-FDSN-All.mseed3
./generate_miniseed3.py -p steim2 -i FDSN:XX_TEST__L_H_Z -s 1 -N 123000000 -f 00000100 -e ../../extra-headers/Example-ExtraHeaders-FDSN-All.json > reference-sinusoid-FDSN-All.mseed3
mseed3-json -d reference-sinusoid-FDSN-All.mseed3 > reference-sinusoid-FDSN-All.json
mseed3-text -d reference-sinusoid-FDSN-All.mseed3 > reference-sinusoid-FDSN-All.txt

echo
echo "Copy new reference-* files to the parent directory to replace canonical reference files"
