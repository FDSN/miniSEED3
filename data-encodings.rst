.. _data-encodings:

==============
Data Encodings
==============

Data payload encodings in the format are identified by a code
(number).  These codes are assigned by the FDSN. A list of valid codes
are as follows:

+-------+------------------------------------------------------------------------------+
|Code   |Description                                                                   |
+=======+==============================================================================+
|**0**  | Text, UTF-8 allowed, use ASCII for maximum portability, no structure defined |
+-------+------------------------------------------------------------------------------+
|**1**  | 16-bit integer (two’s complement), little endian byte order                  |
+-------+------------------------------------------------------------------------------+
|**3**  | 32-bit integer (two’s complement), little endian byte order                  |
+-------+------------------------------------------------------------------------------+
|**4**  | 32-bit floats (IEEE float), little endian byte order                         |
+-------+------------------------------------------------------------------------------+
|**5**  | 64-bit floats (IEEE double), little endian byte order                        |
+-------+------------------------------------------------------------------------------+
|**10** | Steim-1 integer compression, big endian byte order                           |
+-------+------------------------------------------------------------------------------+
|**11** | Steim-2 integer compression, big endian byte order                           |
+-------+------------------------------------------------------------------------------+
|**19** | Steim-3 integer compression, big endian (not in common use in archives)      |
+-------+------------------------------------------------------------------------------+
|**100**| Opaque data - only for use in special scenarios, not intended for archiving  |
+-------+------------------------------------------------------------------------------+

Overview and description of the Steim-1 and Steim-2 compression
encodings may be found in the SEED 2.4 manual, Appendix B.

----------------------------
Retroactive future encodings
----------------------------

New data encodings may be added to the format in the future without
incrementing the format version.  There is no default encoding,
readers must check the encoding value to determine if the encoding is
supported.

----------------------------------------------------------
Retired encoding values, not allowed in this specification
----------------------------------------------------------

The following numeric codes were used in earlier miniSEED versions and
should `not` be used for encodings defined in the future:

:2:  24-bit integers
:12: GEOSCOPE multiplexed format 24-bit integer
:13: GEOSCOPE multiplexed format 16-bit gain ranged, 3-bit exponent
:14: GEOSCOPE multiplexed format 16-bit gain ranged, 4-bit exponent
:15: US National Network compression
:16: CDSN 16-bit gain ranged
:17: Graefenberg 16-bit gain ranged
:18: IPG-Strasbourg 16-bit gain ranged
:30: SRO format
:31: HGLP format
:32: DWWSSN gain ranged format
:33: RSTN 16-bit gain ranged format
