import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import pymongo
import datetime
import random
import os
from numpy.random import choice
import asyncio

cluster = pymongo.MongoClient(os.environ['DBCONNECT'])
db = cluster["checkmatevotingdb"]
rpswinstreak = db["rpswinstreak"]
rpswinstreakre = db["rpswinstreakre"]
rpsre = db["rpsrecord"]
cfwinstreak = db["cfwinstreak"]
cfwinstreakre = db["cfwinstreakre"]
cfre = db["cfrecord"]
secondcluster = pymongo.MongoClient(os.environ['db_connect'])
db2 = secondcluster["MoneyData"]
cd = db2["ClientData"]

hours_added = datetime.timedelta(hours = 8)

class Game(Cog_Extension):

    #Rock Paper Scissors
    @commands.command()
    async def rps(self, ctx, memberchoice=None, num:int=None):
        with open('./data.json', 'r', encoding = 'utf8') as jfile2:
	          jdata2 = json.load(jfile2)
        if not ctx.channel.id in jdata2['gamecmdchannel']:
            await ctx.message.delete(delay=10)
            await ctx.send("請在指定頻道使用此指令", delete_after=10)
            return
        if not memberchoice:
            memberchoice = random.choice(["石頭", "剪刀", "布"])
        if not memberchoice == "石頭" and not memberchoice == "剪刀" and not memberchoice == "布":
            await ctx.message.delete(delay=10)
            await ctx.send("指令用法：^rps [石頭/剪刀/布]", delete_after=10)
            return
        # if not num:
        num = 1000
        if memberchoice == "石頭":
            botchoice = choice(["石頭", "剪刀", "布"], p=[0.3, 0.35, 0.35])
        if memberchoice == "剪刀":
            botchoice = choice(["石頭", "剪刀", "布"], p=[0.35, 0.3, 0.35])
        if memberchoice == "布":
            botchoice = choice(["石頭", "剪刀", "布"], p=[0.35, 0.35, 0.3])
        result = None
        if botchoice == memberchoice:
            result = "Tie"
        elif (botchoice == "石頭" and memberchoice == "剪刀") or (botchoice == "剪刀" and memberchoice == "布") or (botchoice == "布" and memberchoice == "石頭"):
            result = "Bot Win"
        elif (botchoice == "石頭" and memberchoice == "布") or (botchoice == "布" and memberchoice == "剪刀") or (botchoice == "剪刀" and memberchoice == "石頭"):
            result = "Member Win"
        if result == "Bot Win":
            if botchoice == "布":
                url = "https://raw.githubusercontent.com/jackey991206/saveimage/main/bot_paper_win_min-min.png"
            elif botchoice == "石頭":
                url = "https://raw.githubusercontent.com/jackey991206/saveimage/main/bot_rock_win_min-min.png"
            elif botchoice == "剪刀":
                url = "https://raw.githubusercontent.com/jackey991206/saveimage/main/bot_scissors_win_min-min.png"
        elif result == "Tie" or result == "Member Win":
            if botchoice == "布":
                url = "https://raw.githubusercontent.com/jackey991206/saveimage/main/bot_paper_tie_lose_min-min.png"
            elif botchoice == "石頭":
                url = "https://raw.githubusercontent.com/jackey991206/saveimage/main/bot_rock_tie_lose_min-min.png"
            elif botchoice == "剪刀":
                url = "https://raw.githubusercontent.com/jackey991206/saveimage/main/bot_scissors_tie_lose_min-min.png"
        embed = discord.Embed(title="猜拳遊戲", description=f"參與者：\n{ctx.author.mention}", color=0x6666ff,timestamp=datetime.datetime.now())
        if not ctx.author.nick == None:
            displayname = ctx.author.nick
        else:
            displayname = ctx.author.name
        if result == "Tie":
            displayresult = "平手"
        elif result == "Bot Win":
            displayresult = f"{self.bot.user.name}獲勝"
        elif result == "Member Win":
            displayresult = f"{displayname}獲勝"
        now_datetime = datetime.datetime.now()+hours_added
        rpsid = rpsre.find().count()+1
        rpsre.insert_one({
            "_rpsid": rpsid,
            "uid": ctx.author.id,
            "member_choice": memberchoice,
            "bot_choice": botchoice,
            "result": result,
            "at": now_datetime
        })
        embed.add_field(name=f"{displayname}出", value=f"`{memberchoice}`", inline=True)
        embed.add_field(name=f"{self.bot.user.name}出", value=f"`{botchoice}`", inline=True)
        embed.add_field(name="結果", value=f"`{displayresult}`", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url=url)
        if result == "Member Win":
            isexist = rpswinstreak.find_one({
                "_uid": ctx.author.id
            })
            if not isexist:
                rpswinstreak.insert_one({
                    "_uid": ctx.author.id,
                    "winstreak": 1
                })
            else:
                rpswinstreak.update_one({
                    "_uid": ctx.author.id
                },{
                    "$inc":{
                        "winstreak": 1
                    }
                })
            winstreakresult = rpswinstreak.find_one({
                "_uid": ctx.author.id
            })
            winstreak = winstreakresult['winstreak']
            isreexist = rpswinstreakre.find_one({
                "_uid": ctx.author.id
            })
            if not isreexist:
                rpswinstreakre.insert_one({
                    "_uid": ctx.author.id,
                    "highestwinstreak": winstreak
                })
            elif winstreak > isreexist['highestwinstreak']:
                rpswinstreakre.update_one({
                    "_uid": ctx.author.id
                },{
                    "$set":{
                        "highestwinstreak": winstreak
                    }
                })
            else:
                pass
            rpshighestwinstreakre = rpswinstreakre.find_one({
                "_uid": ctx.author.id
            })
            rpshighestwinstreak = rpshighestwinstreakre['highestwinstreak']
            embed.add_field(name="當前連勝", value=f"`{winstreak}`", inline=True)
            embed.add_field(name="自身最高連勝", value=f"`{rpshighestwinstreak}`", inline=True)
            getacc = cd.find_one({
                "_id": str(ctx.author.id)
            })
            if getacc:
                if getacc['money'] >= num:
                    if winstreak == 1:
                        bonus = int(0.65 * num)
                    else:
                        bonus = int((1.3 ** winstreak) * num) - num
                    cd.update_one({
                        "_id": str(ctx.author.id)
                    },{
                        "$inc":{
                            "money": bonus
                        }
                    })
                    embed.set_footer(text=f"獲得 ¥ {bonus}")
                else:
                    embed.set_footer(text="娛樂遊戲")
            else:
                embed.set_footer(text="沒有賬戶")
        elif result == "Bot Win":
            isexist = rpswinstreak.find_one({
                "_uid": ctx.author.id
            })
            if isexist:
                rpswinstreak.delete_one({
                    "_uid": ctx.author.id
                })
            else:
                pass
            rpshighestwinstreakre = rpswinstreakre.find_one({
                "_uid": ctx.author.id
            })
            if rpshighestwinstreakre:
                rpshighestwinstreak = rpshighestwinstreakre['highestwinstreak']
            else:
                rpshighestwinstreak = 0
            embed.add_field(name="當前連勝", value="`0`", inline=True)
            embed.add_field(name="自身最高連勝", value=f"`{rpshighestwinstreak}`", inline=True)
            getacc = cd.find_one({
                "_id": str(ctx.author.id)
            })
            if getacc:
                if getacc['money'] >= num:
                    cd.update_one({
                        "_id": str(ctx.author.id)
                    },{
                        "$inc":{
                            "money": -num
                        }
                    })
                    embed.set_footer(text=f"損失 ¥ {num}")
                else:
                    embed.set_footer(text="娛樂遊戲")
            else:
                embed.set_footer(text="沒有賬戶")
        else:
            winstreakresult = rpswinstreak.find_one({
                "_uid": ctx.author.id
            })
            if winstreakresult:
                winstreak = winstreakresult['winstreak']
            else:
                winstreak = 0
            rpshighestwinstreakre = rpswinstreakre.find_one({
                "_uid": ctx.author.id
            })
            if rpshighestwinstreakre:
                rpshighestwinstreak = rpshighestwinstreakre['highestwinstreak']
            else:
                rpshighestwinstreak = 0
            embed.add_field(name="當前連勝", value=f"`{winstreak}`", inline=True)
            embed.add_field(name="自身最高連勝", value=f"`{rpshighestwinstreak}`", inline=True)
            getacc = cd.find_one({
                "_id": str(ctx.author.id)
            })
            if getacc:
                if getacc['money'] >= num:
                    cd.update_one({
                        "_id": str(ctx.author.id)
                    },{
                        "$inc":{
                            "money": -int(0.28 * num)
                        }
                    })
                    embed.set_footer(text=f"損失 ¥ {int(0.28 * num)}")
                else:
                    embed.set_footer(text="娛樂遊戲")
            else:
                embed.set_footer(text="沒有賬戶")
        highest = rpswinstreakre.find_one({}, sort=[("highestwinstreak", pymongo.DESCENDING)])
        highestuser = ctx.guild.get_member(highest['_uid'])
        embed.add_field(name="伺服器最高連勝", value=f"{highestuser.mention} 達成 `{highest['highestwinstreak']}` 連勝", inline=False)
        await ctx.send(ctx.author.mention, embed=embed)
    
    #coin flip
    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx, memberchoice=None, num:int=None):
        with open('./data.json', 'r', encoding = 'utf8') as jfile2:
	          jdata2 = json.load(jfile2)
        if not ctx.channel.id in jdata2['gamecmdchannel']:
            await ctx.message.delete(delay=10)
            await ctx.send("請在指定頻道使用此指令", delete_after=10)
            return
        if not memberchoice:
            memberchoice = random.choice(["正面", "反面"])
        if not memberchoice == "正面" and not memberchoice == "反面":
            await ctx.message.delete(delay=10)
            await ctx.send("指令用法：^cf [正面/反面]", delete_after=10)
            return
        # if not num:
        num = 1000
        botchoice = random.choice(["正面", "反面"])
        if memberchoice == "正面":
            botchoice = choice(["正面", "反面"], p=[0.46, 0.54])
        if memberchoice == "反面":
            botchoice = choice(["正面", "反面"], p=[0.54, 0.46])
        result = None
        if botchoice == memberchoice:
            result = "Member Win"
        else:
            result = "Bot Win"
        if botchoice == "正面":
            url = "https://raw.githubusercontent.com/jackey991206/saveimage/main/Misaka_Mikoto_coin_observe.png"
        elif botchoice == "反面":
            url = "https://raw.githubusercontent.com/jackey991206/saveimage/main/Misaka_Mikoto_coin_reserve.png"
        embed = discord.Embed(title="擲硬幣", description=f"參與者：\n{ctx.author.mention}", color=0x6666ff,timestamp=datetime.datetime.now())
        if not ctx.author.nick == None:
            displayname = ctx.author.nick
        else:
            displayname = ctx.author.name
        if result == "Bot Win":
            displayresult = "你猜錯了"
        elif result == "Member Win":
            displayresult = "你猜對了"
        now_datetime = datetime.datetime.now()+hours_added
        cfid = cfre.find().count()+1
        cfre.insert_one({
            "_rpsid": cfid,
            "uid": ctx.author.id,
            "member_choice": memberchoice,
            "bot_choice": botchoice,
            "result": result,
            "at": now_datetime
        })
        embed.add_field(name=f"{displayname}猜", value=memberchoice, inline=True)
        embed.add_field(name=f"{self.bot.user.name}擲出", value=botchoice, inline=True)
        embed.add_field(name="結果", value=displayresult, inline=True)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url=url)
        if result == "Member Win":
            isexist = cfwinstreak.find_one({
                "_uid": ctx.author.id
            })
            if not isexist:
                cfwinstreak.insert_one({
                    "_uid": ctx.author.id,
                    "winstreak": 1
                })
            else:
                cfwinstreak.update_one({
                    "_uid": ctx.author.id
                },{
                    "$inc":{
                        "winstreak": 1
                    }
                })
            winstreakresult = cfwinstreak.find_one({
                "_uid": ctx.author.id
            })
            winstreak = winstreakresult['winstreak']
            isreexist = cfwinstreakre.find_one({
                "_uid": ctx.author.id
            })
            if not isreexist:
                cfwinstreakre.insert_one({
                    "_uid": ctx.author.id,
                    "highestwinstreak": winstreak
                })
            elif winstreak > isreexist['highestwinstreak']:
                cfwinstreakre.update_one({
                    "_uid": ctx.author.id
                },{
                    "$set":{
                        "highestwinstreak": winstreak
                    }
                })
            else:
                pass
            cfhighestwinstreakre = cfwinstreakre.find_one({
                "_uid": ctx.author.id
            })
            cfhighestwinstreak = cfhighestwinstreakre['highestwinstreak']
            embed.add_field(name="當前連勝", value=winstreak, inline=True)
            embed.add_field(name="自身最高連勝", value=cfhighestwinstreak, inline=True)
            getacc = cd.find_one({
                "_id": str(ctx.author.id)
            })
            if getacc:
                if getacc['money'] >= num:
                    if winstreak == 1:
                        bonus = int(0.7 * num)
                    else:
                        bonus = int((1.4 ** winstreak) * num) - num
                    cd.update_one({
                        "_id": str(ctx.author.id)
                    },{
                        "$inc":{
                            "money": bonus
                        }
                    })
                    embed.set_footer(text=f"獲得 ¥ {bonus}")
                else:
                    embed.set_footer(text="娛樂遊戲")
            else:
                embed.set_footer(text="沒有賬戶")
        elif result == "Bot Win":
            isexist = cfwinstreak.find_one({
                "_uid": ctx.author.id
            })
            if isexist:
                cfwinstreak.delete_one({
                    "_uid": ctx.author.id
                })
            else:
                pass
            cfhighestwinstreakre = cfwinstreakre.find_one({
                "_uid": ctx.author.id
            })
            if cfhighestwinstreakre:
                cfhighestwinstreak = cfhighestwinstreakre['highestwinstreak']
            else:
                cfhighestwinstreak = 0
            embed.add_field(name="當前連勝", value=0, inline=True)
            embed.add_field(name="自身最高連勝", value=cfhighestwinstreak, inline=True)
            getacc = cd.find_one({
                "_id": str(ctx.author.id)
            })
            if getacc:
                if getacc['money'] >= num:
                    cd.update_one({
                        "_id": str(ctx.author.id)
                    },{
                        "$inc":{
                            "money": -num
                        }
                    })
                    embed.set_footer(text=f"損失 ¥ {num}")
                else:
                    embed.set_footer(text="娛樂遊戲")
            else:
                embed.set_footer(text="沒有賬戶")
        highest = cfwinstreakre.find_one({}, sort=[("highestwinstreak", pymongo.DESCENDING)])
        highestuser = ctx.guild.get_member(highest['_uid'])
        embed.add_field(name="伺服器最高連勝", value=f"{highestuser.mention} 達成 `{highest['highestwinstreak']}` 連勝", inline=False)
        embed0 = discord.Embed()
        randurl = random.choice(["https://raw.githubusercontent.com/jackey991206/saveimage/main/coin_observe.png", "https://raw.githubusercontent.com/jackey991206/saveimage/main/coin_reserve.png"])
        embed0.set_image(url=randurl)
        msg = await ctx.send(ctx.author.mention, embed=embed0)
        counter = 1
        while counter < 8:
            counter += 1
            if counter % 2 == 0:
                await msg.edit(embed=None)
                await asyncio.sleep(0.1)
            else:
                randurl = random.choice(["https://raw.githubusercontent.com/jackey991206/saveimage/main/coin_observe.png", "https://raw.githubusercontent.com/jackey991206/saveimage/main/coin_reserve.png"])
                embed0.set_image(url=randurl)
                await msg.edit(embed=embed0)
                await asyncio.sleep(1)
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(Game(bot))