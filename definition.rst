
=================
Record definition
=================

The fundamental unit of the format is a data record.  A time series is
commonly stored and exchanged as a sequence of these records.  There
is no interdependence of records, each is independent.  There are data
encodings for integers, floats, text or compressed data samples.  To
limit problems with timing system drift and resolution in addition to
practical issues of subsetting and resource limitation for readers of
the data, typical record lengths for raw data generation and archiving
are recommended to be in the range of 256 and 4096 bytes.

Record layout and fields
========================

A record is composed of a header followed by a data payload. The byte
order of binary fields in the header must be least significant byte
first (little endian).

The total length of a record is variable and is the sum of 40 (length
of fixed section of header), field 10 (length of identifier), field 11
(length of extra headers), field 12 (length of payload).

+--------------------+--------------------------+-------+------+------+---------------------+
|Field               |Description               |Type   |Length|Offset|Content              |
+====================+==========================+=======+======+======+=====================+
|:ref:`1 <field-1>`  |Record header indicator   |CHAR   |2     |0     |ASCII 'MS'           |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`2 <field-2>`  |Format version            |UINT8  |1     |2     |Value of 3           |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`3 <field-3>`  |Flags                     |UINT8  |1     |3     |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|                    |Record start time         |       |      |      |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`4a <field-4>` |Nanosecond (0 - 999999999)|UINT32 |4     |4     |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`4b <field-4>` |Year (0-65535)            |UINT16 |2     |8     |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`4c <field-4>` |Day-of-year  (1 - 366)    |UINT16 |2     |10    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`4d <field-4>` |Hour (0 - 23)             |UINT8  |1     |12    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`4e <field-4>` |Minute (0 - 59)           |UINT8  |1     |13    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`4f <field-4>` |Second (0 - 60)           |UINT8  |1     |14    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`5 <field-5>`  |Data payload encoding     |UINT8  |1     |15    |:ref:`data-encodings`|
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`6 <field-6>`  |Sample rate/period        |FLOAT64|8     |16    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`7 <field-7>`  |Number of samples         |UINT32 |4     |24    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`8 <field-8>`  |CRC of the record         |UINT32 |4     |28    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`9 <field-9>`  |Data publication version  |UINT8  |1     |32    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`10 <field-10>`|Length of identifier      |UINT8  |1     |33    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`11 <field-11>`|Length of extra headers   |UINT16 |2     |34    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`12 <field-12>`|Length of data payload    |UINT32 |4     |36    |                     |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`13 <field-13>`|Source identifier         |CHAR   |V     |40    |URI identifier       |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`14 <field-14>`|Extra header fields       |JSON   |V     |40 + field 10               |
+--------------------+--------------------------+-------+------+------+---------------------+
|:ref:`15 <field-15>`|Data payload              |encoded|V     |40 + field 10 + field 11    |
+--------------------+--------------------------+-------+------+------+---------------------+

All length values are specified in bytes, which are assumed to be
8-bits in length.  Data types for each field are defined as follows:

:CHAR:    ASCII encoded character data.
:UINT8:   Unsigned 8-bit integer.
:UINT16:  Unsigned 16-bit integer (little endian byte order).
:UINT32:  Unsigned 32-bit integer (little endian byte order).
:FLOAT64: IEEE-754 64-bit floating point number (little endian byte order).
:JSON:    JSON Data Interchange Standard.

Description of record fields
============================

.. _field-1:

:1: CHAR: **Record header indicator**.  Literal, 2-character sequence
    “MS”, ASCII 77 and 83, designating the start of a record.

.. _field-2:

:2: UINT8: **Format version**.  Set to 3 for this version.  When a
    non-backwards compatible change is introduced the version will be
    incremented.

.. _field-3:

:3: UINT8: **Flags**.  Bit field flags, with bits 0-7 defined as:

      0. Calibration signals present.  [same as SEED 2.4 FSDH, field 12, bit 0]
      1. Time tag is questionable.  [same as SEED 2.4 FSDH, field 14, bit 7]
      2. Clock locked.  [same as SEED 2.4 FSDH, field 13, bit 5]
      3. Reserved for future use.
      4. Reserved for future use.
      5. Reserved for future use.
      6. Reserved for future use.
      7. Reserved for future use.

.. _field-4:

:4: **Record start time**, time of the first data sample.  A
    representation of UTC using individual fields for:

      a. nanosecond
      b. year
      c. day-of-year
      d. hour
      e. minute
      f. second

    A 60 second value is used to represent a time value
    during a positive leap second.  If no time series data are
    included in this record, the time should be relevant for whatever
    headers or flags are included.

.. _field-5:

:5: UINT8: **Data payload encoding**.  A code indicating the encoding
    format, see Section 4: Data encoding codes for a list of valid
    codes.  If no data payload is included set this value to 0.

.. _field-6:

:6: FLOAT64: **Sample rate/period**.  Sample rate encoded in 64-bit
    IEEE-754 floating point format.  When the value is positive it
    represents the rate in samples per second, when it is negative it
    represents the sample period in seconds.  Creators should use the
    negative value sample period notation for rates less than 1
    samples per second to retain resolution. Set to 0.0 if no time
    series data are included in the record.

.. _field-7:

:7: UINT32: **Number of samples**.  Total number of data samples in the
     data payload.  Set to 0 if no samples (header-only records) or
     unknown number of samples (e.g. for opaque payload encoding).

.. _field-8:

:8: UINT32: **CRC of the record**.  CRC-32C (Castagnoli) value of the
    complete record with the 4-byte CRC field set to zeros.  The
    CRC-32C (Castagnoli) algorithm with polynomial 0x1EDC6F41
    (reversed 0x82F63B78) to be used is defined in `RFC 3309
    <https://datatracker.ietf.org/doc/html/rfc3309>`_, which further
    includes references to the relevant background material.

.. _field-9:

:9: UINT8: **Data publication version**.  Values should only be
    considered relative to each other for data from the same data
    center.  Semantics may vary between data centers but generally
    larger values denote later and more preferred data.  Recommended
    values: 1 for raw data, 2+ for revisions produced later,
    incremented for each revision.  A value of 0 indicates unknown
    version such as when data are converted to miniSEED from another
    format.  Changes to this value for user-versioning are not
    recommended, instead an extra header should be used to allow for 
    user-versioning of different derivatives of the data.

.. _field-10:

:10: UINT8: **Length of identifier**.  Length, in bytes, of source
     identifier in field 13.

.. _field-11:

:11: UINT16: **Length of extra headers**.  Length, in bytes, of extra
     headers in field 14.  If no extra headers, set this value to 0.

.. _field-12:

:12: UINT32: **Length of data payload**.  Length, in bytes, of data
     payload starting in field 15.  If no data payload is present, 
     set this value to 0. Note that no padding is permitted in the 
     data record itself, although padding may exist within the 
     payload depending on the type of encoding used.

.. _field-13:

:13: CHAR: **Source identifier**.  A unique identifier of the source
     of the data contained in the record.  Recommended to use
     URI-based identfiers.  Commonly an `FDSN Source Identifier
     <http://docs.fdsn.org/projects/source-identifiers/>`_.

.. _field-14:

:14: JSON: **Extra header fields**.  Extra fields of variable length
     encoded in JavaScript Object Notation (JSON) Data Interchange
     Standard as defined by `ECMA-404
     <https://www.ecma-international.org/publications-and-standards/standards/ecma-404/>`_.
     It is strongly recommended to store compact JSON, containing no
     non-data white space, in this field to avoid wasted space.

     A reserved set of headers fields is defined by the FDSN, see
     :ref:`extra-headers`.  Other header fields may be present and
     should be defined by the organization that created them.

.. _field-15:

:15: encoded: **Data payload**. Length indicated in field 12, encoding
     indicated in field 5.
