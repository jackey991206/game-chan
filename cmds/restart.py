import asyncio
import datetime
import json
from core.classes import Cog_Extension
import os
import sys

isme = int(os.environ['isme'])

hours_added = datetime.timedelta(hours = 8)
    
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

class Restart(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 0

        async def time_task():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                await asyncio.sleep(60)
                now_time = datetime.datetime.now()+hours_added
                now_time = int(now_time.strftime('%H%M'))
                if now_time == 500 and self.counter == 0:
                    self.counter = 1
                    with open('./setting.json', 'r', encoding = 'utf8') as jfile:
                        jdata = json.load(jfile)
                    jdata['RESTART'] = 1
                    with open('./setting.json', 'w', encoding = 'utf8') as jfile:
                        json.dump(jdata, jfile, indent = 1)
                    try:
                        await self.bot.get_user(isme).send("正在重啟...")
                    except:
                        pass
                    restart_program()
                else:
                    self.counter = 0
                    pass
            
        self.bg_task = self.bot.loop.create_task(time_task())

def setup(bot):
    bot.add_cog(Restart(bot))