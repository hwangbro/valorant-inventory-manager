import asyncio, traceback, json, logging

from ..randomizers.skin_randomizer import Skin_Randomizer
from ..randomizers.buddy_randomizer import Buddy_Randomizer
from ..sys_utilities import system
from ..broadcast import broadcast

from ..client_config import CLIENT_STATE_REFRESH_INTERVAL
from .. import shared

logger = logging.getLogger("VIM_main")


class Client_State:

    def __init__(self):
        self.reset()

    def reset(self):
        self.client = shared.client
        self.valclient = shared.client.client

        try:
            self.previous_presence = self.valclient.fetch_presence()
        except:
            self.previous_presence = {}
        self.presence = self.previous_presence
        shared.ingame = False
        self.inrange = False

    async def dispatch_randomizer(self, type):
        logger.debug("randomizing")
        print("randomizing")
        if type == "skins":
            await Skin_Randomizer.randomize()
        elif type == "buddies":
            await Buddy_Randomizer.randomize()

    async def randomizer_check(self):
        if self.presence is not None and self.presence != {}:
            cur_state = self.presence["sessionLoopState"]
            old_state = self.previous_presence["sessionLoopState"]
            if old_state == "INGAME" and cur_state == "MENUS":
                if shared.config["skin_randomizer"]["settings"]["auto_skin_randomize"][
                    "value"
                ]:
                    if self.inrange:
                        if shared.config["skin_randomizer"]["settings"][
                            "randomize_after_range"
                        ]["value"]:
                            print("dispatching randomizer: skins in range")
                            await self.dispatch_randomizer("skins")
                            self.inrange = False
                        else:
                            self.inrange = False
                            return
                    else:
                        print("dispatching randomizer: skins")
                        await self.dispatch_randomizer("skins")

                if shared.config["skin_randomizer"]["settings"]["auto_skin_randomize"][
                    "value"
                ]:
                    await self.dispatch_randomizer("buddies")

    async def check_presence(self):
        self.previous_presence = self.presence
        changed = False
        try:
            self.presence = self.valclient.fetch_presence()
            cur_state = self.presence["sessionLoopState"]
            old_state = self.previous_presence["sessionLoopState"]
            if cur_state in ("PREGAME", "INGAME"):
                shared.ingame = True
            else:
                shared.ingame = False
            changed = cur_state != old_state

            if self.presence["provisioningFlow"] == "ShootingRange":
                self.inrange = True

        except:
            self.reset()
            shared.ingame = False

        return changed

    async def check_game_running(self):
        await shared.client.check_connection()

    async def loop(self):
        while True:
            if self.client.ready:
                changed = await self.check_presence()
                await self.check_game_running()

                # check for randomizer
                await self.randomizer_check()

                if changed:  # only need to broadcast this if the state actually changed
                    await Client_State.update_game_state()

            else:
                await self.check_game_running()

            await asyncio.sleep(CLIENT_STATE_REFRESH_INTERVAL)

    async def update_game_state():
        payload = {"event": "game_state", "data": {"state": shared.ingame}}
        await broadcast(payload)
        return True
