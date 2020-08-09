import discord
from discord.ext import commands
import youtube_dl
import random
import datetime
import pytz
from pytz import timezone

bot = commands.Bot(command_prefix='&')

#Hello! Welcome to my uh, kind of wonky code, to be honest. I'm uploading this for the 2020 Hack Instead hackathon, as a representative of Star Beam, a team consisting of just me.
#When it gets into your hands, you can do whatever you want with it!

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f'{bot.command_prefix}help'))
    print("The bot is ready!")

@bot.command()
async def coin(ctx):
    """Flips a coin."""
    outcome = ["heads", "tails"]
    await ctx.send(f"Landed on **{random.choice(outcome)}**.")

@bot.command()
async def roleinfo(ctx, *, name = ""):
    """Gets a role's info."""
    if name:
        try:
            role = ctx.message.role_mentions[0]
        except IndexError:
            role = ctx.author.guild.get_role(name)
        if not role:
            role = discord.utils.find(lambda m: m.name == name, ctx.guild.roles)
        if not role:
            role = ctx.author.roles[1]
            await ctx.send(f"Couldn't find role! Pulling up {role.names}'s roleinfo.")
    else:
        role = ctx.author.roles[1]
    
    coolzone = timezone("US/Eastern")
    uncoolzone = timezone('UTC')

    vuncooltime = role.created_at
    uncooltime = uncoolzone.localize(vuncooltime)
    cooltime = uncooltime.astimezone(coolzone)

    firstlist = role.members
    secondlist = ""
    for name in firstlist:
        secondlist += str(name)
        secondlist += ", "

    secondlist = secondlist[:-2]

    colour = role.colour
    colourString = str(colour)
    if colourString == "#000000":
        colour = 0x99aab5
        colourString = "#99aab5"
        
    coolembed = discord.Embed(color=colour, timestamp=ctx.message.created_at)
    coolembed.set_author(name=f"{bot.command_prefix}roleinfo")
    coolembed.set_footer(text=f"Developed by Star Beam", icon_url=bot.user.avatar_url)
    coolembed.set_thumbnail(url=bot.user.avatar_url)

    coolembed.add_field(name="Name", value=role.name, inline=False)
    coolembed.add_field(name="ID", value=role.id)
    coolembed.add_field(name="Colour", value=colourString)
    coolembed.add_field(name="Members", value=secondlist, inline=False)
    coolembed.add_field(name="Created", value=cooltime.strftime("%a, %#d %B %Y, %H:%M %Z"))
    
    await ctx.send(embed=coolembed)

@bot.command()
async def roles(ctx):
    """Gets the server's roles."""
    coolserver = ctx.author.guild
    firstRolelist = coolserver.roles
    secondRolelist = ""
    for name in firstRolelist:
        secondRolelist += str(name)
        secondRolelist += ", "

    secondRolelist = secondRolelist[:-2]
    await ctx.send(f"Role List:\n```{secondRolelist}```\nTo learn more, use the roleinfo command!")

@bot.command()
async def rps(ctx, args):
    """Rock, paper, or scissors?"""
    if args == "r" or args == "rock":
        uinput = 1
    elif args == "p" or args == "paper":
        uinput = 2
    elif args == "s" or args == "scissors" or args == "scissor":
        uinput = 3
    else:
        uinput = 0
    outcome = ["rock", "paper", "scissors"]
    output = random.choice(outcome)
    if (uinput == 1 and output == "rock") or (uinput == 2 and output == "paper") or (uinput == 3 and output == "scissors"):
        msg = "I tied."
    elif (uinput == 1 and output == "paper") or (uinput == 2 and output == "scissors") or (uinput == 3 and output == "rock"):
        msg = "I won!"
    elif (uinput == 1 and output == "scissors") or (uinput == 2 and output == "rock") or (uinput == 3 and output == "paper"):
        msg = "I lost..."
    else:
        msg = "I don't think you inputted anything... Try again?"
    await ctx.send(f"You played {args}. I played **{output}**. {msg}")

@bot.command()
async def say(ctx, *args):
    """Repeats your message."""
    output = ''
    for word in args:
        output += word
        output += ' '
    await ctx.send(output)

@bot.command()
async def servericon(ctx, *, name = ""):
    """Gets the server's icon."""
    await ctx.send(ctx.author.guild.icon_url)
    
@bot.command()
async def serverinfo(ctx):
    """Gets the server's info."""
    coolserver = ctx.author.guild

    coolzone = timezone("US/Eastern")
    uncoolzone = timezone('UTC')

    vuncooltime = coolserver.created_at
    uncooltime = uncoolzone.localize(vuncooltime)
    cooltime = uncooltime.astimezone(coolzone)

    coolembed = discord.Embed(color=0x000000, timestamp=ctx.message.created_at)
    coolembed.set_author(name=f"{bot.command_prefix}serverinfo")
    coolembed.set_footer(text=f"Developed by Star Beam", icon_url=bot.user.avatar_url)
    coolembed.set_thumbnail(url=coolserver.icon_url)

    coolembed.add_field(name="Server", value=f"{coolserver.name} ({coolserver.id})")
    coolembed.add_field(name="Members", value=len(coolserver.members))
    coolembed.add_field(name="Server Owner", value=coolserver.owner)
    coolembed.add_field(name="Boost Level", value=coolserver.premium_tier)
    coolembed.add_field(name="Channels", value=f"{len(coolserver.text_channels)} text, {len(coolserver.voice_channels)} voice")
    coolembed.add_field(name="Region", value=coolserver.region)
    coolembed.add_field(name="Creation Date", value=cooltime.strftime("%a, %#d %B %Y, %H:%M %Z"))
    coolembed.add_field(name=f"Roles ({len(coolserver.roles)})", value=f"To see a full list, type {bot.command_prefix}roles!")
    
    
    await ctx.send(embed=coolembed)

@bot.command()
async def usericon(ctx, *, name = ""):
    """Gets a user's icon."""
    if name:
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            member = ctx.guild.get_member_named(name)
        if not member:
            member = discord.utils.find(lambda m: m.name == name, ctx.guild.members)
        if not member:
            member = ctx.author
            await ctx.send(f"Couldn't find user! Pulling up {member.name}'s userinfo.")
    else:
        member = ctx.author

    await ctx.send(member.avatar_url)

@bot.command()
async def userinfo(ctx, *, name = ""):
    """Gets a user's info."""
    if name:
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            member = ctx.guild.get_member_named(name)
        if not member:
            member = discord.utils.find(lambda m: m.name == name, ctx.guild.members)
        if not member:
            member = ctx.author
            await ctx.send(f"Couldn't find user! Pulling up {member.name}'s userinfo.")
    else:
        member = ctx.author

    coolzone = timezone("US/Eastern")
    uncoolzone = timezone('UTC')

    vuncooldiscordtime = member.created_at
    uncooldiscordtime = uncoolzone.localize(vuncooldiscordtime)
    cooldiscordtime = uncooldiscordtime.astimezone(coolzone)

    vuncoolctxtime = member.joined_at
    uncoolctxtime = uncoolzone.localize(vuncoolctxtime)
    coolctxtime = uncoolctxtime.astimezone(coolzone)

    colour = member.colour
    colourString = str(colour)
    if colourString == "#000000":
        colour = 0x99aab5
        colourString = "#99aab5"
        
    coolembed = discord.Embed(color=colour, timestamp=ctx.message.created_at)
    coolembed.set_author(name=f"{bot.command_prefix}userinfo")
    coolembed.set_footer(text=f"Developed by Star Beam", icon_url=bot.user.avatar_url)
    coolembed.set_thumbnail(url=member.avatar_url)

    coolembed.add_field(name="User", value=f"{member.name}#{member.discriminator} ({member.id})", inline=False)
    coolembed.add_field(name="Display Name", value=member.display_name)
    coolembed.add_field(name="Colour", value=colourString)
    coolembed.add_field(name="Presence", value=member.status)
    coolembed.add_field(name="Joined Discord", value=cooldiscordtime.strftime("%a, %#d %B %Y, %H:%M %Z"))
    coolembed.add_field(name=f"Joined {ctx.guild.name}", value=coolctxtime.strftime("%a, %#d %B %Y, %H:%M %Z"))
    
    await ctx.send(embed=coolembed)

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

bot.run(token)
