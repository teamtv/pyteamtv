## 0.15.0 (2022-11-15)

Feature:
- Add cache layer

## 0.14.0 (2022-11-14)

Feature:
- Populate resource metadata when available

## 0.13.2 (2022-10-20)

Bugfix:
- Add missing pol2cart function
- Improve exception when TOKEN is not set

## 0.13.1 (2022-10-12)

Bugfix:
- Fix in dataframe builder

## 0.13.0 (2022-10-12)

*Breaking release*
`ObservationLog.to_pandas` is removed.

Feature:
- Add data frame builder

## 0.12.0/0.12.1 (2022-10-12)

Feature:
- Provide team information from sporting event 

## 0.11.1 (2022-10-06)

Bugfix:
- Handle 'POSSESSION' events correctly

## 0.11.0 (2022-09-20)

Feature:
- Allow video_id and clock_id to be passed for to get_observation_log 

## 0.10.0 (2022-07-25)

Feature:
- Add bulk observation

## 0.9.1 (2022-07-01)

Bugfix:
- Don't break when backend sends an empty list instead of a empty dictionary

## 0.9.0 (2022-07-01)

Feature:
- Add models for Person, Player, LineUp, EventStream

## 0.8.2 (2022-06-10)

Bugfix:
- Make sure bool(List) returns correct result based on items

## 0.8.1 (2022-06-08)

Bugfix:
- Pass description to initVideoUpload

## 0.8.0 (2022-06-03)

Feature:
- Add support for video tags

## 0.7.1 (2022-04-01)

Bugfix:
- Correct time format for Clock

## 0.7.0 (2022-04-01)

Feature:
- Add Clock to SportingEvent

## 0.1.0 (2022-01-14)

Feature:
- Add `upload_video` method to `SportingEvent`. This makes it possible to directly upload one or multiple files to an SportingEvent.