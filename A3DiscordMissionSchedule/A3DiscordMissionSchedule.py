from ast import For
from http import server
from data import sensitiveData
import discord
from discord.ext import commands
from discord.ui import InputText, Modal
import logging  

# Notas:
# ctx quiere decir el contexto, por ejemplo en  "async def modaltest(ctx):"
# Cuando se llama a modaltest el contexto nos dice informacion sobre como ha sido llamado, por quien, cuando etc
#  channel = ctx.channel.id
#   print(f"{channel}")
# En ese ejemplo imprimo el id del canal por donde ha sido llamado
bot = discord.Bot()
servers = [945803024897564723]
channels = bot.get_all_channels


   
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
        await parseDataEvent(self.children)
        
        


@bot.slash_command(guild_ids = servers, name="test", description = "Testing things out")
async def test(ctx):
  print("Command recieved")
  await ctx.respond(f"I am working \n\nLatency: {bot.latency*1000} ms.")

@bot.slash_command(name="newevent", guild_ids= servers)
async def createevent(ctx):
    print("Command recieved")

    class MyView(discord.ui.View):
        @discord.ui.button(label="Start setup", style=discord.ButtonStyle.primary)
        async def button_callback(self, button, interaction):
            modal = MyModal(title="Modal Triggered from Button")
            channel = ctx.channel.id
            print(f"Channel: {channel}")
            await interaction.response.send_modal(modal)

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
        async def send_event(ctx, entries):
            embed = discord.Embed(title="Your Modal Results", color=discord.Color.random())
            embed.add_field(name="First Input", value=entries[0].value, inline=False)
            embed.add_field(name="Second Input", value=entries[1].value, inline=False)
            print(channels)
            await bot.send('hello')
    view = MyView()
    author = ctx.author
    print(f"Author: {author}")
    await author.send("Select a preset to make the event with", view=view)


     
async def parseDataEvent(entries):
     embed = discord.Embed(title="Your Modal Results", color=discord.Color.random())
     embed.add_field(name="First Input", value=entries[0].value, inline=False)
     embed.add_field(name="Second Input", value=entries[1].value, inline=False)
     print(channels)
     channel = discord.utils.get(bot.get_guild(945803024897564723).channels, name='general')
     message = await channel.send(embed=embed)   
     message_id = message.id


def add_reactions(ctx):
  print("Adding reactions")
  channel = ctx.channel.id
  print(f"Channel: {channel}")
  

@bot.event
async def on_message(message):
  print(f"Message from {message.author}: {message.content}")

bot.run(token)
