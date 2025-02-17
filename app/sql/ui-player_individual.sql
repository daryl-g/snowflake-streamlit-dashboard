-- player - individual match tab: player's stats from each individual match
create or replace
    streamlit ui."Player - Individual match"
    from 'dashboard/pages' main_file='player_individual.py';

grant usage
    on streamlit ui."Player - Individual match"
    to application role app_viewer;