-- player - all matches tab: player's stats from all matches
create or replace
    streamlit ui."Player - All matches"
    from 'dashboard/pages' main_file='player_overall.py';

grant usage
    on streamlit ui."Player - All matches"
    to application role app_viewer;