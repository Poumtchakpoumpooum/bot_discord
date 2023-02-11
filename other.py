import random
import discord
import asyncio
from discord.ext import commands

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name = 'chatouille')
    async def chatouille_command(self, ctx, member: discord.User):
        await ctx.message.delete()
        embed = discord.Embed(title=f"yo, y'a {ctx.author} qui chatouille {member}")
        embed.set_image(url='https://media.giphy.com/media/3ohuPBnHuElqeTtlkc/giphy.gif')
        for i in range(15):
            await ctx.send(member.mention, embed = embed)
        
    @commands.command(name = 'slap')
    async def slap_command(self, ctx, member: discord.User):
        await ctx.message.delete()
        embed = discord.Embed(title=f"yo, y'a bagarre entre {ctx.author} et {member}")
        embed.set_image(url='https://media.giphy.com/media/Zau0yrl17uzdK/giphy.gif')
        await ctx.send(member.mention, embed = embed)
        
    @commands.command(name= 'giveaway')
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, duration: int, nb_gagnant: int, *, prize: str):
        """permet de faire un giveaway"""
        embed = discord.Embed(title=f"{prize} {nb_gagnant} gagnant(s)",
                            description=f"Hosted by - {ctx.author.mention}\nReact with :tada: to enter!\nTime Remaining: **{duration}** seconds",
                            color=ctx.guild.me.top_role.color, )

        msg = await ctx.channel.send(content="GIVEAWAY", embed=embed)
        await msg.add_reaction("🎉")
        await asyncio.sleep(duration)
        new_msg = await ctx.channel.fetch_message(msg.id)

        user_list = [u for u in await new_msg.reactions[0].users().flatten() if u != self.bot.user] # Check the reactions/don't count the bot reaction

        if len(user_list) == 0:
            await ctx.send("No one reacted.") 
        else:
            for i in range (nb_gagnant):
                try:
                    winner = random.choice(user_list)
                    e = discord.Embed()
                    e.title = "Giveaway ended!"
                    e.description = f"{winner} just won {prize}"
                    await ctx.send(f"{winner.mention}", embed=e)
                    user_list.remove(winner)
                except:
                    pass