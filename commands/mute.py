import discord
from discord.ext import commands
from discord.utils import get
import asyncio

async def create_mute_role(guild: discord.Guild):
    role_name = "muted"
    mute_role = get(guild.roles, name=role_name)

    if mute_role is None:
        mute_role = await guild.create_role(name=role_name, permissions=discord.Permissions(send_messages=False, speak=False))

    mute_permissions = discord.PermissionOverwrite(send_messages=False)
    mute_voice_permissions = discord.PermissionOverwrite(speak=False)

    for channel in guild.text_channels:
        await channel.set_permissions(mute_role, overwrite=mute_permissions)
        await asyncio.sleep(0)

    for channel in guild.voice_channels:
        await channel.set_permissions(mute_role, overwrite=mute_voice_permissions)
        await asyncio.sleep(0)

    return mute_role

def convert_to_seconds(time: int, unit: str) -> int:
    unit = unit.lower()
    if unit in ['s', 'sec', 'second', 'seconds']:
        return time
    elif unit in ['m', 'min', 'minute', 'minutes']:
        return time * 60
    elif unit in ['h', 'hour', 'hours']:
        return time * 3600
    elif unit in ['d', 'day', 'days']:
        return time * 86400
    elif unit in ['w', 'week', 'weeks']:
        return time * 604800
    else:
        raise ValueError("Invalid time unit! Use seconds, minutes, hours, days, or weeks.")

@commands.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, time: int = 0, unit: str = "minutes"):
    guild = ctx.guild
    mute_role = await create_mute_role(guild)
    
    if mute_role in member.roles:
        await ctx.send(f"{member.name} is already muted!")
    else:
        await member.add_roles(mute_role)
        await ctx.send(f"{member.name} muted")
        
        if time > 0:
            duration_in_seconds = convert_to_seconds(time, unit)
            await asyncio.sleep(duration_in_seconds)
            await member.remove_roles(mute_role)
            await ctx.send(f"{member.name} unmuted")

# Setup function for loading the command
def setup(bot: commands.Bot):
    bot.add_command(mute)
