import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import pymongo
import os

secondcluster = pymongo.MongoClient(os.environ['db_connect'])
db2 = secondcluster["MoneyData"]
cd = db2["ClientData"]

def checkp(guild, author, level):
    with open('./data.json', 'r', encoding = 'utf8') as jfiled:
	      jdatad = json.load(jfiled)
    if level == 1:
        adminrole = [discord.utils.get(guild.roles, id=ar) for ar in jdatad['adminlevelone']]
    elif level == 2:
        adminrole = [discord.utils.get(guild.roles, id=ar) for ar in jdatad['adminlevelone']]
        adminrole += [discord.utils.get(guild.roles, id=ar) for ar in jdatad['adminleveltwo']]
    elif level == 3:
        adminrole = [discord.utils.get(guild.roles, id=ar) for ar in jdatad['adminlevelone']]
        adminrole += [discord.utils.get(guild.roles, id=ar) for ar in jdatad['adminleveltwo']]
        adminrole += [discord.utils.get(guild.roles, id=ar) for ar in jdatad['adminlevelthree']]
    counter = 0
    for a in adminrole:
        if a in author.roles:
            counter = 1
            break
        else:
            pass
    if counter == 1:
        return True
    else:
        return False

class Counting(Cog_Extension):

    @commands.command(aliases=['acc'])
    async def addcountingchannel(self, ctx):
        with open('./data.json', 'r', encoding = 'utf8') as jfiled:
	          jdatad = json.load(jfiled)
        if not checkp(ctx.guild, ctx.author, jdatad['setchannel']):
            await ctx.send(f"要求 {jdatad['setchannel']} 級權限")
            return
        channel = ctx.channel
        cid = channel.id
        with open('./counting.json', 'r', encoding = 'utf8') as jfile:
            jdata = json.load(jfile)
            if not jdata['CONTINUE']:
                jdata['CONTINUE'] = {}
            if not jdata['RECORD']:
                jdata['RECORD'] = {}
            isexist = 0
            for c in jdata['CONTINUE']:
                if c == cid:
                    isexist = 1
                    break
                else:
                    pass
            if isexist == 0:
                jdata['CONTINUE'][f'{str(ctx.channel.id)}'] = {}
                jdata['CONTINUE'][f'{str(ctx.channel.id)}']['lastuser'] = 0
                jdata['CONTINUE'][f'{str(ctx.channel.id)}']['counting'] = 0
                jdata['CONTINUE'][f'{str(ctx.channel.id)}']['msgid'] = 0
            isexist = 0
            for c in jdata['RECORD']:
                if c == cid:
                    isexist = 1
                    break
                else:
                    pass
            if isexist == 0:
                jdata['RECORD'][f'{str(ctx.channel.id)}'] = {}
                jdata['RECORD'][f'{str(ctx.channel.id)}']['recorduser'] = 0
                jdata['RECORD'][f'{str(ctx.channel.id)}']['counting'] = 0
                jdata['RECORD'][f'{str(ctx.channel.id)}']['msgid'] = 0
            if not isexist == 0:
                await ctx.message.delete()
                await ctx.send(f"{channel.mention}已經是{self.bot.user.name}指令頻道了", delete_after=15)
                return
        with open('./counting.json', 'w', encoding = 'utf8') as jfile:
            json.dump(jdata, jfile)
        await ctx.message.delete()
        await ctx.send(f"成功把{channel.mention}加入{self.bot.user.name}指令頻道", delete_after=15)

    @commands.command(aliases=['dcc'])
    async def dropcountingchannel(self, ctx):
        with open('./data.json', 'r', encoding = 'utf8') as jfiled:
	          jdatad = json.load(jfiled)
        if not checkp(ctx.guild, ctx.author, jdatad['setchannel']):
            await ctx.send(f"要求 {jdatad['setchannel']} 級權限")
            return
        channel = ctx.channel
        cid = channel.id
        with open('./counting.json', 'r', encoding = 'utf8') as jfile:
            jdata = json.load(jfile)
            isexist = 0
            for c in jdata['CONTINUE']:
                if c == str(cid):
                    isexist = 1
                    break
                else:
                    pass
            if not isexist == 0:
                del jdata['CONTINUE'][f'{str(ctx.channel.id)}']
            isexist = 0
            for c in jdata['RECORD']:
                if c == str(cid):
                    isexist = 1
                    break
                else:
                    pass
            if not isexist == 0:
                del jdata['RECORD'][f'{str(ctx.channel.id)}']
            if isexist == 0:
                await ctx.message.delete()
                await ctx.send(f"{channel.mention}還不是{self.bot.user.name}指令頻道", delete_after=15)
                return
        with open('./counting.json', 'w', encoding = 'utf8') as jfile:
            json.dump(jdata, jfile)
        await ctx.message.delete()
        await ctx.send(f"成功把{channel.mention}從{self.bot.user.name}指令頻道中移除", delete_after=15)

    @commands.Cog.listener()
    async def on_message(self, msg):
        with open('./counting.json', 'r', encoding = 'utf8') as jfilec:
            jdatac = json.load(jfilec)
        if str(msg.channel.id) in jdatac['CONTINUE'] and str(msg.channel.id) in jdatac['RECORD'] and not msg.author.bot:
            try:
                inputnum = int(msg.content)
                nextnum = jdatac['CONTINUE'][str(msg.channel.id)]['counting'] + 1
                if inputnum == 0:
                    if jdatac['CONTINUE'][str(msg.channel.id)]['counting'] > jdatac['RECORD'][str(msg.channel.id)]['counting']:
                        if not jdatac['RECORD'][str(msg.channel.id)]['recorduser'] == 0:
                            try:
                                recorduser = msg.guild.get_member(jdatac['RECORD'][str(msg.channel.id)]['recorduser'])
                            except:
                                pass
                        if not jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] == 0:
                            try:
                                lastuser = msg.guild.get_member(jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'])
                            except:
                                pass
                        if not jdatac['RECORD'][str(msg.channel.id)]['msgid'] == 0:
                            try:
                                msg0 = await msg.channel.fetch_message(jdatac['RECORD'][str(msg.channel.id)]['msgid'])
                                await msg0.unpin()
                            except:
                                pass
                        if not jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] == 0:
                            try:
                                msg1 = await msg.channel.fetch_message(jdatac['CONTINUE'][str(msg.channel.id)]['msgid'])
                                await msg1.pin()
                            except:
                                pass
                        isexist = cd.find_one({
                            "_id": str(lastuser.id)
                        })
                        if isexist:
                            bonus = 10 * jdatac['CONTINUE'][str(msg.channel.id)]['counting']
                            cd.update_one({
                                "_id": str(lastuser.id)
                            },{
                                "$inc":{
                                    "money": bonus
                                }
                            })
                            if not jdatac['RECORD'][str(msg.channel.id)]['recorduser'] == 0:
                                try:
                                    await msg.channel.send(f"{lastuser.mention} 突破了 {recorduser.mention} 的記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                                except:
                                    await msg.channel.send(f"{lastuser.mention} 突破了 {jdatac['RECORD'][str(msg.channel.id)]['recorduser']} 的記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                            else:
                                await msg.channel.send(f"{lastuser.mention} 突破了記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                        else:
                            await msg.channel.send(f"{lastuser.mention} 突破了 {recorduser.mention} 的記錄達到 `{inputnum}` 但是沒有賬戶 無法獲得獎勵")
                        jdatac['RECORD'][str(msg.channel.id)]['recorduser'] = jdatac['CONTINUE'][str(msg.channel.id)]['lastuser']
                        jdatac['RECORD'][str(msg.channel.id)]['counting'] = jdatac['CONTINUE'][str(msg.channel.id)]['counting']
                        jdatac['RECORD'][str(msg.channel.id)]['msgid'] = jdatac['CONTINUE'][str(msg.channel.id)]['msgid']
                    await msg.add_reaction(emoji="🔁")
                    jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] = 0
                    jdatac['CONTINUE'][str(msg.channel.id)]['counting'] = 0
                    jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] = 0
                elif not msg.author.id == jdatac['CONTINUE'][str(msg.channel.id)]['lastuser']:
                    if inputnum == nextnum:
                        await msg.add_reaction(emoji="⭕")
                        jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] = msg.author.id
                        jdatac['CONTINUE'][str(msg.channel.id)]['counting'] += 1
                        jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] = msg.id
                        with open('./countingbonus.json', 'r', encoding = 'utf8') as jfileb:
                            jdatab = json.load(jfileb)
                        if str(inputnum) in jdatab:
                            for b in jdatab:
                                if str(inputnum) == b:
                                    bonus = jdatab[str(inputnum)]
                                    break
                                else:
                                    pass
                            isexist = cd.find_one({
                                "_id": str(msg.author.id)
                            })
                            if isexist:
                                cd.update_one({
                                    "_id": str(msg.author.id)
                                },{
                                    "$inc":{
                                        "money": bonus
                                    }
                                })
                                await msg.channel.send(f"{msg.author.mention} 達到`{inputnum}` 獲得 `{bonus}PT` 作為獎勵")
                            else:
                                await msg.channel.send(f"{msg.author.mention} 沒有賬戶 無法獲得獎勵")
                        else:
                            pass
                    else:
                        if jdatac['CONTINUE'][str(msg.channel.id)]['counting'] > jdatac['RECORD'][str(msg.channel.id)]['counting']:
                            if not jdatac['RECORD'][str(msg.channel.id)]['recorduser'] == 0:
                                try:
                                    recorduser = msg.guild.get_member(jdatac['RECORD'][str(msg.channel.id)]['recorduser'])
                                except:
                                    pass
                            if not jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] == 0:
                                try:
                                    lastuser = msg.guild.get_member(jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'])
                                except:
                                    pass
                            if not jdatac['RECORD'][str(msg.channel.id)]['msgid'] == 0:
                                try:
                                    msg0 = await msg.channel.fetch_message(jdatac['RECORD'][str(msg.channel.id)]['msgid'])
                                    await msg0.unpin()
                                except:
                                    pass
                            if not jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] == 0:
                                try:
                                    msg1 = await msg.channel.fetch_message(jdatac['CONTINUE'][str(msg.channel.id)]['msgid'])
                                    await msg1.pin()
                                except:
                                    pass
                            isexist = cd.find_one({
                                "_id": str(lastuser.id)
                            })
                            if isexist:
                                bonus = 10 * jdatac['CONTINUE'][str(msg.channel.id)]['counting']
                                cd.update_one({
                                    "_id": str(lastuser.id)
                                },{
                                    "$inc":{
                                        "money": bonus
                                    }
                                })
                                if not jdatac['RECORD'][str(msg.channel.id)]['recorduser'] == 0:
                                    try:
                                        await msg.channel.send(f"{lastuser.mention} 突破了 {recorduser.mention} 的記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                                    except:
                                        await msg.channel.send(f"{lastuser.mention} 突破了 {jdatac['RECORD'][str(msg.channel.id)]['recorduser']} 的記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                                else:
                                    await msg.channel.send(f"{lastuser.mention} 突破了記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                            else:
                                await msg.channel.send(f"{lastuser.mention} 突破了 {recorduser.mention} 的記錄達到 `{inputnum}` 但是沒有賬戶 無法獲得獎勵")
                            jdatac['RECORD'][str(msg.channel.id)]['recorduser'] = jdatac['CONTINUE'][str(msg.channel.id)]['lastuser']
                            jdatac['RECORD'][str(msg.channel.id)]['counting'] = jdatac['CONTINUE'][str(msg.channel.id)]['counting']
                            jdatac['RECORD'][str(msg.channel.id)]['msgid'] = jdatac['CONTINUE'][str(msg.channel.id)]['msgid']
                        await msg.add_reaction(emoji="❌")
                        jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] = 0
                        jdatac['CONTINUE'][str(msg.channel.id)]['counting'] = 0
                        jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] = 0
                else:
                    if jdatac['CONTINUE'][str(msg.channel.id)]['counting'] > jdatac['RECORD'][str(msg.channel.id)]['counting']:
                        if not jdatac['RECORD'][str(msg.channel.id)]['recorduser'] == 0:
                            try:
                                recorduser = msg.guild.get_member(jdatac['RECORD'][str(msg.channel.id)]['recorduser'])
                            except:
                                pass
                        if not jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] == 0:
                            try:
                                lastuser = msg.guild.get_member(jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'])
                            except:
                                pass
                        if not jdatac['RECORD'][str(msg.channel.id)]['msgid'] == 0:
                            try:
                                msg0 = await msg.channel.fetch_message(jdatac['RECORD'][str(msg.channel.id)]['msgid'])
                                await msg0.unpin()
                            except:
                                pass
                        if not jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] == 0:
                            try:
                                msg1 = await msg.channel.fetch_message(jdatac['CONTINUE'][str(msg.channel.id)]['msgid'])
                                await msg1.pin()
                            except:
                                pass
                        isexist = cd.find_one({
                            "_id": str(lastuser.id)
                        })
                        if isexist:
                            bonus = 10 * jdatac['CONTINUE'][str(msg.channel.id)]['counting']
                            cd.update_one({
                                "_id": str(lastuser.id)
                            },{
                                "$inc":{
                                    "money": bonus
                                }
                            })
                            if not jdatac['RECORD'][str(msg.channel.id)]['recorduser'] == 0:
                                try:
                                    await msg.channel.send(f"{lastuser.mention} 突破了 {recorduser.mention} 的記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                                except:
                                    await msg.channel.send(f"{lastuser.mention} 突破了 {jdatac['RECORD'][str(msg.channel.id)]['recorduser']} 的記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                            else:
                                await msg.channel.send(f"{lastuser.mention} 突破了記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                        else:
                            await msg.channel.send(f"{lastuser.mention} 突破了 {recorduser.mention} 的記錄達到 `{inputnum}` 但是沒有賬戶 無法獲得獎勵")
                        jdatac['RECORD'][str(msg.channel.id)]['recorduser'] = jdatac['CONTINUE'][str(msg.channel.id)]['lastuser']
                        jdatac['RECORD'][str(msg.channel.id)]['counting'] = jdatac['CONTINUE'][str(msg.channel.id)]['counting']
                        jdatac['RECORD'][str(msg.channel.id)]['msgid'] = jdatac['CONTINUE'][str(msg.channel.id)]['msgid']
                    await msg.add_reaction(emoji="❌")
                    jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] = 0
                    jdatac['CONTINUE'][str(msg.channel.id)]['counting'] = 0
                    jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] = 0
            except:
                if jdatac['CONTINUE'][str(msg.channel.id)]['counting'] > jdatac['RECORD'][str(msg.channel.id)]['counting']:
                    if not jdatac['RECORD'][str(msg.channel.id)]['recorduser'] == 0:
                        try:
                            recorduser = msg.guild.get_member(jdatac['RECORD'][str(msg.channel.id)]['recorduser'])
                        except:
                            pass
                    if not jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] == 0:
                        try:
                            lastuser = msg.guild.get_member(jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'])
                        except:
                            pass
                    if not jdatac['RECORD'][str(msg.channel.id)]['msgid'] == 0:
                        try:
                            msg0 = await msg.channel.fetch_message(jdatac['RECORD'][str(msg.channel.id)]['msgid'])
                            await msg0.unpin()
                        except:
                            pass
                    if not jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] == 0:
                        try:
                            msg1 = await msg.channel.fetch_message(jdatac['CONTINUE'][str(msg.channel.id)]['msgid'])
                            await msg1.pin()
                        except:
                            pass
                    isexist = cd.find_one({
                        "_id": str(lastuser.id)
                    })
                    if isexist:
                        bonus = 10 * jdatac['CONTINUE'][str(msg.channel.id)]['counting']
                        cd.update_one({
                            "_id": str(lastuser.id)
                        },{
                            "$inc":{
                                "money": bonus
                            }
                        })
                        if not jdatac['RECORD'][str(msg.channel.id)]['recorduser'] == 0:
                            try:
                                await msg.channel.send(f"{lastuser.mention} 突破了 {recorduser.mention} 的記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                            except:
                                await msg.channel.send(f"{lastuser.mention} 突破了 {jdatac['RECORD'][str(msg.channel.id)]['recorduser']} 的記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                        else:
                            await msg.channel.send(f"{lastuser.mention} 突破了記錄達到 `{jdatac['CONTINUE'][str(msg.channel.id)]['counting']}` 獲得 `{bonus}PT` 作為獎勵")
                    else:
                        await msg.channel.send(f"{lastuser.mention} 突破了 {recorduser.mention} 的記錄達到 `{inputnum}` 但是沒有賬戶 無法獲得獎勵")
                    jdatac['RECORD'][str(msg.channel.id)]['recorduser'] = jdatac['CONTINUE'][str(msg.channel.id)]['lastuser']
                    jdatac['RECORD'][str(msg.channel.id)]['counting'] = jdatac['CONTINUE'][str(msg.channel.id)]['counting']
                    jdatac['RECORD'][str(msg.channel.id)]['msgid'] = jdatac['CONTINUE'][str(msg.channel.id)]['msgid']
                await msg.add_reaction(emoji="❌")
                jdatac['CONTINUE'][str(msg.channel.id)]['lastuser'] = 0
                jdatac['CONTINUE'][str(msg.channel.id)]['counting'] = 0
                jdatac['CONTINUE'][str(msg.channel.id)]['msgid'] = 0
            with open('./counting.json', 'w', encoding = 'utf8') as jfilec:
                json.dump(jdatac, jfilec)
        else:
            pass
        
def setup(bot):
    bot.add_cog(Counting(bot))