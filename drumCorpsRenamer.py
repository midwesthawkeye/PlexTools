#!/usr/bin/env python3
import os
import re
from plexapi.server import PlexServer

# This program will attempt to rename episodes of a show using the metadata stored in the filename.
# Files should be stroed in the following manner:
# Top Level Folder is the Library (of type TV Show within Plex) -- (Drum Corps)
# Subfolder to process is the Show Name.  (DCI Finals)
# Subfolders within the Show Name folder are the seasons.  (1974, 1975, etc.)
# 
# Sample media file name (the pattern matcher evaluates this):
# S1984E015 - Colts.mp4

def get_directory_names(path):
    """
    Returns a list of directory names that reside at the given path.
    Used to come up with a list of the Seasons folders here.
    """
    directory_names = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directory_names.append(item)
    return directory_names

def scrub_title_finals(origStr):
    workStr = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', origStr)
    workStr = re.sub(r'_', '', workStr)
    workStr = re.sub(r'USMC', 'USMC ', workStr)
    workStr = re.sub(r"^[^\w]", '', workStr)
    return workStr.strip()

def scrub_title_semis(origStr):
    workStr = re.sub(r'MULTI - ', '', origStr)
    workStr = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', workStr)
    workStr = re.sub(r'_', '', workStr)
    return workStr.strip()

# --- Configuration ---
PLEX_URL = 'http://localhost:32400'           # Update if your Plex server is on a different host/port
PLEX_TOKEN = 'aypiCtP6JnKHp3397Px4'             # Replace with your Plex token
LIBRARY_NAME = 'Drum Corps'                    # Name of your Plex library
FINALS_NAME = 'DCI Finals'
SEMIS_NAME = 'DCI Semi Finals'
SHOW_NAME = SEMIS_NAME
FINALS_HOME = '/media/devmon/Samsung/Drum Corps/DCI Finals'
SEMIS_HOME = '/media/devmon/Samsung/Drum Corps/DCI Semi Finals'
LIBRARY_HOME = ''

if (SHOW_NAME == FINALS_NAME):
    LIBRARY_HOME = FINALS_HOME
elif (SHOW_NAME == SEMIS_NAME):
    LIBRARY_HOME = SEMIS_HOME
else:
    print("SHOW_NAME not properly defined.  Exitting...")
    quit()

# --- Connect to Plex ---
plex = PlexServer(PLEX_URL, PLEX_TOKEN)
library = plex.library.section(LIBRARY_NAME)
tv_show = plex.library.section(LIBRARY_NAME).get(SHOW_NAME)

seasons = get_directory_names(LIBRARY_HOME)

for SEASON_STRING in seasons:
    # In this case, I happen to know that each directory name is an integer (a Year number)
    # so I am forcing the directory name to be interpreted as an integer here since Plex
    # is expecting an integer for a season number.
    SEASON_NUMBER = int(SEASON_STRING)
    season = tv_show.season(SEASON_NUMBER)
    episodes = season.episodes()

    # --- Define a Regex Pattern ---
    # This example assumes filenames like: "S01E01 - Episode Title.mkv"
    # Adjust the regex if your naming differs.
    pattern = re.compile(r"S\d+E\d+ - (.+)\.[^.]+$")

    # --- So for each episode in a particular year ---
    for episode in episodes:
        try:
            # Retrieve the file path from the current episode's media information
            file_path = episode.media[0].parts[0].file
            # Isolate just the base file name
            file_name = os.path.basename(file_path)
        except Exception as e:
            print(f"Could not retrieve file name for episode '{episode.title}': {e}")
            continue

        print("Path: " + file_path)
        print("File Name: " + file_name)

        if (SHOW_NAME == SEMIS_NAME):
            file_name = re.sub(r'_', ' - ', file_name)

        # # Try to extract the episode title from the filename
        match = pattern.match(file_name)
        if match:
            new_title = match.group(1).strip()

            if (SHOW_NAME == FINALS_NAME):
                new_title = scrub_title_finals(new_title)
            elif (SHOW_NAME == SEMIS_NAME):
                new_title = scrub_title_semis(new_title)

            new_title = new_title.lstrip()

            print("New Title: " + new_title)
            # If the new title is not the same as the current episode name
            if new_title != episode.title:
                print(f"Updating episode title for '{episode.title}' to '{new_title}'")
                try:
                    # Update the episode's title on Plex.
                    # Note: Your Plex server must allow metadata editing for this to work.
                    # I am not sure WHY this magical syntax does the job, but it does.
                    episode.edit(**{"title.value":new_title})
                    print("Update of title was successful.")
                except Exception as e:
                    print(f"Error updating episode '{episode.title}': {e}")
            else:
                print(f"Episode '{episode.title}' already has the expected title.")
        else:
            print(f"Filename '{file_name}' does not match the expected pattern. Skipping.")

        print("")
