.. _FDSN-reserved-headers:

======================
FDSN Reserved Headers
======================

The **"FDSN"** key at the root of the :ref:`extra-headers` are reserved for
definition by the FDSN.  See :ref:`example-fdsn-extra-headers` for an example
of FDSN extra headers.

The FDSN reserved headers are defined and documented in `JSON Schema <http://json-schema.org/>`_.

Download the `FDSN Extra Header schema v1.0 <https://raw.githubusercontent.com/FDSN/miniSEED3/main/extra-headers/ExtraHeaders-FDSN-v1.0.schema-2023-07.json>`_.

The documentation and schema of these headers may be browsed here:

.. raw:: html
  :file: extra-headers/ExtraHeaders-FDSN-v1.0.schema.html

|

When not present, the boolean values in the FDSN reserved headers
should be considered to be `false` unless otherwise documented.  Such
values do not need to be included when the value is `false`.
