#!/usr/bin/env python3
import os
import re
from plexapi.server import PlexServer

# --- Configuration ---
PLEX_URL = 'http://localhost:32400'           # Update if your Plex server is on a different host/port
PLEX_TOKEN = 'aypiCtP6JnKHp3397Px4'             # Replace with your Plex token
LIBRARY_NAME = 'TV Shows'                    # Name of your Plex library
SHOW_NAME = 'Dilbert'
SEASON_NUMBER = 1

# --- Connect to Plex ---
plex = PlexServer(PLEX_URL, PLEX_TOKEN)
library = plex.library.section(LIBRARY_NAME)
tv_show = plex.library.section(LIBRARY_NAME).get(SHOW_NAME)
season = tv_show.season(SEASON_NUMBER)
episodes = season.episodes()

# --- Define a Regex Pattern ---
# This example assumes filenames like: "Show Name - S01E01 - Episode Title.mkv"
# Adjust the regex if your naming differs.
# pattern = re.compile(r".* - S\d+E\d+ - (.+)\.[^.]+$")

# --- Process Each Episode ---
for episode in episodes:
    try:
        # Retrieve the file path from the episode media information
        # file_path = episode.media[0].parts[0].file
        # file_name = os.path.basename(file_path)
        print(f"Title: {episode.title}, Season: {episode.seasonNumber}, Episode: {episode.episodeNumber}")
    except Exception as e:
        print(f"Could not retrieve file name for episode '{episode.title}': {e}")
        continue

    # print("Path: " + file_path)
    # print("File Name: " + file_name)

    # # Try to extract the episode title from the filename
    # match = pattern.match(file_name)
    # if match:
    #     new_title = match.group(1).strip()
    #     print("New Title: " + new_title)
    #     print("")
    #     if new_title != episode.title:
    #         print(f"Updating episode title for '{episode.title}' to '{new_title}'")
    #         try:
    #             # Update the episode's title on Plex.
    #             # Note: Your Plex server must allow metadata editing for this to work.
    #             episode.edit(title=new_title)
    #             print("Update successful.")
    #         except Exception as e:
    #             print(f"Error updating episode '{episode.title}': {e}")
    #     else:
    #         print(f"Episode '{episode.title}' already has the expected title.")
    # else:
    #     print(f"Filename '{file_name}' does not match the expected pattern. Skipping.")
