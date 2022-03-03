from http import server
from data import sensitiveData
import discord
from discord.ext import commands
from discord.ui import InputText, Modal
from discord import Embed
import logging  
import json
from json import loads
import os 

#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger("discord")
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename="discord.log",encoding="utf-8",mode="w")
#handler.setFormatter(logging.Formatter("%(asctime)s:%(LevelName)s:%(name)s:%(message)s"))
#logger.addHandler(handler)

# Notas:
# ctx quiere decir el contexto, por ejemplo en  "async def modaltest(ctx):"
# Cuando se llama a modaltest el contexto nos dice informacion sobre como ha sido llamado, por quien, cuando etc
#  channel = ctx.channel.id
#   print(f"{channel}")
# En ese ejemplo imprimo el id del canal por donde ha sido llamado
bot = discord.Bot()
servers = [945803024897564723]


   
token = sensitiveData.Data.token()

class MyModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Mission name", placeholder="Operation Greencoat"))

        self.add_item(
            InputText(
                label="Description",
                placeholder="In this operation we will be performing...",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Your Modal Results", color=discord.Color.random())
        embed.add_field(name="First Input", value=self.children[0].value, inline=False)
        embed.add_field(name="Second Input", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embeds=[embed])


@bot.slash_command(guild_ids = servers, name="test", description = "Testing things out")
async def test(ctx):
  print("Command recieved")
  await ctx.respond(f"I am working, \n\nMy Latency Is: {bot.latency*1000} ms.")


@bot.slash_command(name="currentmembers", guild_ids= servers, description = "Watch Member List")
async def currentmembers(ctx):
    async def parse_embed_json(json_file):
        embdes_json = loads(json_file)["members"]
        for embed_json in embdes_json:
            embed = Embed().from_dict(embed_json)
            yield embed
        with open("members.json", "r") as file:
            temp_ban_embeds = parse_embed_json(file.read())

        for embed in temp_ban_embeds:
            await ctx.send(embed=embed)



@bot.slash_command(name="seemembers", guild_ids= servers, description = "Watch Member List")
async def seemembers(ctx):
    with open("members.json", "r") as json_file:
        
        default = "The list of members is: "
        answer = ""
        answer = answer + default
        
        count = 0
        for line in json_file.readlines():       
            data=json.loads(line)
            for item in data["members"]:
                print(count)
                answer2= data["members"][count]["missions"]
                answer = answer + data["members"][count]["name"] + " = " + answer2 + " | "
                count = count + 1
        await ctx.respond(answer)  
        

@bot.slash_command(name="addmember", guild_ids= servers, description = "Add Member to the List")
async def addmember(ctx, name, missions):
    database = []
    await ctx.respond(int(name) +" " + int(missions))
    
    for i in range(1):
        members = {}
        name = input("name: ")
        missions= input("number: ")
        database.append(members)
    with open("members.json","a") as json_file:
        json.dump(database, json_file)
        print("File saved")




@bot.slash_command(name="createevent", guild_ids= servers)
async def createevent(ctx):
    print("Command recieved")

    class MyView(discord.ui.View):
        @discord.ui.button(label="Start setup", style=discord.ButtonStyle.primary)
        async def button_callback(self, button, interaction):
            modal = MyModal(title="Modal Triggered from Button")
            channel = ctx.channel.id
            print(f"Channel: {channel}")
            await channel.send.send_modal(f"modal")

        @discord.ui.select(
            placeholder="Select the preset",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="First Modal", description="Shows the first modal"),
                discord.SelectOption(label="Second Modal", description="Shows the second modal"),
            ],
        )
        async def select_callback(self, select, interaction):
            modal = MyModal(title="Temporary Title")
            modal.title = select.values[0]
            await interaction.response.send_modal(modal)
            
        add_reactions(ctx)
    view = MyView()
    author = ctx.author
    print(f"Author: {author}")
    await author.send("Select a preset to make the event with", view=view)

def add_reactions(ctx):
  print("Adding reactions")
  channel = ctx.channel.id
  print(f"Channel: {channel}")
  

@bot.event
async def on_message(message):
  print(f"Message from {message.author}: {message.content}")

bot.run(token)
