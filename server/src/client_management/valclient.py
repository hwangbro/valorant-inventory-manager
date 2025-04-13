from . import auth

import json
import requests
import urllib3
import base64


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ValClient:
    def __init__(self, region: str = "na"):
        self.player_name: str = ""
        self.player_tag: str = ""
        lock_file_data = auth.parse_lockfile()
        self.local_port: int = int(lock_file_data["port"])
        self.password: str = lock_file_data["password"]
        self.puuid, self.headers, self.local_headers = auth.get_auth_headers(
            self.local_port, self.password
        )
        self.shard: str = region
        self.region: str = region

        self.base_url = f"https://pd.{self.shard}.a.pvp.net"
        self.base_url_glz = f"https://glz-{self.region}-1.{self.shard}.a.pvp.net"
        self.base_url_shared = f"https://shared.{self.shard}.a.pvp.net"
        self.local_url = f"https://127.0.0.1:{self.local_port}"

    def _verify_status_code(self, status_code, exceptions={}):
        if status_code in exceptions:
            response_exception = exceptions[status_code]
            raise response_exception[0](response_exception[1])

    def call(
        self,
        call_type: str,
        endpoint: str = "/",
        endpoint_type: str = "pd",
        json_data=None,
        exceptions={},
    ) -> dict:
        data = None
        response = None
        match call_type:
            case "get":
                func = requests.get
            case "put":
                func = requests.put
            case "post":
                func = requests.post
            case _:
                func = None
        if func is None:
            raise Exception(f"invalid call_type {call_type}")

        call_args = {}
        if json_data is not None:
            call_args["data"] = json.dumps(json_data)

        if endpoint_type in ("pd", "glz", "shared"):
            url = {
                "pd": self.base_url,
                "glz": self.base_url_glz,
                "shared": self.base_url_shared,
            }
            call_args["url"] = f"{url[endpoint_type]}{endpoint}"
            call_args["headers"] = self.headers
        elif endpoint_type == "local":
            call_args["url"] = f"{self.local_url}{endpoint}"
            call_args["headers"] = self.local_headers
            call_args["verify"] = False

        response = requests.request(call_type, **call_args)

        if response is None:
            raise Exception("Response is None")

        self._verify_status_code(response.status_code, exceptions)

        try:
            data = json.loads(response.text)
        except:
            pass

        if data is None:
            raise Exception("Request returned NoneType")

        if "httpStatus" not in data:
            return data

        if data["httpStatus"] == 400:
            # if headers expire, refresh
            self.puuid, self.headers, self.local_headers = auth.get_auth_headers(
                self.local_port, self.password
            )
            return self.call(
                call_type=call_type, endpoint=endpoint, endpoint_type=endpoint_type
            )
        return {}

    # PVP endpoints
    def fetch_player_loadout(self):
        data = self.call(
            "get",
            # endpoint=f"/personalization/v2/players/{self.puuid}/playerloadout",
            endpoint=f"/personalization/v3/players/{self.puuid}/playerloadout",
            endpoint_type="pd",
        )
        return data

    def put_player_loadout(self, loadout):
        data = self.call(
            "put",
            endpoint=f"/personalization/v3/players/{self.puuid}/playerloadout",
            endpoint_type="pd",
            json_data=loadout,
        )
        return data

    def fetch_mmr(self, puuid=None):
        """
        MMR_FetchPlayer
        Get the match making rating for a player
        """
        puuid = self._check_puuid(puuid)
        return self.call(
            call_type="get", endpoint=f"/mmr/v1/players/{puuid}", endpoint_type="pd"
        )

    def store_fetch_entitlements(
        self, item_type: str = "e7c63390-eda7-46e0-bb7a-a6abdacd2433"
    ):
        """
        Store_GetEntitlements
        List what the layer owns (agents, skins, buddies, etc)
        Correlate with UUIDs in client.fetch_content() to know what items are owned

        NOTE: uuid to item type
        "e7c63390-eda7-46e0-bb7a-a6abdacd2433": "skin_level",
        "3ad1b2b2-acdb-4524-852f-954a76ddae0a": "skin_chroma",
        "01bb38e1-da47-4e6a-9b3d-945fe4655707": "agent",
        "f85cb6f7-33e5-4dc8-b609-ec7212301948": "contract_definition",
        "dd3bf334-87f3-40bd-b043-682a57a8dc3a": "buddy",
        "d5f120f8-ff8c-4aac-92ea-f2b5acbe9475": "spray",
        "3f296c07-64c3-494c-923b-fe692a4fa1bd": "player_card",
        "de7caa6b-adf7-4588-bbd1-143831e786c6": "player_title",
        """
        return self.call(
            call_type="get",
            endpoint=f"/store/v1/entitlements/{self.puuid}/{item_type}",
            endpoint_type="pd",
        )

    # party endpoints
    def party_fetch_player(self):
        """
        Party_FetchPlayer
        Get the Party ID that a given player belongs to
        """
        return self.call(
            call_type="get",
            endpoint=f"/parties/v1/players/{self.puuid}",
            endpoint_type="glz",
        )

    # live game endpoints
    # pregame endpoints
    def pregame_fetch_player(self):
        """
        Pregame_GetPlayer
        Get the ID of a game in the pre-game stage
        """
        return self.call(
            call_type="get",
            endpoint=f"/pregame/v1/players/{self.puuid}",
            endpoint_type="glz",
            exceptions={404: [PhaseError, "You are not in a pre-game"]},
        )

    # local riotclient endpoints
    def fetch_presence(self, puuid=None):
        """
        PRESENCE_RNet_GET
        Note: only works on self or active user''
        """
        puuid = self._check_puuid(puuid)
        data = self.call(
            call_type="get",
            endpoint="/chat/v4/presences",
            endpoint_type="local",
            exceptions={},
        )
        try:
            for presence in data["presences"]:
                if presence["puuid"] == puuid:
                    return json.loads(base64.b64decode(presence["private"]))
        except:
            return None

    def riotclient_session_fetch_sessions(self):
        """
        RiotClientSession_FetchSessions
        Gets info about the running Valorant process including start arguments
        """
        return self.call(
            call_type="get",
            endpoint="/product-session/v1/external-sessions",
            endpoint_type="local",
        )

    # local utility functions
    def _get_live_season(self) -> str:
        """Get the UUID of the live competitive season"""
        return self.fetch_mmr()["LatestCompetitiveUpdate"]["SeasonID"]

    def _check_puuid(self, puuid) -> str:
        """If puuid passed in is none, use player's puuid instead"""
        return self.puuid if puuid is None else puuid

    def _check_party_id(self, party_id) -> str:
        pass

    def _get_current_party_id(self) -> str:
        party = self.party_fetch_player()
        return party["CurrentPartyID"]

    def _pregame_check_match_id(self, match_id) -> str:
        return self.pregame_fetch_player()["MatchID"] if match_id is None else match_id

    def _check_queue_type(self, queue_id) -> None:
        if queue_id not in (
            "competitive",
            "custom",
            "deathmatch",
            "ggteam",
            "snowball",
            "spikerush",
            "unrated",
            "onefa",
            "null",
        ):
            raise ValueError("Invalid queue type")


class HandshakeError(Exception):
    """
    Raised whenever there's a problem while attempting to communicate with the local Riot server.
    """

    pass


class LockfileError(Exception):
    """
    Raised whenever there's a problem while attempting to fetch the Riot lockfile.
    """

    pass


class ResponseError(Exception):
    """
    Raised whenever an empty response is given by the Riot server.
    """

    pass


class PhaseError(Exception):
    """
    Raised whenever there's a problem while attempting to fetch phase data.
    This typically occurs when the phase is null (i.e. player is not in the agent select phase.)
    """

    pass


if __name__ == "__main__":
    c = ValClient()
    # print(c.fetch_player_loadout())
