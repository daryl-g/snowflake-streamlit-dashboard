-- create provider role
create role if not exists dashboard_provider;
grant role dashboard_provider to role accountadmin;
grant create application package on account to role dashboard_provider;
grant create database on account to role dashboard_provider;

-- ensure a warehouse is usable by provider
create warehouse if not exists dashboard_wh;
grant usage on warehouse dashboard_wh to role dashboard_provider;