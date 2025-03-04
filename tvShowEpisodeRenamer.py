#!/usr/bin/env python3
import os
import re
from plexapi.server import PlexServer


def get_directory_names(path):
    """
    Returns a list of directory names in the given path.
    """
    directory_names = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directory_names.append(item)
    return directory_names

# --- Configuration ---
PLEX_URL = 'http://localhost:32400'           # Update if your Plex server is on a different host/port
PLEX_TOKEN = 'aypiCtP6JnKHp3397Px4'             # Replace with your Plex token
LIBRARY_NAME = 'Drum Corps'                    # Name of your Plex library
SHOW_NAME = 'DCI Finals'
#SEASON_NUMBER = 1970

# --- Connect to Plex ---
plex = PlexServer(PLEX_URL, PLEX_TOKEN)
library = plex.library.section(LIBRARY_NAME)
tv_show = plex.library.section(LIBRARY_NAME).get(SHOW_NAME)

seasons = get_directory_names('/media/devmon/Samsung/Drum Corps/DCI Finals')

for SEASON_STRING in seasons:
    SEASON_NUMBER= int(SEASON_STRING)
    season = tv_show.season(SEASON_NUMBER)
    episodes = season.episodes()

    # --- Define a Regex Pattern ---
    # This example assumes filenames like: "Show Name - S01E01 - Episode Title.mkv"
    # Adjust the regex if your naming differs.
    pattern = re.compile(r"S\d+E\d+ - (.+)\.[^.]+$")

    # --- Process Each Episode ---
    for episode in episodes:
        try:
            # Retrieve the file path from the episode media information
            file_path = episode.media[0].parts[0].file
            file_name = os.path.basename(file_path)
            # print(f"Title: {episode.title}, Season: {episode.seasonNumber}, Episode: {episode.episodeNumber}")
        except Exception as e:
            print(f"Could not retrieve file name for episode '{episode.title}': {e}")
            continue

        print("Path: " + file_path)
        print("File Name: " + file_name)

        # # Try to extract the episode title from the filename
        match = pattern.match(file_name)
        if match:
            new_title = match.group(1).strip()
            print("New Title: " + new_title)
            print("")
            if new_title != episode.title:
                print(f"Updating episode title for '{episode.title}' to '{new_title}'")
                try:
                    # Update the episode's title on Plex.
                    # Note: Your Plex server must allow metadata editing for this to work.
                    episode.edit(**{"title.value":new_title})
                    episode.refresh
                    print("Updated Title: " + episode.title)
                    print("Update successful.")
                except Exception as e:
                    print(f"Error updating episode '{episode.title}': {e}")
            else:
                print(f"Episode '{episode.title}' already has the expected title.")
        else:
            print(f"Filename '{file_name}' does not match the expected pattern. Skipping.")
