# General
This repository contains scripts used to query data from IGDB (Internet Games Database) for use in tracking my games played each year.

# Output

Output looks like below, and running the script will also download the cover image to the current directory as a png.

```ps
PS I:\Documents\Git\igdb> python .\QueryIgdbForGame.py
Token expiration time is 2024-03-15 15:06:05.224357
Existing token valid, skipping query. To force a refresh, delete token.json
Type game name: Satisfactory
[?] More than one game matches your string, which one do you want to query?: Satisfactory
   Satisfactory: Update 5
   Satisfactory: Update 6
   Satisfactory: Update 1
   Satisfactory: Update 2
   Satisfactory: Update 7
   Satisfactory: Update 3
   Satisfactory: Update 4
   Satisfactory: Update 8
 > Satisfactory

Title: Satisfactory
Release Date: Mar 19, 2019
Genres: Simulator, Strategy, Adventure, Indie
Platforms: PC (Microsoft Windows)
Online: Single Player, Co-op, Multiplayer
Developers: Coffee Stain Studios
Publishers: Coffee Stain Studios
```