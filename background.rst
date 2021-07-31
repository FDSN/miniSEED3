.. _background:

===============
Background
===============

The `Standard for the Exchange of Earthquake Data
<http://www.fdsn.org/publications/>`_ (SEED) was adopted by the FDSN
in the 1987 and served as the dominant standard for seismological
research data archiving and exchange for many decades.

The previous specification of miniSEED, latest 2.4, is defined as a
subset of SEED that contains only data records.

-----------------------
Changes relative to 2.4
-----------------------

An overview of significant changes between miniSEED 2.4 and this specification:

* Adoption of FDSN Source Identifiers, replacing independent SEED
  codes (network, station, location, channel).
* Incorporate critical details previously in blockettes (actual sample
  rate, encoding, microseconds) into the fixed section of the data
  header
* Increase sample rate/period representation to a 64-bit floating point value
* Increase start time resolution to nanoseconds
* Specify fixed byte order (little endian) for the binary portions of
  the headers and define a byte order for each data encoding
* Drop legacy data encodings and reserve their values so they are not
  used again in the future
* Add a format version
* Add a data publication version
* Add CRC field for validating integrity of record
* Add a “mass position off scale” flag
* Add “Recenter” (mass, gimbal, etc.) headers
* Add “ProvenanceURI” header to identify provenance documentation
* Replace the blockette structure with flexible extra header construct:

  * Specify a reserved set of extra headers defined by the FDSN, provide schema for validation
  * Previous flags and blockette contents defined in reserved extra headers
  * Allow arbitrary headers to be included in a record

* Remove the restriction on record length to be powers of 2, allow variable length

Near complete preservation of miniSEED 2.4 data.  Information that is
not retained is limited to: clock model specification per timing
exception (current specification only allows a single clock model
specification per record), Blockettes 400 (Beam) & 405 (Beam Delay)
and Blockette 2000 (Opaque Data).
