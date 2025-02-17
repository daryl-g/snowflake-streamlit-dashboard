-- landing page tab: just a landing page
create or replace
    streamlit ui."Landing page"
    from 'dashboard' main_file='landing_page.py';

grant usage
    on streamlit ui."Landing page"
    to application role app_viewer;