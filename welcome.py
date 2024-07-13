import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the token from environment variables
BOT_TOKEN = os.getenv('DISCORD_TOKEN_PLUM')

# Custom color for embeds
custom_color = discord.Color.from_rgb(171, 0, 0)

# Intents setup
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.voice_states = True
intents.message_content = True
intents.members = True

# Create bot instance with intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store guild-specific welcome channels
welcome_channels_1 = {}
welcome_channels_2 = {}

# Event listener for when the bot has connected to Discord
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command to set the first welcome channel
@bot.command(name="setWelcOne")
@commands.has_permissions(administrator=True)
async def setwelcome1(ctx, channel: discord.TextChannel):
    welcome_channels_1[ctx.guild.id] = channel.id
    await ctx.send(f'First welcome channel set to {channel.mention}')

# Command to set the second welcome channel
@bot.command(name="setWelcTwo")
@commands.has_permissions(administrator=True)
async def setwelcome2(ctx, channel: discord.TextChannel):
    welcome_channels_2[ctx.guild.id] = channel.id
    await ctx.send(f'Second welcome channel set to {channel.mention}')

# Event listener for when a member joins a guild
@bot.event
async def on_member_join(member):
    channel_id_1 = welcome_channels_1.get(member.guild.id)
    if channel_id_1:
        channel_1 = bot.get_channel(channel_id_1)
        if channel_1:
            embed_1 = discord.Embed(
                title=f"Welcome to the Asylum {member.display_name}!",
                description=f"<a:syringe:1261638351434547240> Please accept the rules in https://discord.com/channels/1201228112374009959/1201301677706334228 to gain access to the server.",
                color=custom_color
            )
            embed_1.set_author(name=member.display_name, icon_url=member.avatar.url)
            embed_1.set_image(url="https://media.discordapp.net/attachments/1207057097926115379/1261630682405277726/SOCIAL_5.gif?ex=6693a8a2&is=66925722&hm=e54f4c354e5731738432915716bef5bb412585f0140f467f769c37b3774d80b4&=")
            await channel_1.send(embed=embed_1)

    channel_id_2 = welcome_channels_2.get(member.guild.id)
    if channel_id_2:
        channel_2 = bot.get_channel(channel_id_2)
        if channel_2:
            embed_2 = discord.Embed(
                title="Welcome to Asylum",
                description=f"Inpatient {member.mention} has been processed",
                color=custom_color
            )
            embed_2.set_author(name=member.display_name, icon_url=member.avatar.url)
            embed_2.set_thumbnail(url=member.avatar.url)
            embed_2.add_field(name="Welcome them warmly!", value="Make sure to say hi!", inline=True)
            await channel_2.send(embed=embed_2)


# Error handler for missing permissions on setWelcOne command
@setwelcome1.error
async def setwelcome1_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

# Error handler for missing permissions on setWelcTwo command
@setwelcome2.error
async def setwelcome2_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")

# Run the bot with the token
bot.run(BOT_TOKEN)
