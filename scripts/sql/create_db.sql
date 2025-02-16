-- This file contains the SQL commands to create the database schema.

-- Set context
use role accountadmin;
use warehouse dashboard_wh;

-- Create the database
create database if not exists opta_data;
use database opta_data;
-- Create the schema
create schema if not exists data;
use schema data;


-- Create tables
-- Contestants/Teams
create or replace table contestants (
    contestantId varchar,
    contestantName varchar not null,
    contestantShortName varchar not null,
    contestantOfficialName varchar not null,
    contestantCode varchar not null,
    contestantCountryId varchar not null,
    contestantCountryName varchar not null,
    primary key(contestantId)
);

-- Competitions
create or replace table competitions (
    competitionId varchar,
    competitionName varchar not null,
    competitionCode varchar not null,
    competitionAreaId varchar not null,
    competitionAreaName varchar not null,
    tournamentCalendarId varchar not null,
    tournamentCalendarName varchar not null,
    tournamentCalendarStartDate date not null,
    tournamentCalendarEndDate date not null,
    primary key(competitionId, tournamentCalendarId)
);

-- Matches
create or replace table matches_info (
    matchId varchar,
    matchDescription varchar not null,
    matchDate date not null,
    matchTime time not null,
    contestantId1 varchar not null,
    contestantId2 varchar not null,
    competitionId varchar not null,
    competitionName varchar not null,
    tournamentCalendarId varchar not null,
    primary key(matchId),
    foreign key(contestantId1) references contestants(contestantId),
    foreign key(contestantId2) references contestants(contestantId),
    foreign key(competitionId, tournamentCalendarId) references competitions(competitionId, tournamentCalendarId)
);

create or replace table match_details (
    matchId varchar not null,
    matchLengthMin int not null,
    matchLengthSec int not null,
    numberOfPeriods int not null,
    periodLength int not null,
    overtimeLength int not null,
    periods array not null,
    scores array not null,
    primary key(matchId),
    foreign key(matchId) references matches_info(matchId)
);

-- Players
create or replace table players (
    contestantId varchar not null,
    playerId varchar,
    playerKnownName varchar not null,
    playerMatchName varchar not null,
    primary key(playerId),
    foreign key(contestantId) references contestants(contestantId),
);

-- Events
create or replace table events (
    eventId varchar,
    contestantId varchar not null,
    matchId varchar not null,
    playerId varchar,
    typeId int not null,
    periodId int not null,
    matchMin int not null,
    matchSec int not null,
    eventOutcome varchar not null,
    eventX float not null,
    eventY float not null,
    timeStamp timestamp_ntz not null,
    qualifiers array not null,
    primary key(eventId),
    foreign key(contestantId) references contestants(contestantId),
    foreign key(matchId) references matches_info(matchId),
    foreign key(playerId) references players(playerId)
);

-- Pass matrix
create or replace table pass_matrix (
    contestantId varchar not null,
    matchId varchar not null,
    playerId varchar not null,
    avgX float not null,
    avgY float not null,
    passSuccess int not null,
    passLost int not null,
    playerPasses array not null,
    primary key(contestantId, matchId, playerId),
    foreign key(contestantId) references contestants(contestantId),
    foreign key(matchId) references matches_info(matchId),
    foreign key(playerId) references players(playerId)
);

-- xG-related stuff
create or replace table xgoal (
    contestantId varchar not null,
    matchId varchar not null,
    playerId varchar not null,
    stats array not null,
    primary key(contestantId, matchId, playerId),
    foreign key(contestantId) references contestants(contestantId),
    foreign key(matchId) references matches_info(matchId),
    foreign key(playerId) references players(playerId)
);

-- General stats
create or replace table player_stats (
    contestantId varchar not null,
    matchId varchar not null,
    playerId varchar not null,
    stats array not null,
    primary key(contestantId, matchId, playerId),
    foreign key(contestantId) references contestants(contestantId),
    foreign key(matchId) references matches_info(matchId),
    foreign key(playerId) references players(playerId)
);

create or replace table contestant_stats (
    contestantId varchar not null,
    matchId varchar not null,
    generalStats array not null,
    xgoalStats array not null,
    primary key(contestantId, matchId),
    foreign key(contestantId) references contestants(contestantId),
    foreign key(matchId) references matches_info(matchId)
);