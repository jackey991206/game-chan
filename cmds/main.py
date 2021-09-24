import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('./setting.json', 'r', encoding = 'utf8') as jfile:
	  jdata = json.load(jfile)

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

class Main(Cog_Extension):

    @commands.command()
    async def prefix(self, ctx, args:str=None):
        with open('data.json', 'r', encoding='utf8') as jfiled:
            jdatad = json.load(jfiled)
        if not checkp(ctx.guild, ctx.author, jdatad['prefix']):
            await ctx.send(f"要求 {jdatad['prefix']} 級權限")
            return
        if not ctx.channel.id in jdatad['cmdchannel']:
            await ctx.send("請在指定頻道使用此指令")
            return
        if not args:
            await ctx.send("請輸入一個要替換的指令前綴")
            return
        with open('setting.json', 'r', encoding = 'utf8') as jfiles:
            jdatas = json.load(jfiles)
            jdatas['PREFIX'] = args
        with open('setting.json', 'w', encoding = 'utf8') as jfiles:
            json.dump(jdatas, jfiles)
        await ctx.message.delete()
        self.bot.command_prefix = args
        await self.bot.change_presence(activity=discord.Game(f"指令 {self.bot.command_prefix}help"))
        await ctx.send(f"成功將指令前綴改成 {args}")

    @commands.command(aliases=['h'])
    async def help(self, ctx, args:str=None):
        with open('data.json', 'r', encoding='utf8') as jfiled:
            jdatad = json.load(jfiled)
        if not checkp(ctx.guild, ctx.author, jdatad['createvote']):
            await ctx.send(f"要求 {jdatad['createvote']} 級權限")
            return
        await ctx.message.delete()
        await ctx.send(f"```\n[{self.bot.command_prefix}rps]剪刀、石頭、布：\n\n1. 玩一次 1000PT\n2. 玩家第一次連勝獲得 0.65 * 1000PT\n3. 第二次連勝開始將獲得 ((1.3 ^ 當前連勝數) - 1) * 1000PT\n4. 平手則支付 0.28 * 1000PT\n5. 平手、玩家獲勝，連勝將不會重置\n6. 機器人獲勝則連勝重置\n\n\n[{self.bot.command_prefix}cf]擲硬幣：\n\n1. 玩一次 1000PT\n2. 玩家第一次連勝獲得 0.7 * 1000PT\n3. 第二次連勝開始將獲得 ((1.4 ^ 當前連勝數) - 1) * 1000PT\n4. 沒有平手\n5. 猜對，連勝將不會重置\n6. 猜錯則連勝重置\n```")

def setup(bot):
    bot.add_cog(Main(bot))