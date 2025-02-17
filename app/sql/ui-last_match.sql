-- last match tab: data from the last match
create or replace
    streamlit ui."Last match"
    from 'dashboard/pages' main_file='matches_lastmatch.py';

grant usage
    on streamlit ui."Last match"
    to application role app_viewer;