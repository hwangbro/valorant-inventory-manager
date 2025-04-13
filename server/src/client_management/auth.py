import requests
from pathlib import Path
import os
import base64


_CLIENT_PLATFORM = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"


def parse_lockfile() -> dict[str, str]:
    p = Path(
        os.getenv("LOCALAPPDATA", ""), "Riot Games", "Riot Client", "Config", "lockfile"
    )
    if not p.is_file():
        raise Exception("Lockfile not found. Is Valorant running?")

    with open(p) as lf:
        data = lf.read().split(":")
        keys = ("name", "PID", "port", "password", "protocol")
        return dict(zip(keys, data))


def _get_current_version() -> str:
    data = requests.get("https://valorant-api.com/v1/version")
    data = data.json()["data"]
    return f"{data['branch']}-shipping-{data['buildVersion']}-{data['version'].split('.')[3]}"


def get_auth_headers(
    port: int, password: str
) -> tuple[str, dict[str, str], dict[str, str]]:
    token = base64.b64encode(f"riot:{password}".encode()).decode()

    # headers for pd/glz endpoints
    local_headers = {"Authorization": f"Basic {token}"}
    uri = f"https://127.0.0.1:{port}/entitlements/v1/token"

    response = requests.get(
        uri,
        headers=local_headers,
        verify=False,
    )
    entitlements = response.json()
    puuid = entitlements["subject"]
    headers = {
        "Authorization": f"Bearer {entitlements['accessToken']}",
        "X-Riot-Entitlements-JWT": entitlements["token"],
        "X-Riot-ClientPlatform": _CLIENT_PLATFORM,
        "X-Riot-ClientVersion": _get_current_version(),
    }

    return puuid, headers, local_headers
