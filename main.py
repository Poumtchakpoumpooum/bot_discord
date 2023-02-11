from moderation import Moderation
from message import Message
from other import Other
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="config")

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name = 'aide')
    async def help_command(self, ctx):
        """affiche toutes les commandes disponible."""
        embed =  discord.Embed(title="Liste des commandes disponibles", description="")
        commands = []
        for command in self.bot.commands:
            commands.append(f"{self.bot.command_prefix}{command.name}")
        embed.add_field(name="Commandes", value="\n".join(commands),inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()
              
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

if __name__ == '__main__':
    bot.add_cog(Moderation(bot))
    bot.add_cog(Message(bot))
    bot.add_cog(Other(bot))
    bot.add_cog(Help(bot))
    bot.run(os.getenv("TOKEN"))