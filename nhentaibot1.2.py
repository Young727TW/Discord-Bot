import discord
from discord.ext import commands,tasks
import random
import copy
import requests
import bs4
import json

with open('setting.json', mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot=commands.Bot(command_prefix=".",intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    game = discord.Game("Testing")
    await bot.change_presence(status=discord.Status.idle, activity=game)
##################################################################################################

@bot.command()
async def n(ctx,number=None,page=0):
    c = ctx.channel.is_nsfw()
    if c == False:
        await ctx.send("This is not NSFW channel")
    else:
        if number!=None:
            #爬蟲
            #從內容頁面
            urls = []
            page = 0
            while 1:
                text = f"https://nhentai.net/g/{number}/{page+1}/"
                hentai = requests.get(text)
                #hentai.encoding = 'utf-8'
                data = bs4.BeautifulSoup(hentai.text, "lxml").select("#image-container img")#這行不確定

                urls = ["src"] if not ["src"].startswith("src")

                strTitle = bs4.BeautifulSoup(hentai.text, "lxml").bs4.soup.title.text#這行也不確定
                if ("404" in strTitle) == True:#判斷網頁是否404
                    break
                #urls[page] = f"{data}"
                #if not i["src"].startswith("data")
                page += 1
                #img class=fit-horizontal
                #section id=image-container
            #輸出訊息
            embed=discord.Embed(color=0x009dff,title="Nhentai Viewer",url=text)
            embed.set_footer(text="By Young#0001")
            embed.set_image(url=urls[0])
            message=await ctx.send(embed=embed)
            for i in ["◀","▶"]:
                await message.add_reaction(i)
            #檢查表情符號(函式)
            def check(reaction, user):
                return user == ctx.author and reaction.message == message
            #檢查表情符號(迴圈)
            while 1 :
                if(page + 1 > len(urls) - 1):
                    embed=discord.Embed(color=0x009dff,title="Nhentai Viewer",description="The end.")
                    embed.set_footer(text="By Young#0001")
                    await message.edit(embed=embed)
                    break
                reaction, user = await bot.wait_for("reaction_add",timeout=60.0,check=check)
                if str(reaction) ==  "▶":
                    page+=1
                elif str(reaction) == "◀":
                    page-=1
                await message.remove_reaction(reaction,user)
                embed=discord.Embed(color=0x009dff,title="Nhentai Viewer",url=text)
                embed.set_footer(text="By Young#0001")
                embed.set_image(url=urls[page])
                await message.edit(embed=embed)
        else:
            await ctx.send(f"Please input number")

##################################################################################################
bot.run(jdata['TestBotTOKEN'])