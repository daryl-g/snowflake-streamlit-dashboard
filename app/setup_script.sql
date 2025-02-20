-- This SQL script contains the SQL commands to set up the Native App.

-- This is the setup script that will run while installing your application instance in a consumer's account.
-- For more information on how to create setup file, visit https://docs.snowflake.com/en/developer-guide/native-apps/creating-setup-script

-- this app exposes 2 application roles: admin and viewer
create application role if not exists app_admin;
create application role if not exists app_viewer;

-- viewer permissions are a subset of those for the admin
grant application role app_viewer to application role app_admin;

-- the config data schema holds configuration data
-- we create a non-versioned schema "if not exists"
-- so that we do not clobber state whenever we upgrade the app
create schema if not exists config_data;
    grant usage on schema config_data to application role app_admin;
    execute immediate from './sql/config_data-configuration.sql';

-- the ui schema holds all streamlits
create or alter versioned schema ui;
    grant usage on schema ui to application role app_viewer;
    execute immediate from './sql/ui-landing_page.sql';
    -- execute immediate from './sql/ui-how_to.sql';
    -- execute immediate from './sql/ui-last_match.sql';
    -- execute immediate from './sql/ui-player_individual.sql';
    -- execute immediate from './sql/ui-player_overall.sql';

-- simple generic methods to register callbacks
create or alter versioned schema config_code;
    grant usage on schema config_code to application role app_admin;
    execute immediate from './sql/config_code-register_single_callback.sql';

-- we need two views for each table we want to share from the provider through the app:
-- one set of views live in the package schema; the other set of views are defined here
create or alter versioned schema shared_content;
    execute immediate from './sql/shared_content-contestants.sql';
    execute immediate from './sql/shared_content-competitions.sql';
    execute immediate from './sql/shared_content-match_details.sql';
    execute immediate from './sql/shared_content-matches_info.sql';

    -- share the views with the app roles
    grant select on all tables in schema shared_content to application role app_viewer;

    grant select on all tables in schema shared_content to application role app_admin;

