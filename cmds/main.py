import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import asyncio

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
        with open('./data.json', 'r', encoding='utf8') as jfiled:
            jdatad = json.load(jfiled)
        with open('./counting.json', 'r', encoding = 'utf8') as jfilec:
            jdatac = json.load(jfilec)
        await ctx.message.delete()
        if ctx.channel.id in jdatad['gamecmdchannel']:
            await ctx.send(f"```ini\n[{self.bot.command_prefix}rps] 剪刀、石頭、布：\n\n1. 玩一次  [1000PT]\n2. 玩家第一次連勝獲得 [0.65 * 1000PT]\n3. 第二次連勝開始將獲得 [((1.3 ^ 當前連勝數) - 1) * 1000PT]\n4. 其中星期六以及星期日\n    玩家第一次連勝獲得 [0.65 * 1.5 * 1000PT]\n    第二次連勝開始將獲得 [((1.3 ^ 當前連勝數 * 1.5) - 1) * 1000PT]\n5. 當中晚上八點正到十點會有\n    玩家第一次連勝獲得 [0.65 * 2 * 1000PT]\n    第二次連勝開始將獲得 [((1.3 ^ 當前連勝數 * 2) - 1) * 1000PT]\n6. 平手則支付 [0.28 * 1000PT]\n7. 平手、玩家獲勝，連勝將不會重置\n8. 機器人獲勝則連勝重置\n\n\n[{self.bot.command_prefix}cf] 擲硬幣：\n\n1. 玩一次  [1000PT]\n2. 玩家第一次連勝獲得 [0.7 * 1000PT]\n3. 第二次連勝開始將獲得 [((1.4 ^ 當前連勝數) - 1) * 1000PT]\n4. 其中星期六以及星期日\n    玩家第一次連勝獲得 [0.7 * 1.5 * 1000PT]\n    第二次連勝開始將獲得 [((1.4 ^ 當前連勝數 * 1.5) - 1) * 1000PT]\n5. 當中晚上八點正到十點會有\n    玩家第一次連勝獲得 [0.7 * 2 * 1000PT]\n    第二次連勝開始將獲得 [((1.4 ^ 當前連勝數 * 2) - 1) * 1000PT]\n6. 沒有平手\n7. 猜對，連勝將不會重置\n8. 猜錯則連勝重置\n```")
        if ctx.channel.id in jdatad['guessnumberchannel']:
            await ctx.send(f"```ini\n[{self.bot.command_prefix}gn] 猜數字：\n\n1. 玩一次 [1500PT]\n2. 一場遊戲最多猜5次/輪\n3. 數字範圍介於1至{jdatad['range']}\n4. 提示將會每十二小時刷新一次\n5. 賬戶餘額必須有至少 [1500PT] 才能在猜中後獲得PT\n6. 沒有賬戶呼賬戶餘額少過 [1500PT] 開始玩遊戲不會有任何的PT增減\n7. 計費遊戲中：\n    猜第1次/輪扣 [100PT]\n    猜第2次/輪扣 [200PT]\n    猜第3次/輪扣 [300PT]\n    猜第4次/輪扣 [400PT]\n    猜第5次/輪扣 [500PT]\n8. 獎勵如下：\n    猜中當下將不會有PT減扣，且會返還本場遊戲中所有減扣的PT\n    第1次/輪猜中獲得 [3000PT]\n    第2次/輪猜中獲得 [2000PT + 100PT = 2100PT]\n    第3次/輪猜中獲得 [1200PT + 300PT = 1500PT]\n    第4次/輪猜中獲得 [600PT + 600PT = 1200PT]\n    第5次/輪猜中獲得 [200PT + 1000PT = 1200PT]\n9. 以上算式皆為 [獎勵 + 回扣 = 獎勵總額]\n    其中星期六以及星期日，當中的獎勵為 [獎勵 * 1.5]\n    當中更會在晚上八點正到十點會有 [獎勵 * 2]\n```")
        if str(ctx.channel.id) in jdatac['CONTINUE'] and str(ctx.channel.id) in jdatac['RECORD']:
            await ctx.send("```fix\n數字接龍：\n\n1. 不需要任何PT就能進行遊戲，但要有賬戶\n2. 從1開始\n3. 接下來的數字不能是自己\n4. 錯了重頭開始\n5. 達到指定數會獲得PT，例：達到100有1000PT\n6. 突破記錄會獲得PT\n```")

    @commands.command(aliases=['sg'])
    async def startgame(self, ctx, args:str=None):
        with open('./data.json', 'r', encoding = 'utf8') as jfiled:
	          jdatad = json.load(jfiled)
        if not checkp(ctx.guild, ctx.author, jdatad['setchannel']) and not ctx.author.id == jdatad['specialallowed']:
            await ctx.send(f"要求 {jdatad['setchannel']} 級權限")
            return
        if not ctx.channel.id == jdatad['mainhall']:
            await ctx.send("請在大廳使用該指令")
            return
        await ctx.message.delete()
        with open('./counting.json', 'r', encoding = 'utf8') as jfile:
            jdata = json.load(jfile)
        await ctx.send("3")
        for c in jdata['CONTINUE']:
            channel = self.bot.get_channel(int(c))
            await channel.send("3")
        await asyncio.sleep(1)
        await ctx.send("2")
        for c in jdata['CONTINUE']:
            channel = self.bot.get_channel(int(c))
            await channel.send("2")
        await asyncio.sleep(1)
        await ctx.send("1")
        for c in jdata['CONTINUE']:
            channel = self.bot.get_channel(int(c))
            await channel.send("1")
        await asyncio.sleep(1)
        await ctx.send("遊戲開始!!!")
        for c in jdata['CONTINUE']:
            channel = self.bot.get_channel(int(c))
            await channel.send("START!!!")
            await channel.set_permissions(ctx.guild.default_role, view_channel=False, manage_channels=False, manage_permissions=False, manage_webhooks=False, create_instant_invite=False, send_messages=True, embed_links=False, attach_files=False, add_reactions=False, use_external_emojis=False, mention_everyone=False, manage_messages=False, read_message_history=True, send_tts_messages=False, use_slash_commands=False)
        await asyncio.sleep(120)
        await ctx.send("時間還有3分鐘")
        await asyncio.sleep(120)
        await ctx.send("時間還有1分鐘")
        await asyncio.sleep(60)
        for c in jdata['CONTINUE']:
            channel = self.bot.get_channel(int(c))
            await channel.send("TIME UP!!!")
            await channel.set_permissions(ctx.guild.default_role, view_channel=False, manage_channels=False, manage_permissions=False, manage_webhooks=False, create_instant_invite=False, send_messages=False, embed_links=False, attach_files=False, add_reactions=False, use_external_emojis=False, mention_everyone=False, manage_messages=False, read_message_history=True, send_tts_messages=False, use_slash_commands=False)
        await ctx.send("遊戲結束!!!")

def setup(bot):
    bot.add_cog(Main(bot))