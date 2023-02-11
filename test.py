import discord
from discord.ext import commands

client = commands.Bot(" ")

@client.listen("on_message")
@discord.ui.button(label = "comment vas tu")
async def on_message(message: discord.Message):
    await discord.ui.callback(print('hello'))
    await client.send_message('slt')
client.run("MTA3MTQ4Mzk0ODQyNjg2Njc1OA.Gqs4ed.Bnw4yEEYEXYOhJqKF2lNaYr2cut8C_5x0eNmcc")