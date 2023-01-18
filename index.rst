.. FDSN miniSEED 3 documentation master file

========================
Overview
========================

The `International Federation of Digital Seismograph Networks
<http://www.fdsn.org/>`_ (FDSN) defines **miniSEED** as a format for
digital data and related information.  The primary intended uses are
data collection, archiving and exchange of seismological data.  The
format is also appropriate for time series data from other geophysical
measurements such as pressure, temperature, tilt, etc.  In addition to
the time series, storage of related state-of-health and parameters
documenting the state of the recording system are supported.  The FDSN
metadata counterpart of miniSEED is `StationXML <http://docs.fdsn.org/projects/stationxml>`_
which is used to describe characteristics needed to interpret the data
such as location, instrument response, etc.

----------
Versioning
----------

Starting with version 3 of **miniSEED**, the specification version is a single
integer. Any non-backward compatible change to the structure of the header or
record results in an increment to this number. The specification version
corresponds to :ref:`field 2, Format version<field-2>`, in the
header of records written to conform
with this version of the specification. There are no minor revisions.
However, the addition of new data encodings or new reserved headers is
considered backwards compatible. The FDSN may add encodings and extra headers
within the FDSN key or make editorial changes to the specification without change to the
major version, resulting only in a new revision of the specification document.
Note that all parsing software MUST allow for the potential of unknown, new data
encodings and new extra headers as these are subject to extension. This
requirement allows older software to parse future records successfully within
the same specification major version, even though they may be unable to
decompress the data payload for new encodings.

This document is miniSEED |doc_version|.

.. note::
   This specification defines miniSEED |major_version|.  See
   :ref:`background` for information on earlier versions.

.. toctree::
   :maxdepth: 2

   self
   definition
   data-encodings
   extra-headers
   fdsn-reserved
   background
   appendix
   software
   changes
   FDSN home <https://www.fdsn.org/>
