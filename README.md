# Vietnam National Team Data App

## Intro
You are not having deja vu, no. This is a fork of the original [vietnamdataapp](https://github.com/daryl-g/vietnamdataapp) repo that I made for version 1.0 of the Vietnam NT Data Dashboard. This version (2.0), however, is integrated into Snowflake with its Streamlit integration to simulate a workflow that goes from raw JSON data files to a complete, full-fetched Streamlit dashboard.

This guide will attempt to walk you through the files that are contained in this repo. For the guide on how to use the app, I have made a small section called 'User guide' on the homepage of the app. But I will rewrite an extended version of that section once the app is put to sleep either by Streamlit or by me.

![Capture](https://user-images.githubusercontent.com/63649138/183244933-df54022e-4ea2-4d75-8c86-11d76304e2c2.PNG)

## Folders
-data: The backbone of the app, which is also the folder that contains all the data of Vietnam's 2022 World Cup Asian Qualifiers and AFF Cup 2020 campaigns (with an addition of Vietnam U23's data from the U23 Asian Cup 2022).

-pages: This is the folder that contains the Python codes that run each 'Data page' of the app.

## Files
-MultiPage.py: Originally the code of Prakhar Rathi (https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030), the code in this file allows the app to run with the multipage functionality.

-config.toml: Set the dark theme as the default for the app (though this is done within the Streamlit Cloud menu, but I am and have used this for another app).

-landing_page.py: The code for the main page of the app, which imports other Python files from the pages folder to create the multipage app.

-requirements.txt: All of the Python libs that I used to create the app

## Notes
-Neither the data nor the vizzes for Vietnam U23's Asian Cup campaign are present in the app, but they are in the folder because I find the data relevant to this repo and I would be really appreciated if someone could find a better use for such data (and the data of other competitions) than my usage for it (I initially had a plan to write a short article to analyse Vietnam U23's performance after their elimination but did not have the time and commitment to do it).
