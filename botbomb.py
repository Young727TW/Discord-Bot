import discord
from discord.ext import commands, tasks  #這裡是discord.ext
from discord import Guild, channel, guild  #Guild定義在discord底下
import random
import copy
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

global channellist
@bot.event()
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    channellist = [guild.Members] #bot.get_all_channels 
    for i in range (len(channellist)):
        print(channellist[i])

@bot.command()
async def b(ctx,cha,msg):
    for i in range (len(channellist)):
        channel = bot.get_channel(channellist[i])#channel = channellist
        while 1:
            await channel.send("@everyone")
            time.sleep(1)

@bot.command()
@commands.is_owner()
async def reboot(ctx):
    await ctx.send("```\n重啟\n```")
    await bot.close()
@reboot.error
async def rebooterror(ctx, error):
    await ctx.send("錯誤 非bot擁有者")

bot.run("")