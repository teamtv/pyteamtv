## 0.30.3 (2024-11-18)

Bugfix:
- make api access lazy so it won't hit the api's on token validation

## 0.30.2 (2024-11-11)

Bugfix:
- Fix for token check: add leeway

## 0.30.1 (2024-11-01)

Bugfix:
- is_upload_completed for livestream

## 0.30.0 (2024-10-31)

Feature:
- Add livestream

## 0.29.0 (2024-09-26)

Feature:
- Use tuspy >= 1.0.0 instead of ==1.0.0, as there is a wheel for 1.0.3 
- Add get_state to EventStream

## 0.28.0 (2024-03-13)

Feature:
- Add sync videos

## 0.27.0 (2024-03-07)

Feature:
- Add connect/read timeout to upload

## 0.26.3 (2024-01-25)

Bugfix:
- Fix _session - part 2

## 0.26.2 (2024-01-25)

Bugfix:
- Fix _session 

## 0.26.1 (2024-01-02)

Bugfix:
- Add missing `get_access_requester`

## 0.26.0 (2023-12-19)

Feature:
- Add `raise_on_missing_token` to `get_current_app`

## 0.25.1 (2023-12-06)

Bugfix:
- Use personId from nested data when attribute doesn't exist anymore at top level


## 0.25.0 (2023-11-17)

Feature:
- Add possession_id and all available observations

## 0.24.3 (2023-10-04)

Bugfix:
- Set tus retries/retry_delay to sane values

## 0.24.2 (2023-10-03)

Bugfix:
- Fix get_last_event

## 0.24.1 (2023-10-03)

Bugfix:
- Make get_last_event available

## 0.24.0 (2023-10-03)

Feature:
- Add EventStreamReader

## 0.23.0 (2023-09-04)

Feature:
- Allow sportType for sharing groups api

## 0.22.1 (2023-08-23)

Bugfix:
- Fix in DataframeBuilder when opponentPerson is filled

## 0.22.0 (2023-07-06)

Feature:
- Add basic LearningGroup support

## 0.21.0 (2023-05-18)

Feature:
- Add `timeout` argument for `Requester`, with default of 30 seconds

## 0.20.0 (2023-01-25)

Feature:
- Make decoding of token available output of TeamTVApp

## 0.19.0 (2023-01-15)

Feature:
- Resume uploads

## 0.18.1 (2022-12-09)

Bugfix:
- Move `is_local` to `TeamTVObject`

## 0.18.0 (2022-12-09)

Feature:
- Do some cleaning when loading teams
- Add type to SportingEvent (match or training)

## 0.17.0 (2022-12-08)

Feature:
- Add has privilege check, and original item

## 0.16.0 (2022-11-25)

Bugfix:
- Accept training SportingEvent type

Feature:
- Make it possible to pass skipTranscoding parameter

## 0.15.2 (2022-11-15)

Bugfix:
- Make Api pickleable

## 0.15.1 (2022-11-15)

Bugfix:
- Add caching for apps

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