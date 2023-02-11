import discord
from discord.ext import commands

class Message (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        """signale quand le bot est opérationnel"""
        print("Le bot est prêt.")
        role = discord.utils.get(self.bot.guilds[0].roles, name="Muted")
        if role is None:
            role = await self.bot.guilds[0].create_role(name="Muted")
            permissions = role.permissions
            permissions.update(send_messages=False)
            
    @commands.command(name = 'clear')
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
           
    @commands.command(name = 'say')
    async def say_command(self, ctx, message: str):
        await ctx.channel.send(message)
        await ctx.message.delete()
        
    @commands.command(name = 'mp')
    async def send_mp(self, ctx, user: discord.User,  message: str):
        """envoyer un message privée à une personne ciblé."""
        private_channel = await user.create_dm()
        await private_channel.send(message)
        await ctx.message.delete()
        
    @commands.command(name = 'mp_all')
    @commands.has_permissions(administrator=True)
    async def send_mp_all(self, ctx,  message: str):
        """envoyé un message privée à toutes les personness du serveur"""
        for member in ctx.guild.members:
            if member.bot != True:
                private_channel = await member._user.create_dm()
                await private_channel.send(message)
        await ctx.message.delete()
        
    @commands.command(name='createChat')
    async def create_chat(self, ctx,*, name_chat =  None):
        """commande de création d'un nouveau salon avec pour nom le prénom de l'utilisateur par défaut
        ou le nom entré"""
        guild = ctx.guild
        if name_chat != None:
            name = name_chat
        else:
            name = ctx.author.display_name + "'s Chat"
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        new_channel = await guild.create_text_channel(name, overwrites=overwrites)
        await ctx.send(f'Canal de discussion créé: {new_channel.mention}')  
        await ctx.message.delete()
        
    @commands.command(name='createVocal')
    async def create_vocal(self, ctx,*, name_vocal = None):
        guild = ctx.guild
        if name_vocal != None:
            name = name_vocal
        else:
            name = ctx.author.display_name + "'s chat"
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        new_channel = await guild.create_voice_channel(name, overwrites=overwrites)
        await ctx.send(f'Canal vocal créé: {new_channel.mention}')  
        await ctx.message.delete()
    
    @commands.command(name='invite')
    @commands.has_permissions(manage_channels=True)
    async def invite_to_vocal(self, ctx, member: discord.Member):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if channel:
                invite = await channel.create_invite(max_uses=1, unique=True)
                embed = discord.Embed(title=f"Invitation to join {channel.name}", description=invite.url)
                await member.send(embed=embed)
                await ctx.send(f'Invitation envoyée à {member.mention}')
            else:
                await ctx.send("Vous n'êtes pas connecté à un canal vocal.") 
        elif ctx.author.text:
            channel = ctx.author.text.channel
            if channel:
                invite = await channel.create_invite(max_uses=1, unique=True)
                embed = discord.Embed(title=f"Invitation to join {channel.name}", description=invite.url)
                await member.send(embed=embed)
                await ctx.send(f'Invitation envoyée à {member.mention}')
            else:
                await ctx.send("Vous n'êtes pas connecté à un chat.")  
        else:
            await ctx.send("Vous n'êtes pas connecté à un canal.")