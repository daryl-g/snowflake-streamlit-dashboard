-- View for the match_details table
create or replace view shared_content.match_details_view
    as select * from package_shared.match_details_view;