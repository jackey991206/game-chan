import discord
import json, asyncio
from core.classes import Cog_Extension
import pymongo
import os
import datetime
import random

#read setting.json
with open('./setting.json', 'r', encoding = 'utf8') as jfile1:
	  jdata1 = json.load(jfile1)

cluster = pymongo.MongoClient(os.environ['DBCONNECT'])
db = cluster["checkmatevotingdb"]
gamblers = db["gamblers"]

hours_added = datetime.timedelta(hours = 8)

class Rook(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def interval():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                guild = self.bot.get_guild(jdata1['GUILD'])
                # with open('./data.json', 'r', encoding = 'utf8') as jfile2:
	              #     jdata2 = json.load(jfile2)
                channel = guild.get_channel(897093322399711243)
                msg1 = await channel.fetch_message(897096804892565535)
                msg2 = await channel.fetch_message(897096807199412266)
                now = datetime.datetime.now()+hours_added
                now_minutes = int(now.strftime("%M"))
                now_hours = int(now.strftime("%H"))
                if now_minutes == 0:
                    with open('./data.json', 'r', encoding = 'utf8') as jfile2:
                        jdata2 = json.load(jfile2)
                    if now_hours in jdata2['time']:
                        farthest = random.randint(10, jdata2['range'])
                        medium = random.randint(10, farthest)
                        nearest = random.randint(10, medium)
                        with open('./guessgap.json', 'r', encoding = 'utf8') as jfile3:
                            jdata3 = json.load(jfile3)
                            jdata3['farthest'] = farthest
                            jdata3['medium'] = medium
                            jdata3['nearest'] = nearest
                        with open('./guessgap.json', 'w', encoding = 'utf8') as jfile3:
                            json.dump(jdata3, jfile3)
                    ranking = gamblers.find().sort('values', -1).limit(10)
                    embed = discord.Embed(title="賭神榜", color=0x66ffff, timestamp=datetime.datetime.now())
                    i = 0
                    for r in ranking:
                        try:
                            i += 1
                            temp = await guild.fetch_member(r['_uid'])
                            embed.add_field(name=f"榜{i}", value=f"{temp.mention} 總計在賭場裡贏了 `{r['values']}PT`", inline=False)
                            if i == 1:
                                embed.set_thumbnail(url=temp.avatar_url)
                        except:
                            i -= 1
                    await msg1.edit(embed=embed)
                    ranking = gamblers.find().sort('values', 1).limit(10)
                    embed = discord.Embed(title="非洲榜", color=0x66ffff, timestamp=datetime.datetime.now())
                    i = 0
                    for r in ranking:
                        try:
                            i += 1
                            temp = await guild.fetch_member(r['_uid'])
                            embed.add_field(name=f"榜{i}", value=f"{temp.mention} 總計在賭場裡贏了 `{r['values']}PT`", inline=False)
                            if i == 1:
                                embed.set_thumbnail(url=temp.avatar_url)
                        except:
                            i -= 1
                    await msg2.edit(embed=embed)
                await asyncio.sleep(60)
        self.bg_task = self.bot.loop.create_task(interval())

def setup(bot):
    bot.add_cog(Rook(bot))