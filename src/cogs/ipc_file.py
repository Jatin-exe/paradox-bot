import discord 
from discord.ext import commands, ipc
from pymongo import MongoClient
from core import get_prefix
from discord.ext.commands.cooldowns import BucketType

from dotenv import dotenv_values
VALUES = dotenv_values("paradox-bot/venv/.env")
cluster = MongoClient(VALUES["DB_URI"])

db = cluster["paradox"]
g_configs = db["guild_configs"]



class ipc_file(commands.Cog):
    """Change the Configuration of the bot"""
    def __init__(self, client):
        self.client = client

#GIT_CHECK





    @ipc.server.route()
    async def get_guild_ids(self, data):
        final = []
        for guild in self.client.guilds:
            final.append(guild.id)
        return final






    @ipc.server.route()
    async def get_guild_channels(self, data):
        guild = self.client.get_guild(int(data.guild_id))
        guild_ch = []
        for x in guild.by_category():
            ids = []
            for ch in x[1]: 
                ids.append((ch.name, str(ch.id)))
            if x[0] is not None:
                guild_ch.append(((x[0].name, str(x[0].id)), ids))
            else:
                guild_ch.append((("UnCategorized", 0), ids))
        return guild_ch


    """ON GULD JOIN
                        level_reward = [
                        (10, "725738661676711986", {}),
                        (20, "725738798654423101", {}),
                        (30, "726005744905879562", {}),
                        (40, "726005945716703245", {}),   
                        (50, "817383614357438504", {})
                    ]
    """

    @ipc.server.route()
    async def get_guild_roles(self, data):
        guild = self.client.get_guild(int(data.guild_id))
        guild_roles = []
        for role in guild.roles:
            if role.id != data.guild_id:
                guild_roles.append((role.name, str(role.id)))
        return guild_roles

    @ipc.server.route()        
    async def update_guild_configs(self,data):
        #sync with leveling.py
        #SYNC MOST IMPORTANT
        #logging
        guild_id = data.guild_id
        module = data.module
        data = data.data
        print("Updating Db")
        print(data, guild_id, module)
        if isinstance(data, dict):

            if module == 'leveling':
                data = data["leveling"]
                no_xp_channels = data['no_xp_channels'] 
                no_xp_roles = data['no_xp_roles']
                xp_rate = data["xp_rate"]
                action_on_level_up = data.get("action_on_level_up") #tuple -> (level_the_action_should_trigger, reward_on_level_milestone, action..ie:dm user , send msg in channel) 
                level_reward = data.get("level_reward")
                leveling_enabled = data.get("leveling_enabled") or "off"
                len_levels = data['len_levels']
                



                db = cluster["paradox"]
                g_configs = db["guild_configs"]

                old_configs = g_configs.find_one({"_id": guild_id})
                if old_configs is None:
                    payload = {
                        "_id": guild_id,
                        "prefix": ".",
                        "roles": {},
                        "channels": {},
                        "leveling": {"no_xp_channels": no_xp_channels,
                            "no_xp_roles":  no_xp_roles ,
                            "xp_rate": xp_rate, 
                            "action_on_level_up": action_on_level_up, 
                            "level_reward": level_reward,
                            "leveling_enabled": leveling_enabled,
                            "len_levels": len_levels 
                            },
                        "moderation": {},
                    }

                    g_configs.insert_one(payload)
                
                else:
                    old_configs["leveling"] = {
                            "no_xp_channels": no_xp_channels,
                            "no_xp_roles":  no_xp_roles ,
                            "xp_rate": xp_rate, 
                            "action_on_level_up": action_on_level_up, 
                            "level_reward": level_reward,
                            "leveling_enabled": leveling_enabled,
                            "len_levels": len_levels 
                            }

                    g_configs.replace_one({"_id": guild_id}, old_configs)

            else:
                print("module is not leveling")












    @ipc.server.route()
    async def get_guild_configs(self, data):
        """Checks the DB for any previous/default data for the Form"""
        print("Fetching DB")
        guild_id = data.guild_id


        db = cluster["paradox"]
        g_configs = db["guild_configs"]

        fetched_configs = g_configs.find_one({"_id": guild_id})
        print("Fetchedconfigs", fetched_configs)


        if fetched_configs is None:
            payload = {
                "_id": guild_id,
                "prefix": ".",
                "roles": {},
                "channels": {},
                "leveling": {"no_xp_channels": [],
                    "no_xp_roles":[] ,
                    "xp_rate": 1, 
                    "action_on_level_up": None, 
                    "level_reward": None,
                    "leveling_enabled": False,
                    "len_levels": 0
                    },
                "moderation": {},
            }

            g_configs.insert_one(payload)
            print("DB Date Created and Inserted")
            return payload
            
        else:
            print(fetched_configs)
            return fetched_configs
                






#----------------------------------------------------------------------
def setup(client):
  client.add_cog(ipc_file(client))



    #MANIPULATING LEVEL STATS
    #change xp and things