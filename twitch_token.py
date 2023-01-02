import requests
import json
import os.path

from datetime import datetime, timedelta


class twitch_token:

    def __init__(self,
                 secret_file = "twitch_secret.json",
                 token_output_file = "token.json"):
        if os.path.isfile(secret_file) is False:
            raise FileNotFoundError(
                f"Secret file {secret_file} does not exist")

        self.secret_file = secret_file
        self.token_output_file = token_output_file

    def queryTwitchAccessToken(self, client_id, client_secret, grant_type):
        expired = False
        not_available = False
        invalid = False

        if os.path.isfile(self.token_output_file):
            with open(self.token_output_file, "r") as infile:
                token_json = json.loads(infile.read())

                if "expiry_time" in token_json:
                    expiry_time = datetime.fromisoformat(
                        token_json["expiry_time"])
                    print(f"Token expiration time is {expiry_time}")
                    if datetime.now() > expiry_time:
                        print("Token is expired")
                        expired = True
                    else:
                        print(
                            f"Existing token valid, skipping query. To force a refresh, delete {self.token_output_file}"
                        )
                else:
                    invalid = True
                    print("Expiration time is invalid, querying a new token.")
        else:
            print("Token not available")
            not_available = True

        if expired or not_available or invalid:
            requestUri = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}"
            response = requests.post(requestUri)
            if response.status_code == 200:
                # Add the expiry time
                response_json = response.json()
                now = datetime.now()
                expiry_time = now + timedelta(
                    seconds = response_json["expires_in"])
                response_json["expiry_time"] = expiry_time

                with open(self.token_output_file, "w") as outfile:
                    outfile.write(
                        json.dumps(response_json, indent = 4, default = str))
            else:
                print(f"Failed to query token, result: {response.status_code}")

    def queryTwitchAccessTokenFromFile(self):
        with open(self.secret_file, "r") as infile:
            twitch_secret_json = json.loads(infile.read())
            self.queryTwitchAccessToken(twitch_secret_json["client_id"],
                                        twitch_secret_json["client_secret"],
                                        twitch_secret_json["grant_type"])
