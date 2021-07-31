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

.. note::
   This specification defines version 3 of miniSEED.  See
   :ref:`background` for information on earlier versions.

.. toctree::
   :maxdepth: 2

   self
   definition
   data-encodings
   extra-headers
   background
   appendix
   software
   changes
   FDSN home <https://www.fdsn.org/>

* :ref:`search`

