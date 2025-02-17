-- View for the contestants table
create or replace view shared_content.contestants_view
    as select * from package_shared.contestants_view;