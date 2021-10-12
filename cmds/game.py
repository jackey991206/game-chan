import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import pymongo
import datetime
import random
import os
from numpy.random import choice
# import asyncio

cluster = pymongo.MongoClient(os.environ['DBCONNECT'])
db = cluster["checkmatevotingdb"]
rpswinstreak = db["rpswinstreak"]
rpswinstreakre = db["rpswinstreakre"]
rpsre = db["rpsrecord"]
cfwinstreak = db["cfwinstreak"]
cfwinstreakre = db["cfwinstreakre"]
cfre = db["cfrecord"]
gamblers = db["gamblers"]
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
            await ctx.send(f"指令用法：{self.bot.command_prefix}rps [石頭/剪刀/布]", delete_after=10)
            return
        # if not num:
        num = 1000
        if memberchoice == "石頭":
            botchoice = choice(["石頭", "剪刀", "布"], p=[0.34, 0.33, 0.33])
        if memberchoice == "剪刀":
            botchoice = choice(["石頭", "剪刀", "布"], p=[0.33, 0.34, 0.33])
        if memberchoice == "布":
            botchoice = choice(["石頭", "剪刀", "布"], p=[0.33, 0.33, 0.34])
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
            gog = gamblers.find_one({
                "_uid": ctx.author.id
            })
            if getacc:
                if getacc['money'] >= num:
                    currentday = now_datetime.strftime("%A")
                    currenttime = int(now_datetime.strftime("%H%M"))
                    if currentday in ["Saturday", "Sunday"]:
                        if currenttime >= 2000 and  currenttime < 2200:
                            if winstreak == 1:
                                bonus = int(0.65 * 2 * num)
                            else:
                                bonus = int((1.3 ** winstreak) * 2 * num) - num
                        else:
                            if winstreak == 1:
                                bonus = int(0.65 * 1.5 * num)
                            else:
                                bonus = int((1.3 ** winstreak) * 1.5 * num) - num
                    else:
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
                    if gog:
                        gamblers.update_one({
                            "_uid": ctx.author.id
                        },{
                            "$inc":{
                                "values": bonus
                            }
                        })
                    else:
                        gamblers.insert_one({
                            "_uid": ctx.author.id,
                            "values": bonus
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
            gog = gamblers.find_one({
                "_uid": ctx.author.id
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
                    if gog:
                        gamblers.update_one({
                            "_uid": ctx.author.id
                        },{
                            "$inc":{
                                "values": -num
                            }
                        })
                    else:
                        gamblers.insert_one({
                            "_uid": ctx.author.id,
                            "values": -num
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
            gog = gamblers.find_one({
                "_uid": ctx.author.id
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
                    if gog:
                        gamblers.update_one({
                            "_uid": ctx.author.id
                        },{
                            "$inc":{
                                "values": -int(0.28 * num)
                            }
                        })
                    else:
                        gamblers.insert_one({
                            "_uid": ctx.author.id,
                            "values": -int(0.28 * num)
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
            await ctx.send(f"指令用法：{self.bot.command_prefix}cf [正面/反面]", delete_after=10)
            return
        # if not num:
        num = 1000
        botchoice = random.choice(["正面", "反面"])
        if memberchoice == "正面":
            botchoice = choice(["正面", "反面"], p=[0.49, 0.51])
        if memberchoice == "反面":
            botchoice = choice(["正面", "反面"], p=[0.51, 0.49])
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
            gog = gamblers.find_one({
                "_uid": ctx.author.id
            })
            if getacc:
                if getacc['money'] >= num:
                    currentday = now_datetime.strftime("%A")
                    currenttime = int(now_datetime.strftime("%H%M"))
                    if currentday in ["Saturday", "Sunday"]:
                        if currenttime >= 2000 and  currenttime < 2200:
                            if winstreak == 1:
                                bonus = int(0.7 * 2 * num)
                            else:
                                bonus = int((1.4 ** winstreak) * 2 * num) - num
                        else:
                            if winstreak == 1:
                                bonus = int(0.7 * 1.5 * num)
                            else:
                                bonus = int((1.4 ** winstreak) * 1.5 * num) - num
                    else:
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
                    if gog:
                        gamblers.update_one({
                            "_uid": ctx.author.id
                        },{
                            "$inc":{
                                "values": bonus
                            }
                        })
                    else:
                        gamblers.insert_one({
                            "_uid": ctx.author.id,
                            "values": bonus
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
            gog = gamblers.find_one({
                "_uid": ctx.author.id
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
                    if gog:
                        gamblers.update_one({
                            "_uid": ctx.author.id
                        },{
                            "$inc":{
                                "values": -num
                            }
                        })
                    else:
                        gamblers.insert_one({
                            "_uid": ctx.author.id,
                            "values": -num
                        })
                    embed.set_footer(text=f"損失 ¥ {num}")
                else:
                    embed.set_footer(text="娛樂遊戲")
            else:
                embed.set_footer(text="沒有賬戶")
        highest = cfwinstreakre.find_one({}, sort=[("highestwinstreak", pymongo.DESCENDING)])
        highestuser = ctx.guild.get_member(highest['_uid'])
        embed.add_field(name="伺服器最高連勝", value=f"{highestuser.mention} 達成 `{highest['highestwinstreak']}` 連勝", inline=False)
        # embed0 = discord.Embed()
        # randurl = random.choice(["https://raw.githubusercontent.com/jackey991206/saveimage/main/coin_observe.png", "https://raw.githubusercontent.com/jackey991206/saveimage/main/coin_reserve.png"])
        # embed0.set_image(url=randurl)
        # msg = await ctx.send(ctx.author.mention, embed=embed0)
        # counter = 1
        # while counter < 4:
        #     counter += 1
        #     if counter % 2 == 0:
        #         await msg.edit(embed=None)
        #         await asyncio.sleep(0.1)
        #     else:
        #         randurl = random.choice(["https://raw.githubusercontent.com/jackey991206/saveimage/main/coin_observe.png", "https://raw.githubusercontent.com/jackey991206/saveimage/main/coin_reserve.png"])
        #         embed0.set_image(url=randurl)
        #         await msg.edit(embed=embed0)
        #         await asyncio.sleep(1)
        # await msg.edit(embed=embed)
        await ctx.send(ctx.author.mention, embed=embed)
    
    #Guess the number
    @commands.command(aliases=['gn'])
    async def guessnumber(self, ctx):
        with open('./data.json', 'r', encoding = 'utf8') as jfile2:
	          jdata2 = json.load(jfile2)
        if not ctx.channel.id in jdata2['guessnumberchannel']:
            await ctx.message.delete(delay=10)
            await ctx.send("請在指定頻道使用此指令", delete_after=10)
            return
        with open('./guessnumber.json', 'r', encoding = 'utf8') as jfilegn:
            jdatagn = json.load(jfilegn)
        with open('./guesstimes.json', 'r', encoding = 'utf8') as jfilegt:
            jdatagt = json.load(jfilegt)
        if not str(ctx.author.id) in jdatagt:
            pass
        elif jdatagt[str(ctx.author.id)] == 5:
            pass
        elif not jdatagt[str(ctx.author.id)] == 5:
            await ctx.send(f"{ctx.author.mention} 請先完成上一場遊戲")
            return
        else:
            pass
        jdatagn[str(ctx.author.id)] = random.randint(1, jdata2['range'])
        with open('./guessnumber.json', 'w', encoding = 'utf8') as jfilegn:
            json.dump(jdatagn, jfilegn)
        jdatagt[str(ctx.author.id)] = 0
        with open('./guesstimes.json', 'w', encoding = 'utf8') as jfilegt:
            json.dump(jdatagt, jfilegt)
        with open('./guesstype.json', 'r', encoding = 'utf8') as jfilegty:
            jdatagty = json.load(jfilegty)
        getacc = cd.find_one({
            "_id": str(ctx.author.id)
        })
        if getacc:
            if getacc['money'] >= 1500:
                await ctx.send(f"{ctx.author.mention} 開始猜號碼\n請注意：本場遊戲為計費遊戲\n下面開始猜第`1`次數字")
                jdatagty[str(ctx.author.id)] = "billing"
            else:
                await ctx.send(f"{ctx.author.mention} 開始猜號碼\n請注意：由於你的賬戶餘額不足 `1500PT` 本場遊戲將不會有任何的計費\n下面開始猜第`1`次數字")
                jdatagty[str(ctx.author.id)] = "entertainment"
        else:
            await ctx.send(f"{ctx.author.mention} 開始猜號碼\n請注意：由於你沒有賬戶，本場遊戲不會有任何的獲利\n下面開始猜第`1`次數字")
            jdatagty[str(ctx.author.id)] = "nonaccount"
        with open('./guesstype.json', 'w', encoding = 'utf8') as jfilegty:
            json.dump(jdatagty, jfilegty)

    @commands.Cog.listener()
    async def on_message(self, msg):
        with open('./data.json', 'r', encoding = 'utf8') as jfile2:
	          jdata2 = json.load(jfile2)
        if not msg.channel.id in jdata2['guessnumberchannel']:
            return
        if msg.author.bot:
            return
        try:
            int(msg.content)
        except:
            return
        with open('./guesstimes.json', 'r', encoding = 'utf8') as jfilegt:
            jdatagt = json.load(jfilegt)
        if not str(msg.author.id) in jdatagt:
            return
        if jdatagt[str(msg.author.id)] == 5:
            await msg.channel.send(f"{msg.author.mention} 開始下一局猜數字遊戲吧~")
            return
        current = datetime.datetime.now() + hours_added
        guessnum = int(msg.content)
        times = jdatagt[str(msg.author.id)] + 1
        jdatagt[str(msg.author.id)] = times
        with open('./guesstimes.json', 'w', encoding = 'utf8') as jfilegt:
            json.dump(jdatagt, jfilegt)
        with open('./guessnumber.json', 'r', encoding = 'utf8') as jfilegn:
            jdatagn = json.load(jfilegn)
        with open('./guesstype.json', 'r', encoding = 'utf8') as jfilegty:
            jdatagty = json.load(jfilegty)
        with open('./guessgap.json', 'r', encoding = 'utf8') as jfilegg:
            jdatagg = json.load(jfilegg)
        if guessnum > jdatagn[str(msg.author.id)] or guessnum < jdatagn[str(msg.author.id)]:
            firstsentence = f"第`{times}`次猜錯了，"
            if guessnum > jdatagn[str(msg.author.id)]:
                if guessnum-jdatagn[str(msg.author.id)] > jdatagg['farthest']:
                    secondsentence = "你猜得太大了，差得很遠呢"
                elif guessnum-jdatagn[str(msg.author.id)] > jdatagg['medium'] and guessnum-jdatagn[str(msg.author.id)] <= jdatagg['farthest']:
                    secondsentence =  "你猜得大了，但不是離得太遠~"
                elif guessnum-jdatagn[str(msg.author.id)] > jdatagg['nearest'] and guessnum-jdatagn[str(msg.author.id)] <= jdatagg['medium']:
                    secondsentence = "你猜大了，但接近了~"
                else:
                    secondsentence = f"你猜大了，`{jdatagg['nearest']}`步之內"
                # else:
                #    secondsentence = "你猜大了，但接近了~"
            if guessnum < jdatagn[str(msg.author.id)]:
                if jdatagn[str(msg.author.id)]-guessnum > jdatagg['farthest']:
                    secondsentence = "你猜得太小了，差得很遠呢"
                elif jdatagn[str(msg.author.id)]-guessnum > jdatagg['medium'] and jdatagn[str(msg.author.id)]-guessnum <= jdatagg['farthest']:
                    secondsentence = "你猜得小了，但不是離得太遠~"
                elif jdatagn[str(msg.author.id)]-guessnum > jdatagg['nearest'] and jdatagn[str(msg.author.id)]-guessnum <= jdatagg['medium']:
                    secondsentence = "你猜小了，但接近了~"
                else:
                    secondsentence = f"你猜小了，`{jdatagg['nearest']}`步之內"
                # else:
                #     secondsentence = "你猜小了，但接近了~"
            if jdatagty[str(msg.author.id)] == "billing":
                gog = gamblers.find_one({
                    "_uid": msg.author.id
                })
                if times == 1:
                    minus = 100
                elif times == 2:
                    minus = 200
                elif times == 3:
                    minus = 300
                elif times == 4:
                    minus = 400
                elif times == 5:
                    minus = 500
                else:
                    minus = 0
                cd.update_one({
                    "_id": str(msg.author.id)
                },{
                    "$inc":{
                        "money": -minus
                    }
                })
                if gog:
                    gamblers.update_one({
                        "_uid": msg.author.id
                    },{
                        "$inc":{
                            "values": -minus
                        }
                    })
                else:
                    gamblers.insert_one({
                        "_uid": msg.author.id,
                        "values": -minus
                    })
                if not times == 5:
                    await msg.channel.send(f"{msg.author.mention} {firstsentence}{secondsentence}\n本輪扣除 `{minus}PT`，接著猜第`{times+1}`次吧")
                else:
                    await msg.channel.send(f"{msg.author.mention} {firstsentence}{secondsentence}\n本輪扣除 `{minus}PT`，本場答案为**{jdatagn[str(msg.author.id)]}**\n你用完了5次機會，重新猜一局吧~")
            if jdatagty[str(msg.author.id)] == "entertainment":
                if not times == 5:
                    await msg.channel.send(f"{msg.author.mention} {firstsentence}{secondsentence}\n本輪為娛樂遊戲，接著猜第`{times+1}`次吧")
                else:
                    await msg.channel.send(f"{msg.author.mention} {firstsentence}{secondsentence}\n本輪為娛樂遊戲，本場答案为**{jdatagn[str(msg.author.id)]}**\n你用完了5次機會，重新猜一局吧~")
            if jdatagty[str(msg.author.id)] == "nonaccount":
                if not times == 5:
                    await msg.channel.send(f"{msg.author.mention} {firstsentence}{secondsentence}\n沒有賬戶用以增減PT，接著猜第`{times+1}`次吧")
                else:
                    await msg.channel.send(f"{msg.author.mention} {firstsentence}{secondsentence}\n沒有賬戶用以增減PT，本場答案为**{jdatagn[str(msg.author.id)]}**\n你用完了5次機會，重新猜一局吧~")
        if guessnum == jdatagn[str(msg.author.id)]:
            if jdatagty[str(msg.author.id)] == "billing":
                currentday = current.strftime("%A")
                currenttime = int(current.strftime("%H%M"))
                gog = gamblers.find_one({
                    "_uid": msg.author.id
                })
                if times == 1:
                    bonus = 3000
                    rebate = 0
                elif times == 2:
                    bonus = 2000
                    rebate = 100
                elif times == 3:
                    bonus = 1200
                    rebate = 300
                elif times == 4:
                    bonus = 600
                    rebate = 600
                elif times == 5:
                    bonus = 200
                    rebate = 1000
                else:
                    bonus = 0
                    rebate = 0
                if currentday in ["Saturday", "Sunday"]:
                    if currenttime >= 2000 and  currenttime < 2200:
                        total = int(bonus * 2) + rebate
                    else:
                        total = int(bonus * 1.5) + rebate
                else:
                    total = bonus + rebate
                cd.update_one({
                    "_id": str(msg.author.id)
                },{
                    "$inc":{
                        "money": total
                    }
                })
                if gog:
                    gamblers.update_one({
                        "_uid": msg.author.id
                    },{
                        "$inc":{
                            "values": total
                        }
                    })
                else:
                    gamblers.insert_one({
                        "_uid": msg.author.id,
                        "values": total
                    })
                if times == 1:
                    await msg.channel.send(f"{msg.author.mention} 居然一次就猜中，太不可思議了吧，恭喜你獲得 `{total}PT` <a:waaaaaa:894791520933261334>")
                else:
                    sentence = ["好厲害！！！", "太棒了！！！", "太神啦！！！"]
                    await msg.channel.send(f"{msg.author.mention} 你猜中了，{random.choice(sentence)}，獲得 `{total}PT`")
            if jdatagty[str(msg.author.id)] == "entertainment":
                if times == 1:
                    await msg.channel.send(f"{msg.author.mention} 居然一次就猜中，太不可思議了吧，但遺憾的是，本場為娛樂遊戲~")
                else:
                    sentence = ["好厲害！！！", "太棒了！！！", "太神啦！！！"]
                    await msg.channel.send(f"{msg.author.mention} 你猜中了，{random.choice(sentence)}，但遺憾的是，本場為娛樂遊戲~")
            if jdatagty[str(msg.author.id)] == "nonaccount":
                if times == 1:
                    await msg.channel.send(f"{msg.author.mention} 居然一次就猜中，太不可思議了吧，但遺憾的是，你沒有賬戶~")
                else:
                    sentence = ["好厲害！！！", "太棒了！！！", "太神啦！！！"]
                    await msg.channel.send(f"{msg.author.mention} 你猜中了，{random.choice(sentence)}，但遺憾的是，你沒有賬戶~")
            jdatagt[str(msg.author.id)] = 5
            with open('./guesstimes.json', 'w', encoding = 'utf8') as jfilegt:
                json.dump(jdatagt, jfilegt)

def setup(bot):
    bot.add_cog(Game(bot))