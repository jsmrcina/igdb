import requests
import json
import os.path
import time


class igdb_api:

    def __init__(self,
                 secret_file = "twitch_secret.json",
                 token_file = "token.json"):
        if os.path.isfile(secret_file) is False:
            raise FileNotFoundError(
                f"Secret file {secret_file} does not exist")

        if os.path.isfile(token_file) is False:
            raise FileNotFoundError(f"Token file {token_file} does not exist")

        self.secret_file = secret_file
        self.token_file = token_file

    def queryIgdb(self, data, endpoint, delay = 0.3):
        if delay < 0.3 or delay > 100:
            print(
                "Invalid delay, any delay less than 0.3 will hit a rate limit and more than 100s is unsupported"
            )
            return None

        baseUri = "https://api.igdb.com/v4/"
        uri = baseUri + endpoint

        with open(self.secret_file, "r") as secret_file:
            with open(self.token_file, "r") as token_file:
                twitch_secret = json.loads(secret_file.read())
                twitch_token = json.loads(token_file.read())
                access_token = twitch_token["access_token"]
                headers = {
                    "Client-ID": twitch_secret["client_id"],
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "text/plain"
                }

        response = requests.post(uri, data = data, headers = headers)
        time.sleep(delay)
        return response

    def queryGameById(self, id):
        data = f'fields *; where id = {id};'
        return self.queryIgdb(data, "games")

    def queryGameByCaseSensitiveName(self, name):
        data = f'fields *; where name = "{name}";'
        return self.queryIgdb(data, "games")

    def queryGameByCaseInsensitiveName(self, name):
        data = f'fields *; where name ~ "{name}";'
        return self.queryIgdb(data, "games")

    def queryGameByCaseInsensitiveSubstringOfName(self, name):
        data = f'fields *; where name ~ *"{name}"*;'
        return self.queryIgdb(data, "games")

    def queryGenre(self, genre):
        data = f"fields *; where id = {genre};"
        return self.queryIgdb(data, "genres")

    def queryPlatform(self, platform):
        data = f"fields *; where id = {platform};"
        return self.queryIgdb(data, "platforms")

    def queryMultiplayerMode(self, mpMode):
        data = f"fields *; where id = {mpMode};"
        return self.queryIgdb(data, "multiplayer_modes")

    def queryDevelopersByGameId(self, game):
        data = f"fields *; where developed = ({game});"
        return self.queryIgdb(data, "companies")

    def queryPublishersByGameId(self, game):
        data = f"fields *; where published = ({game});"
        return self.queryIgdb(data, "companies")

    def queryCoverByGameId(self, game, type = "1080p"):
        data = f"fields *; where game = ({game});"
        coverResponse = self.queryIgdb(data, "covers")
        image = coverResponse.json()[0]["url"].replace("thumb", type)[2:]
        uri = f"https://{image}"
        return requests.get(uri).content