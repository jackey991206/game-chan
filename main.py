import discord
from discord.ext import commands
import json, os
import keep_alive
import sys

#read setting.json
with open('setting.json', 'r', encoding='utf8') as jfile:
	  jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=jdata['PREFIX'], intents=intents, help_command=None)
isme = int(os.environ['isme'])

#display message when bot online
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(f"指令 {bot.command_prefix}help"))
    print(">> Bot is online <<")
    with open('./setting.json', 'r', encoding = 'utf8') as jfile:
	      jdata = json.load(jfile)
    if jdata['RESTART'] == 1:
        jdata['RESTART'] = 0
        with open('./setting.json', 'w', encoding = 'utf8') as jfile:
            json.dump(jdata, jfile, indent = 1)
        try:
            await bot.get_user(isme).send("重啟完成")
        except:
            pass
    else:
        pass

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("查無指令")
        return
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("請輸入正確參數")
        return
    raise error

@bot.command()
async def load(ctx, extension):
    if not isinstance(ctx.channel, discord.DMChannel) and not ctx.author.id == isme:
        return
    bot.load_extension(f'cmds.{extension}')
    try:
        await ctx.author.send(f'{extension}載入完成')
    except:
        pass

@bot.command()
async def unload(ctx, extension):
    if not isinstance(ctx.channel, discord.DMChannel) and not ctx.author.id == isme:
        return
    bot.unload_extension(f'cmds.{extension}')
    try:
        await ctx.author.send(f'{extension}卸載完成')
    except:
        pass

@bot.command()
async def reload(ctx, extension):
    if not isinstance(ctx.channel, discord.DMChannel) and not ctx.author.id == isme:
        return
    bot.reload_extension(f'cmds.{extension}')
    try:
        await ctx.author.send(f'{extension}重載完成')
    except:
        pass

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@bot.command()
async def restart(ctx):
    if not isinstance(ctx.channel, discord.DMChannel) and not ctx.author.id == isme:
        return
    restart_program()
    try:
        await ctx.author.send("重啟完成")
    except:
        pass

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    keep_alive.keep_alive()
    #run bot
    bot.run(os.environ['TOKEN'])
