.. _appendix:

=======================================
Appendix
=======================================

.. _example-fdsn-extra-headers:

---------------------------------------
A: Extra header examples
---------------------------------------

The example extra header structures below include additional white
space and formatting for readability, which should not be used in an
actual record.

+++++++++++++++++++++++++++
FDSN reserved extra headers
+++++++++++++++++++++++++++

A relatively simple example of reserved FDSN extra headers that
contains a timing quality value and an event detection is:

.. literalinclude:: extra-headers/Example-ExtraHeaders-FDSN-TQ-ED.json
  :language: JSON

An example of the reserved FDSN headers defined by the FDSN is
provided below.  In this (pathalogical) illustration, all reserved
fields are represented.

.. literalinclude:: extra-headers/Example-ExtraHeaders-FDSN-All.json
  :language: JSON

.. _example-non-fdsn-extra-headers:

+++++++++++++++++++++++++++
Non-FDSN extra headers
+++++++++++++++++++++++++++

An example of reserved FDSN headers combined with other top-level
headers, illustrating how custom headers may be added.

.. literalinclude:: extra-headers/Example-ExtraHeaders-FDSN-Other.json
  :language: JSON

---------------------------------------
B: Reference data
---------------------------------------

The reference data set is intended as an illustration of properly
constructed miniSEED 3 and to be used by software implementors during
development and testing.

The set contains multiple examples of data records illustrating
different characteristics and data encodings of the from. Each example
is available in miniSEED 3, JSON, and human-readable text representations.

The whole data set may be downloaded from documentation repository.

All time series in the reference set that contain series are
the same expanding sinusoid signal.

===  ================================================================  =====================================================================
#    Description                                                       Download
===  ================================================================  =====================================================================
1    Text payload                                                      :download:`mseed3 <reference-data/reference-text.mseed3>` :download:`JSON <reference-data/reference-text.json>` :download:`Text <reference-data/reference-text.txt>`
2    Event detection headers only, no data payload                     :download:`mseed3 <reference-data/reference-detectiononly.mseed3>` :download:`JSON <reference-data/reference-detectiononly.json>` :download:`Text <reference-data/reference-detectiononly.txt>`
3    Sinusoid series encoded as 16-bit integers                        :download:`mseed3 <reference-data/reference-sinusoid-int16.mseed3>` :download:`JSON <reference-data/reference-sinusoid-int16.json>` :download:`Text <reference-data/reference-sinusoid-int16.txt>`
4    Sinusoid series encoded as 32-bit integers                        :download:`mseed3 <reference-data/reference-sinusoid-int32.mseed3>` :download:`JSON <reference-data/reference-sinusoid-int32.json>` :download:`Text <reference-data/reference-sinusoid-int32.txt>`
5    Sinusoid series encoded as 32-bit IEEE float                      :download:`mseed3 <reference-data/reference-sinusoid-float32.mseed3>` :download:`JSON <reference-data/reference-sinusoid-float32.json>` :download:`Text <reference-data/reference-sinusoid-float32.txt>`
6    Sinusoid series encoded as 64-bit IEEE float                      :download:`mseed3 <reference-data/reference-sinusoid-float64.mseed3>` :download:`JSON <reference-data/reference-sinusoid-float64.json>` :download:`Text <reference-data/reference-sinusoid-float64.txt>`
7    Sinusoid series encoded as Steim-1 compressed integers            :download:`mseed3 <reference-data/reference-sinusoid-steim1.mseed3>` :download:`JSON <reference-data/reference-sinusoid-steim1.json>` :download:`Text <reference-data/reference-sinusoid-steim1.txt>`
8    Sinusoid series encoded as Steim-2 compressed integers            :download:`mseed3 <reference-data/reference-sinusoid-steim2.mseed3>` :download:`JSON <reference-data/reference-sinusoid-steim2.json>` :download:`Text <reference-data/reference-sinusoid-steim2.txt>`
9    Series with time quality, correction, event detections headers    :download:`mseed3 <reference-data/reference-sinusoid-TQ-TC-ED.mseed3>` :download:`JSON <reference-data/reference-sinusoid-TQ-TC-ED.json>` :download:`Text <reference-data/reference-sinusoid-TQ-TC-ED.txt>`
10   Series with some FDSN and non-FDSN extra headers                  :download:`mseed3 <reference-data/reference-sinusoid-FDSN-Other.mseed3>` :download:`JSON <reference-data/reference-sinusoid-FDSN-Other.json>` :download:`Text <reference-data/reference-sinusoid-FDSN-Other.txt>`
11   Series with all FDSN extra headers (unrealistic)                  :download:`mseed3 <reference-data/reference-sinusoid-FDSN-All.mseed3>` :download:`JSON <reference-data/reference-sinusoid-FDSN-All.json>` :download:`Text <reference-data/reference-sinusoid-FDSN-All.txt>`
===  ================================================================  =====================================================================

---------------------------------------
C: Mapping from miniSEED 2.4
---------------------------------------

.. include:: appendix-24mapping.rst


