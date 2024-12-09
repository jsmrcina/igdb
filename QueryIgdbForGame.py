import inquirer

from datetime import datetime, timezone
from twitch_token import twitch_token
from igdb_api import igdb_api
from PIL import Image
from io import BytesIO


# Utility
def chooseGameDict(gameOptions):
    choices = []
    for game in gameOptions:
        choices.append(game["name"])

    questions = [
        inquirer.List(
            'game',
            message =
            "More than one game matches your string, which one do you want to query?",
            choices = choices,
            carousel = True)
    ]

    answer = inquirer.prompt(questions)["game"]
    output = [x for x in gameOptions if x["name"] == answer]
    return output


def printSection(sectionName, sectionList):
    print(f"{sectionName}: ", end = "")
    print(', '.join(sectionList))


def main():
    # Query an access token using our secret. The access token will be written to disk
    # including an expiration time. The twitch_token class will take care of re-queries
    # any time it queryTwitchAccessTokenFromFile is called. We don't worry about expiration
    # during our execution since it's short lived.
    token = twitch_token()
    token.queryTwitchAccessTokenFromFile()

    # Create the igdb API class. This uses the token and secret files from above
    api = igdb_api()

    gameName = input("Type game name: ")
    gameResults = api.queryGameByCaseInsensitiveName(
        gameName).json()

    if len(gameResults) == 1:
        selectedGame = gameResults[0]
    else:
        gameResults = api.queryGameByCaseInsensitiveSubstringOfName(
            gameName).json()

        # If more than 1 game matches, let the user choose
        if len(gameResults) == 0:
            print("Failed to find game by name.")
            exit(1)
        if len(gameResults) == 1:
            selectedGame = gameResults[0]
        else:
            selectedGame = chooseGameDict(gameResults)[0]

    # Title
    printSection("Title", [selectedGame["name"]])

    # Release Date
    release_date = [
        datetime.fromtimestamp(
            selectedGame["first_release_date"], timezone.utc).strftime('%b %d, %Y')
    ]
    printSection("Release Date", release_date)

    # Image
    i = Image.open(BytesIO(api.queryCoverByGameId(selectedGame["id"])))
    i.save(gameName + ".png", bitmap_format = "png")

    # Genres
    genres = []
    for genre in selectedGame["genres"]:
        genres.append(api.queryGenre(genre).json()[0]["name"])
    printSection("Genres", genres)

    # Platforms
    platforms = []
    for platform in selectedGame["platforms"]:
        platforms.append(api.queryPlatform(platform).json()[0]["name"])
    printSection("Platforms", platforms)

    # Multiplayer Modes
    if "multiplayer_modes" in selectedGame:
        for mpMode in selectedGame["multiplayer_modes"]:
            mpModeResponse = api.queryMultiplayerMode(mpMode).json()[0]

            campaigncoop = mpModeResponse["campaigncoop"]
            lancoop = mpModeResponse["lancoop"]
            offlinecoop = mpModeResponse["offlinecoop"]
            onlinecoop = mpModeResponse["onlinecoop"]
            splitscreen = mpModeResponse["splitscreen"]

            multiplayer_modes = ["Single Player"]
            if campaigncoop or lancoop or offlinecoop or onlinecoop or splitscreen:
                multiplayer_modes.append("Co-op")
                multiplayer_modes.append("Multiplayer")

            printSection("Online", multiplayer_modes)

    # Developers
    developers = []
    developerResponse = api.queryDevelopersByGameId(selectedGame["id"])
    for developer in developerResponse.json():
        developers.append(developer["name"])
    printSection("Developers", developers)

    # Publishers
    publishers = []
    publisherResponse = api.queryPublishersByGameId(selectedGame["id"])
    for publisher in publisherResponse.json():
        publishers.append(publisher["name"])
    printSection("Publishers", publishers)


# Main
if __name__ == "__main__":
    main()