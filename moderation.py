import nltk
import unidecode
from nltk.corpus import stopwords
nltk.download('stopwords')
import discord
import asyncio
from discord.ext import commands
import humanfriendly
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                
    @commands.Cog.listener()  
    async def on_message(self, message):
        """analyse les mots de chaque message pour les comparé à une liste de mots bannis"""
        words = nltk.word_tokenize(message.content)
        print(words)
        vulgar_words = []
        with open("C:/Users/Hugo/Desktop/code/code avec chatgpt/bot discord/vulgar_words.txt") as f:
            vulgar_words = f.read().splitlines()
        for word in words:
            word = unidecode.unidecode(word)
            word = word.lower()
            if word in vulgar_words:
                await message.delete()
                await message.channel.send("Attention à la vulgarité!! ")

    #@commands.command(name = 'time_out')
    #async def time_out(self, ctx,member: discord.Member, duration):
    
    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(self, ctx):
        channel = ctx.channel
        everyone_perms = discord.PermissionOverwrite(read_messages=True, send_messages=False)
        await channel.set_permissions(channel.guild.default_role, overwrite=everyone_perms)
        await ctx.send("Le canal est verrouillé. Seuls les administrateurs peuvent écrire.")
        
    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx):
        channel = ctx.channel
        everyone_perms = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        await channel.set_permissions(channel.guild.default_role, overwrite=everyone_perms)
        await ctx.send("Le canal est déverrouillé.")
    
        
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """commande pour bannir une personne sans débannage programméé"""
        await ctx.message.delete()
        await member.ban(reason=reason)
        await ctx.send(f'{member} a été banni pour la raison suivante: {reason}')
        
    @commands.command(name='tempban')
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, duration: int, *, reason=None):
        """ban temporaire """
        await ctx.message.delete()
        await member.ban(reason=reason)
        await ctx.send(f'{member} a été banni pendant {duration} secondes pour la raison suivante: {reason} ')
        await asyncio.sleep(duration)
        await member.unban(reason=reason)
        await ctx.send(f'{member} a été débanni')
        
    @commands.command(name = 'timeout')
    async def timeout(self, ctx, member: discord.Member, time=None, reason=None):
        time = humanfriendly.parse_timespan(time)
        await member.timeout(until = discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
        await ctx.send (f"{member} callate un rato anda {time}")