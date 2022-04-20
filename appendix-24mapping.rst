.. _appendix-24mapping:

The following list of miniSEED 2.4 format structures specifies the
mapping of all fields to this specification.  In this listing the
following abbreviations are used:

:EH:   Extra Header (of this specification), with path
:SID:  Source Identifier (of this specification)
:FSDH: Fixed Section Data Header (in either specification)

++++++++++++++++++++++++++++++++++++++++++++++
miniSEED 2.4 Fixed Section Data Header (FSDH)
++++++++++++++++++++++++++++++++++++++++++++++

+-----+--------------------------------+----------------------------------------+
|Field|Description                     |This specification                      |
+=====+================================+========================================+
|1    |Sequence number                 |EH: `FDSN.Sequence`                     |
+-----+--------------------------------+----------------------------------------+
|2    |Data header/quality indicator   |EH: `FDSN.DataQuality`                  |
|     |                                |                                        |
|     |                                | | A data center may choose to          |
|     |                                | | translate miniSEED 2.4 quality       |
|     |                                | | values to publication versions       |
|     |                                | | with the following mapping:          |
|     |                                |                                        |
|     |                                |   +-------------+--------------+       |
|     |                                |   |2.4 quality  |Pub. version  |       |
|     |                                |   +=============+==============+       |
|     |                                |   |      R      |      1       |       |
|     |                                |   +-------------+--------------+       |
|     |                                |   |      D      |      2       |       |
|     |                                |   +-------------+--------------+       |
|     |                                |   |      Q      |      3       |       |
|     |                                |   +-------------+--------------+       |
|     |                                |   |      M      |      4       |       |
|     |                                |   +-------------+--------------+       |
+-----+--------------------------------+----------------------------------------+
|3    |Reserved byte                   | [no mapping]                           |
+-----+--------------------------------+----------------------------------------+
|4    |Station identifier code         | Incorporated into SID, FSDH field 13   |
+-----+--------------------------------+----------------------------------------+
|5    |Location identifier             | Incorporated into SID, FSDH field 13   |
+-----+--------------------------------+----------------------------------------+
|6    |Channel identifier              | Incorporated into SID, FSDH field 13   |
+-----+--------------------------------+----------------------------------------+
|7    |Network code                    | Incorporated into SID, FSDH field 13   |
+-----+--------------------------------+----------------------------------------+
|8    |Record start time               | FSDH field 4                           |
+-----+--------------------------------+----------------------------------------+
|9    |Number of samples               | FSDH field 7                           |
+-----+--------------------------------+----------------------------------------+
|10   |Sample rate factor              | Incorporated into FSDH field 6         |
+-----+--------------------------------+----------------------------------------+
|11   |Sample rate multiplier          | Incorporated into FSDH field 6         |
+-----+--------------------------------+----------------------------------------+
|12   |Activity flags:                 |FSDH and Extra headers:                 |
|     | | 0 = calibration signals      | | FSDH field 3, bit 0                  |
|     | | 1 = time correction applied  | | [no mapping]                         |
|     | | 2 = begining of event        | | `FDSN.Event.Begin`                   |
|     | | 3 = end of event             | | `FDSN.Event.End`                     |
|     | | 4 = + leap second included   | | `FDSN.Time.LeapSecond`               |
|     | | 5 = - leap second included   | | `FDSN.Time.LeapSecond`               |
|     | | 6 = event in progress        | | `FDSN.Event.InProgress`              |
+-----+--------------------------------+----------------------------------------+
|13   |I/O flags, bits:                |FSDH and Extra headers:                 |
|     | | 0 = Sta. volume parity error | | `FDSN.Flags.StationVolumeParityError`|
|     | | 1 = Long record read         | | `FDSN.Flags.LongRecordRead`          |
|     | | 2 = Short record read        | | `FDSN.Flags.ShortRecordRead`         |
|     | | 3 = Start of time series     | | `FDSN.Flags.StartOfTimeSeries`       |
|     | | 4 = End of time series       | | `FDSN.Flags.EndOfTimeSeries`         |
|     | | 5 = Clock locked             | | FSDH field 3, bit 2                  |
+-----+--------------------------------+----------------------------------------+
|14   |Data quality flags, bits:       |FSDH and Extra headers:                 |
|     | | 0 = Amp. saturation detected | | `FDSN.Flags.AmplifierSaturation`     |
|     | | 1 = Dig. clipping detected   | | `FDSN.Flags.DigitizerClipping`       |
|     | | 2 = Spikes detected          | | `FDSN.Flags.Spikes`                  |
|     | | 3 = Glitches detected        | | `FDSN.Flags.Glitches`                |
|     | | 4 = Missing/padded data      | | `FDSN.Flags.MissingData`             |
|     | | 5 = Telemetry synch. error   | | `FDSN.Flags.TelemetrySyncError`      |
|     | | 6 = Digital filter charging  | | `FDSN.Flags.FilterCharging`          |
|     | | 7 = Time tag questionable    | | FSDH field 3, bit 1                  |
+-----+--------------------------------+----------------------------------------+
|15   |Number of blockettes that follow|[no mapping]                            |
+-----+--------------------------------+----------------------------------------+
|16   |Time correction                 | EH: `FDSN.Time.Correction`             |
+-----+--------------------------------+----------------------------------------+
|17   |Beginning of data               | [no mapping]                           |
+-----+--------------------------------+----------------------------------------+
|18   |First blockette                 | [no mapping]                           |
+-----+--------------------------------+----------------------------------------+

++++++++++++++++++++++++++++++++++
Blockette 100 (Sample Rate)
++++++++++++++++++++++++++++++++++

+-----+--------------------------------+----------------------------------------+
|Field|Description                     |This specification                      |
+=====+================================+========================================+
|3    |Actual sample rate              | FSDH field 6                           |
+-----+--------------------------------+----------------------------------------+
|4    |Flags (undefined)               | [no mapping]                           |
+-----+--------------------------------+----------------------------------------+
|4    |Reserved byte                   | [no mapping]                           |
+-----+--------------------------------+----------------------------------------+

+++++++++++++++++++++++++++++++++++++++
Blockette 200 (Generic Event Detection)
+++++++++++++++++++++++++++++++++++++++

+-----+---------------------------+---------------------------------------------+
|Field|Description                |This specification                           |
+=====+===========================+=============================================+
|3    |Signal amplitude           | EH: `FDSN.Event.Detection.SignalAmplitude`  |
+-----+---------------------------+---------------------------------------------+
|4    |Signal period              | EH: `FDSN.Event.Detection.SignalPeriod`     |
+-----+---------------------------+---------------------------------------------+
|5    |Background estimate        |EH: `FDSN.Event.Detection.BackgroundEstimate`|
+-----+---------------------------+---------------------------------------------+
|6    |Event detection flag bits: |Extra headers:                               |
|     | | 0 = dil./comp. wave     | | `FDSN.Event.Detection.Wave`               |
|     | | 1 = units               | | `FDSN.Event.Detection.Units`              |
+-----+---------------------------+---------------------------------------------+
|7    |Reserved byte              | [no mapping]                                |
+-----+---------------------------+---------------------------------------------+
|8    |Signal onset time          | EH: `FDSN.Event.Detection.OnsetTime`        |
+-----+---------------------------+---------------------------------------------+
|9    |Detector name              | EH: `FDSN.Event.Detection.Detector`         |
+-----+---------------------------+---------------------------------------------+

+++++++++++++++++++++++++++++++++++++++
Blockette 201 (Murdock Event Detection)
+++++++++++++++++++++++++++++++++++++++

+-----+---------------------------+---------------------------------------------+
|Field|Description                |This specification                           |
+=====+===========================+=============================================+
|3    |Signal amplitude           | EH: `FDSN.Event.Detection.SignalAmplitude`  |
+-----+---------------------------+---------------------------------------------+
|4    |Signal period              | EH: `FDSN.Event.Detection.SignalPeriod`     |
+-----+---------------------------+---------------------------------------------+
|5    |Background estimate        |EH: `FDSN.Event.Detection.BackgroundEstimate`|
+-----+---------------------------+---------------------------------------------+
|6    |Event detection flag bits: |Extra headers:                               |
|     | | 0 = dil./comp. wave     | | `FDSN.Event.Detection.Wave`               |
+-----+---------------------------+---------------------------------------------+
|7    |Reserved byte              | [no mapping]                                |
+-----+---------------------------+---------------------------------------------+
|8    |Signal onset time          | EH: `FDSN.Event.Detection.OnsetTime`        |
+-----+---------------------------+---------------------------------------------+
|9    |Signal-to-noise values     | EH: `FDSN.Event.Detection.MEDSNR` (array)   |
+-----+---------------------------+---------------------------------------------+
|10   |Lookback value             | EH: `FDSN.Event.Detection.MEDLookback`      |
+-----+---------------------------+---------------------------------------------+
|11   |Pick algorithm             | EH: `FDSN.Event.Detection.MEDPickAlgorithm` |
+-----+---------------------------+---------------------------------------------+
|12   |Detector name              | EH: `FDSN.Event.Detection.Detector`         |
+-----+---------------------------+---------------------------------------------+

+++++++++++++++++++++++++++++++++++++++
Blockette 300 (Step Calibration)
+++++++++++++++++++++++++++++++++++++++

+-----+-------------------+-----------------------------------------------------+
|Field|Description        |This specification                                   |
+=====+===================+=====================================================+
|3    |Start calib        | EH: `FDSN.Calibration.Sequence.Begintime`           |
+-----+-------------------+-----------------------------------------------------+
|4    |Num of calibs      | EH: `FDSN.Calibration.Sequence.Steps`               |
+-----+-------------------+-----------------------------------------------------+
|5    |Calibration flags: |Extra headers:                                       |
|     | | 0 = first pulse | | `FDSN.Calibration.Sequence.StepFirstPulsePositive`|
|     | | 1 = cal alt sign| | `FDSN.Calibration.Sequence.StepAlternateSign`     |
|     | | 2 = cal auto    | | `FDSN.Calibration.Sequence.Trigger`               |
|     | | 3 = cal cont    | | `FDSN.Calibration.Sequence.Continued`             |
+-----+-------------------+-----------------------------------------------------+
|6    |Duration of step   | EH: `FDSN.Calibration.Sequence.Duration`            |
+-----+-------------------+-----------------------------------------------------+
|7    |Time between steps | EH: `FDSN.Calibration.Sequence.StepBetween`         |
+-----+-------------------+-----------------------------------------------------+
|8    |Amp. of cal. signal| EH: `FDSN.Calibration.Sequence.Amplitude`           |
+-----+-------------------+-----------------------------------------------------+
|9    |Channel cal. signal| EH: `FDSN.Calibration.Sequence.InputChannel`        |
+-----+-------------------+-----------------------------------------------------+
|10   |Reserved byte      | [no mapping]                                        |
+-----+-------------------+-----------------------------------------------------+
|11   |Reference amplitude| EH: `FDSN.Calibration.Sequence.ReferenceAmplitude`  |
+-----+-------------------+-----------------------------------------------------+
|12   |Coupling of signal | EH: `FDSN.Calibration.Sequence.Coupling`            |
+-----+-------------------+-----------------------------------------------------+
|13   |Rolloff of filters | EH: `FDSN.Calibration.Sequence.Rolloff`             |
+-----+-------------------+-----------------------------------------------------+

+++++++++++++++++++++++++++++++++++++++
Blockette 310 (Sine Calibration)
+++++++++++++++++++++++++++++++++++++++

+-----+-------------------+-----------------------------------------------------+
|Field|Description        |This specification                                   |
+=====+===================+=====================================================+
|3    |Start calib        | EH: `FDSN.Calibration.Sequence.Begintime`           |
+-----+-------------------+-----------------------------------------------------+
|4    |Reserved byte      | [no mapping]                                        |
+-----+-------------------+-----------------------------------------------------+
|5    |Calibration flags: |Extra headers:                                       |
|     | | 2 = cal auto    | | `FDSN.Calibration.Sequence.Trigger`               |
|     | | 3 = cal cont    | | `FDSN.Calibration.Sequence.Continued`             |
|     | | 4 = PtoP amp    | | `FDSN.Calibration.Sequence.AmplitudeRange`        |
|     | | 5 = ZtoP amp    | | `FDSN.Calibration.Sequence.AmplitudeRange`        |
|     | | 6 = RMS amp     | | `FDSN.Calibration.Sequence.AmplitudeRange`        |
+-----+-------------------+-----------------------------------------------------+
|6    |Duration of cal    | EH: `FDSN.Calibration.Sequence.Duration`            |
+-----+-------------------+-----------------------------------------------------+
|7    |Period of signal   | EH: `FDSN.Calibration.Sequence.Period`              |
+-----+-------------------+-----------------------------------------------------+
|8    |Amp. of cal. signal| EH: `FDSN.Calibration.Sequence.Amplitude`           |
+-----+-------------------+-----------------------------------------------------+
|9    |Channel cal. signal| EH: `FDSN.Calibration.Sequence.InputChannel`        |
+-----+-------------------+-----------------------------------------------------+
|10   |Reserved byte      | [no mapping]                                        |
+-----+-------------------+-----------------------------------------------------+
|11   |Reference amplitude| EH: `FDSN.Calibration.Sequence.ReferenceAmplitude`  |
+-----+-------------------+-----------------------------------------------------+
|12   |Coupling of signal | EH: `FDSN.Calibration.Sequence.Coupling`            |
+-----+-------------------+-----------------------------------------------------+
|13   |Rolloff of filters | EH: `FDSN.Calibration.Sequence.Rolloff`             |
+-----+-------------------+-----------------------------------------------------+

++++++++++++++++++++++++++++++++++++++++++
Blockette 320 (Pseudo-random Calibration)
++++++++++++++++++++++++++++++++++++++++++

+-----+-------------------+-----------------------------------------------------+
|Field|Description        |This specification                                   |
+=====+===================+=====================================================+
|3    |Start calib        | EH: `FDSN.Calibration.Sequence.Begintime`           |
+-----+-------------------+-----------------------------------------------------+
|10   |Reserved byte      | [no mapping]                                        |
+-----+-------------------+-----------------------------------------------------+
|5    |Calibration flags: |Extra headers:                                       |
|     | | 2 = cal auto    | | `FDSN.Calibration.Sequence.Trigger`               |
|     | | 3 = cal cont    | | `FDSN.Calibration.Sequence.Continued`             |
|     | | 4 = Random amps | | `FDSN.Calibration.Sequence.AmplitudeRange`        |
+-----+-------------------+-----------------------------------------------------+
|6    |Duration of cal    | EH: `FDSN.Calibration.Sequence.Duration`            |
+-----+-------------------+-----------------------------------------------------+
|7    |PtoP amp. of steps | EH: `FDSN.Calibration.Sequence.Amplitude`           |
+-----+-------------------+-----------------------------------------------------+
|8    |Channel cal. signal| EH: `FDSN.Calibration.Sequence.InputChannel`        |
+-----+-------------------+-----------------------------------------------------+
|9    |Reserved byte      | [no mapping]                                        |
+-----+-------------------+-----------------------------------------------------+
|10   |Reference amplitude| EH: `FDSN.Calibration.Sequence.ReferenceAmplitude`  |
+-----+-------------------+-----------------------------------------------------+
|11   |Coupling of signal | EH: `FDSN.Calibration.Sequence.Coupling`            |
+-----+-------------------+-----------------------------------------------------+
|12   |Rolloff of filters | EH: `FDSN.Calibration.Sequence.Rolloff`             |
+-----+-------------------+-----------------------------------------------------+
|13   |Noise type         | EH: `FDSN.Calibration.Sequence.Noise`               |
+-----+-------------------+-----------------------------------------------------+

++++++++++++++++++++++++++++++++++++++++++
Blockette 390 (Generic Calibration)
++++++++++++++++++++++++++++++++++++++++++

+-----+-------------------+-----------------------------------------------------+
|Field|Description        |This specification                                   |
+=====+===================+=====================================================+
|3    |Start calib        | EH: `FDSN.Calibration.Sequence.Begintime`           |
+-----+-------------------+-----------------------------------------------------+
|10   |Reserved byte      | [no mapping]                                        |
+-----+-------------------+-----------------------------------------------------+
|5    |Calibration flags: |Extra headers:                                       |
|     | | 2 = cal auto    | | `FDSN.Calibration.Sequence.Trigger`               |
|     | | 3 = cal cont    | | `FDSN.Calibration.Sequence.Continued`             |
+-----+-------------------+-----------------------------------------------------+
|6    |Duration of cal    | EH: `FDSN.Calibration.Sequence.Duration`            |
+-----+-------------------+-----------------------------------------------------+
|7    |Amplitude of signal| EH: `FDSN.Calibration.Sequence.Amplitude`           |
+-----+-------------------+-----------------------------------------------------+
|8    |Channel cal. signal| EH: `FDSN.Calibration.Sequence.InputChannel`        |
+-----+-------------------+-----------------------------------------------------+
|9    |Reserved byte      | [no mapping]                                        |
+-----+-------------------+-----------------------------------------------------+

++++++++++++++++++++++++++++++++++++++++++
Blockette 395 (Calibration Abort)
++++++++++++++++++++++++++++++++++++++++++

+-----+-------------------+-----------------------------------------------------+
|Field|Description        |This specification                                   |
+=====+===================+=====================================================+
|3    |End calib          | EH: `FDSN.Calibration.Sequence.Endtime`             |
+-----+-------------------+-----------------------------------------------------+
|10   |Reserved byte      | [no mapping]                                        |
+-----+-------------------+-----------------------------------------------------+

++++++++++++++++++++++++++++++++++++++++++++++++
Blockette 400 (Beam), Blockette 405 (Beam Delay)
++++++++++++++++++++++++++++++++++++++++++++++++

No mapping for these blockettes

+++++++++++++++++++++++++++++++++++++++
Blockette 500 (Timing)
+++++++++++++++++++++++++++++++++++++++

+-----+---------------------------+---------------------------------------------+
|Field|Description                |This specification                           |
+=====+===========================+=============================================+
|3    |VCO correction             | EH: `FDSN.Time.Exception.VCOCorrection`     |
+-----+---------------------------+---------------------------------------------+
|4    |Time of exception          | EH: `FDSN.Time.Exception.Time`              |
+-----+---------------------------+---------------------------------------------+
|5    |Microsecond offset         | [included in record start time]             |
+-----+---------------------------+---------------------------------------------+
|6    |Reception quality          | EH: `FDSN.Time.Exception.ReceptionQuality`  |
+-----+---------------------------+---------------------------------------------+
|7    |Exception count            | EH: `FDSN.Time.Exception.Count`             |
+-----+---------------------------+---------------------------------------------+
|8    |Exception type             | EH: `FDSN.Time.Exception.Type`              |
+-----+---------------------------+---------------------------------------------+
|9    |Clock model                | EH: `FDSN.Clock.Model`                      |
+-----+---------------------------+---------------------------------------------+
|10   |Clock status               | EH: `FDSN.Time.Exception.ClockStatus`       |
+-----+---------------------------+---------------------------------------------+

+++++++++++++++++++++++++++++++++++++++
Blockette 1000 (Data Only SEED)
+++++++++++++++++++++++++++++++++++++++

+-----+---------------------------+---------------------------------------------+
|Field|Description                |This specification                           |
+=====+===========================+=============================================+
|3    |Encoding format            | FSDH field 5                                |
+-----+---------------------------+---------------------------------------------+
|4    |Word order                 | [no mapping, no longer needed]              |
+-----+---------------------------+---------------------------------------------+
|5    |Data record length         | [no mapping, no longer needed]              |
+-----+---------------------------+---------------------------------------------+
|6    |Reserved byte              | [no mapping]                                |
+-----+---------------------------+---------------------------------------------+

+++++++++++++++++++++++++++++++++++++++
Blockette 1001 (Data Extension)
+++++++++++++++++++++++++++++++++++++++

+-----+---------------------------+---------------------------------------------+
|Field|Description                |This specification                           |
+=====+===========================+=============================================+
|3    |Timing quality             | EH: `FDSN.Time.Quality`                     |
+-----+---------------------------+---------------------------------------------+
|4    |Microsecond offset         | Incorporated into FSDH field 4              |
+-----+---------------------------+---------------------------------------------+
|5    |Reserved byte              | [no mapping]                                |
+-----+---------------------------+---------------------------------------------+
|6    |Frame count                | [no mapping]                                |
+-----+---------------------------+---------------------------------------------+

++++++++++++++++++++++++++++++++++++++++++++++++
Blockette 2000 (Variable Length Opaque)
++++++++++++++++++++++++++++++++++++++++++++++++

No mapping for this blockette.  The opaque data encoding may be used
to specify an opaque payload for nearly equivalent functionality.

++++++++++++++++++++++++++++++++++
Unsupported miniSEED 2.4 content
++++++++++++++++++++++++++++++++++

The following defined information in miniSEED 2.4 cannot be represented in this specification:

- Clock model specification per timing exception.  Current
  specification only allows a single clock model specification per
  record.

- Blockettes 400 (Beam) & 405 (Beam Delay)

- Blockette 2000 (Opaque Data)
