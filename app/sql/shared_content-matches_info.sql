-- View for the matches_info table
create or replace view shared_content.matches_info
    as select * from package_shared.matches_info;