from http import server
import sensitiveData
import discord
from discord.ext import commands
from discord.ui import InputText, Modal
import logging  
import json

member_list = {"Miembro":"juan"}
json1 = json.dumps(member_list, indent = 2)
file = open("members.json", "a")
file.write(json1)
file.close
                    
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
  await ctx.respond(f"I am working \n\nLatency: {bot.latency*1000} ms.")

@bot.slash_command(name="showmembers", guild_ids= servers)
async def showmembers(ctx):
    with open("members.json", "r") as json_file:
        for line in json_file.redlines():
            data=json.loads(line)
            for item in data:
                print(item)

@bot.slash_command(name="createevent", guild_ids= servers)
async def createevent(ctx):
    print("Command recieved")

    class MyView(discord.ui.View):
        @discord.ui.button(label="Start setup", style=discord.ButtonStyle.primary)
        async def button_callback(self, button, interaction):
            modal = MyModal(title="Modal Triggered from Button")
            channel = ctx.channel.id
            print(f"Channel: {channel}")
            await channel.send.send_modal(modal)

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
