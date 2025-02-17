-- View for the contestants table
create or replace view shared_content.contestants
    as select * from package_shared.contestants;