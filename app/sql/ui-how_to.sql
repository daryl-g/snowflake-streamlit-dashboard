-- how to tab: instructions on how to use the dashboard
create or replace
    streamlit ui."How to"
    from 'dashboard/pages' main_file='how_to.py';

grant usage
    on streamlit ui."How to"
    to application role app_viewer;