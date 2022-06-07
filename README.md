# FDSN miniSEED 3 specification

The [International Federation of Digital Seismograph
Networks](https://www.fdsn.org/) (FDSN) defines `miniSEED` as a format
for digital data and related information.  The primary intended uses
are data collection, archiving and exchange of seismological data.
The format is also appropriate for time series data from other
geophysical measurements such as pressure, temperature, tilt, etc.  In
addition to the time series, storage of related state-of-health and
parameters documenting the state of the recording system are
supported.  The FDSN metadata counterpart of miniSEED is StationXML
which is used to describe characteristics needed to interpret the data
such as location, instrument response, etc.

This repository contains the source of the documentation and serves as
a coordination point for additions and changes to the specification.

Specification releases are at:
https://docs.fdsn.org/projects/miniSEED3

## Documentation source organization

* The `draft` branch contains the latest draft documentation
* Specification releases are branches from `main`, following a release:
** the version (in conf.py) is updated appropriately on the branch, never in main

## Change procedure

The specification is maintained by FDSN [Working Group II](http://fdsn.org/wg/wgII/).

To propose changes a submitter must provide two things:

* A written description of the change (motivations, potential impact, etc.).
* A fork of the most recent `draft` branch of the repository submitted
  as a pull request (PR) on GitHub.  The PR should include the changes
  being proposed.

The procedure is as follows:

1. Submitter sends written proposal to the WG-II mailing list, with or
   without a link to a GitHub pull request or issue.
2. If written proposal is approved by WG-II but no pull request was
   submitted, the proposer should submit a pull request to the repository
   and send a link to the WG-II for technical review.
3. If the written proposal and technical review of the pull request
   are approved by WG-II, a gatekeeper will merge the pull request.

The change will then be included in the next release.

For technical discussion of a potential change without creating pull request,
an issue may be created.  The procedure for Working Group II,
described above, must be followed for any changes.

Changes and issues should only be grouped together when logically
related in order to streamline review and acceptance.

## Documentation build and publishing status:
[![Documentation Status](https://readthedocs.org/projects/miniSEED3/badge/?version=latest)](http://docs.fdsn.org/projects/miniSEED3/en/latest/?badge=latest)
