-- create consumer role
create role if not exists dashboard_admin;
create role if not exists dashboard_viewer;
grant role dashboard_admin to role accountadmin;
grant role dashboard_viewer to role accountadmin;
grant create database on account to role dashboard_admin;
grant create application on account to role dashboard_admin;
grant execute task, execute managed task on account to role dashboard_admin with grant option;
grant role dashboard_viewer to role dashboard_admin;

-- ensure a warehouse is usable by consumer
grant usage on warehouse dashboard_wh to role dashboard_admin;
grant usage on warehouse dashboard_wh to role dashboard_viewer;

-- grant access to a secondary role
-- use role dashboard_admin;
-- use warehouse dashboard_wh;

-- allow a secondary viewer role restricted access to the app
-- grant application role dashboard_app.app_viewer
    -- to role dashboard_viewer;