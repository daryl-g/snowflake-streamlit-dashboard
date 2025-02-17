-- This file is only used with Snowflake CLI (configured in snowflake.yml)

-- For more information, refer to https://docs.snowflake.com/en/developer-guide/native-apps/preparing-data-content

-- mark that our application package depends on an external database in
-- the provider account. By granting "reference_usage", the proprietary data
-- in the opta_data database can be shared through the app
grant reference_usage on database opta_data
    to share in application package {{ package_name }};

-- now that we can reference our proprietary data, let's create some views
-- this "package schema" will be accessible inside of our setup script
create schema if not exists {{ package_name }}.package_shared;
use schema {{ package_name }}.package_shared;

-- View for contestants data
create view if not exists package_shared.contestants_view
    as select   contestantId,
                contestantName,
                contestantShortName,
                contestantOfficialName,
                contestantCode,
                contestantCountryId,
                contestantCountryName
    from opta_data.data.contestants;

-- View for competitions data
create view if not exists package_shared.competitions_view
    as select   competitionId,
                competitionName,
                competitionCode,
                competitionAreaId,
                competitionAreaName,
                tournamentCalendarId,
                tournamentCalendarName,
                tournamentCalendarStartDate,
                tournamentCalendarEndDate
    from opta_data.data.competitions;

-- View for matches data
create view if not exists package_shared.matches_info_view
    as select   matchId,
                competitionId,
                tournamentCalendarId,
                matchDescription,
                matchDate,
                matchTime,
                contestantId1,
                contestantId2
    from opta_data.data.matches_info;

-- View for match details data
create view if not exists package_shared.match_details_view
    as select   matchId,
                matchLengthMin,
                matchLengthSec,
                matchAttendance,
                matchRefereeId,
                matchRefereeName,
                matchRefereeCountryId,
                matchRefereeCountryName
    from opta_data.data.match_details;

-- these grants allow our setup script to actually refer to our views
grant usage on schema package_shared
  to share in application package {{ package_name }};
grant select on view package_shared.sensor_types_view
  to share in application package {{ package_name }};
grant select on view package_shared.sensor_ranges
  to share in application package {{ package_name }};
grant select on view package_shared.sensor_service_schedules
  to share in application package {{ package_name }};