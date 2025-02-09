import random
import discord
from datetime import datetime
from discord.ext import commands
from discord.ui import View , Button
import requests
import aiohttp
import time
from better_profanity import profanity
import json
import os
bot = commands.Bot(command_prefix="/", intents = discord.Intents.all())


@bot.event
async def on_ready():
    
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game("/auric"))
    print("Bot is Ready")

    try:
        synced = await bot.tree.sync()
        print(f"Synces {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="insult",description="This Command sends a random insult sentence !")
async def hello(interaction: discord.Interaction,user: str):
    url = "https://evilinsult.com/generate_insult.php?lang=en&type=json&num=" + str(random.randint(0, 999))
    data = requests.get(url)
    json_data = data.json()
    ephemeral=True
    await interaction.response.send_message(f""+user+" "+json_data["insult"],ephemeral=ephemeral)
    
@bot.tree.command(name="counttoday", description="Counts the number of messages sent today in this channel")
async def counttoday(interaction: discord.Interaction):
    await interaction.response.defer()
    
    today = datetime.utcnow().date()
    count = 0
    
    async for message in interaction.channel.history(limit=None):
        if message.created_at.date() == today:
            count += 1
    
    await interaction.followup.send(f"Messages sent today in this channel: {count}")


@bot.tree.command(name="roll",description="This Command rolls a dice !")
async def roll(interaction: discord.Interaction):
    die_face = ["https://cdn.discordapp.com/attachments/1045735310350356490/1085928064300621924/Dice_Face1.png","https://cdn.discordapp.com/attachments/1045735310350356490/1085928064560681071/Dice_Face2.png","https://cdn.discordapp.com/attachments/1045735310350356490/1085928064770392174/Dice_Face3.png","https://cdn.discordapp.com/attachments/1045735310350356490/1085928063268823131/Dice_Face4.png","https://cdn.discordapp.com/attachments/1045735310350356490/1085928063570825266/Dice_Face5.png","https://cdn.discordapp.com/attachments/1045735310350356490/1085928063839256647/Dice_Face6.png"]
    die_num=random.randint(0,5)
    die = die_face[die_num]
    embed = discord.Embed(color=discord.Color.dark_gold())
    embed.set_image(url =die)
    embed.set_author(name = die_num+1)
    await interaction.response.send_message(embed=embed)
    ephemeral=True





@bot.tree.command(name="qr",description="This Command creates QR code !")
async def roll(interaction: discord.Interaction,text:str):
    embed = discord.Embed(color=discord.Color.dark_gold())
    embed.set_image(url="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+text)
    await interaction.response.send_message(embed = embed)
    ephemeral=True





@bot.tree.command(name="ban",description="Bans a user")
@commands.has_permissions(ban_members=True)
async def ban(interaction:discord.Interaction, member: discord.Member, reason:str):
    await member.ban(reason=reason)
    await interaction.response.send_message(f'{member} has been banned. Reason: {reason}')





# Kick command
@bot.tree.command(name="kick",description="Kicks a member")
@commands.has_permissions(kick_members=True)
async def kick(interaction:discord.Interaction, member: discord.Member, reason:str):
    await member.kick(reason=reason)
    await interaction.response.send_message(f'{member} has been kicked. Reason: {reason}')





# Mute command
@bot.tree.command(name="mute",description="This Command sends a random insult sentence !")
@commands.has_permissions(manage_roles=True)
async def mute(interaction:discord.Interaction, member: discord.Member, duration: int, reason:str):
    role = discord.utils.get(interaction.guild.roles, name='Muted')
    await member.add_roles(role)
    await interaction.response.send_message(f'{member} has been muted for {duration} minutes. Reason: {reason}')
    await time.sleep(duration*60)
    await member.remove_roles(role)
    await interaction.response.send_message(f'{member} has been unmuted after {duration} minutes.')





# Unmute command
@bot.tree.command(name="unmute",description="This Command sends a random insult sentence !")
@commands.has_permissions(manage_roles=True)
async def unmute(interaction:discord.Interaction, member: discord.Member):
    role = discord.utils.get(interaction.guild.roles, name='Muted')
    await member.remove_roles(role)
    await interaction.response.send_message(f'{member} has been unmuted.')





# Warn command
@bot.tree.command(name="warn",description="This Command sends a random insult sentence !")
@commands.has_permissions(kick_members=True)
async def warn(interaction:discord.Interaction, member: discord.Member, *,  reason:str):
    await interaction.response.send_message(f'{member.mention}, you have been warned for ```{reason}```')




# Purge command
@bot.tree.command(name="purge",description="This Command sends a random insult sentence !")
@commands.has_permissions(manage_messages=True)
async def purge(interaction:discord.Interaction, amount: int):
    await interaction.response.send_message(f'Wait')
    time.sleep(2)
    await interaction.channel.purge(limit=amount+1)
    await interaction.channel.send(f'{amount} messages have been deleted.',delete_after=2)





# Lockdown command
@bot.tree.command(name="lock",description="This Command sends a random insult sentence !")
@commands.has_permissions(manage_channels=True)
async def lockdown(interaction:discord.Interaction, *,  reason:str):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message(f'{interaction.channel.mention} has been locked down. Reason: {reason}')





# Unlock command
@bot.tree.command(name="unlock",description="This Command sends a random insult sentence !")
@commands.has_permissions(manage_channels=True)
async def unlock(interaction:discord.Interaction,*,reason:str):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message(f'{interaction.channel.mention} has been unlocked. Reason: {reason}')





# Tempban command
@bot.tree.command(name="tempban",description="This Command sends a random insult sentence !")
@commands.has_permissions(ban_members=True)
async def tempban(interaction:discord.Interaction, member: discord.Member, duration: int, reason:str):
    await member.ban(reason=reason)
    await interaction.response.send_message(f'{member} has been temporarily banned for {duration} minutes. Reason: {reason}')
    await time.sleep(duration*60)
    await member.unban(reason=reason)
    await interaction.send(f'{member} has been unbanned after {duration} minutes.')





# Unban command
@bot.tree.command(name="unban",description="This Command sends a random insult sentence !")
@commands.has_permissions(ban_members=True)
async def unban(interaction:discord.Interaction, user: discord.User, reason:str):
    await interaction.guild.unban(user, reason=reason)
    await interaction.response.send_message(f'{user} has been unbanned. Reason: {reason}')





@bot.tree.command(name="meme",description="This command sends a random meme from the internet !")
async def hello(interaction: discord.Interaction,cateogory:str):
    embed = discord.Embed(color=discord.Color.dark_gold())
    meme_url = "https://meme-api.com/gimme/"+cateogory
    mdata = requests.get(meme_url)
    json_data = mdata.json()
    name= json_data["title"]
    like =json_data["ups"]
    meme = json_data["url"]
    embed.set_author(name = name)
    embed.set_footer(text =f"{like} people liked this meme")
    embed.set_image(url =meme)
    await interaction.response.send_message(embed = embed)
    ephemeral=True



abuseive = ["Caught in 4K","Aw hell nah man :skull:","Just Why?"," :warning: Innappropriate message :warning:",":warning: :warning: :warning: :warning: :warning: :warning:","Not Today","FBI, stop right there","Hold UP!"]
foot=["No naughty naughty !","You ok bro?","Don't do it","Just don't do it","Why Abuse?","I don't have words for you","I see you","NOPE!"]

abuse = True






@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    msg = message.content
    author = str(message.author) + " "
    if profanity.contains_profanity(msg):

        embed = discord.Embed(color=discord.Color.dark_gold(),
                            title=random.choice(abuseive),
                            description=author + "Was caught sending inappropriate message " + "(" + msg + ")")
        embed.set_footer(text=random.choice(foot))
        await message.channel.send(embed=embed)
        await message.delete()



async def set_slowmode(self, ctx, duration: int):
  """
  This function sets slowmode for a channel.

  Args:
      ctx (discord.Interaction): The interaction object.
      duration (int): The duration of slowmode in seconds.
  """
  if duration < 0 or duration > 21600:  # Enforce limits (0-6 hours)
    await ctx.response.send_message("Slowmode duration must be between 0 and 6 hours.")
    return

  try:
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=duration)
    await ctx.response.send_message(f"Slowmode has been set to {duration} seconds in this channel.")
  except discord.HTTPException as e:
    await ctx.response.send_message(f"Failed to set slowmode: {e}")

async def anti_raid(self, member):
  """
  This function checks for potential raids based on certain criteria.

  Args:
      member (discord.Member): The member object.
  """
  # Define raid criteria (adjust these values as needed)
  new_member_threshold = 5  # Minimum number of new members in a short time
  time_threshold = 60  # Time window (in seconds) to consider new members

  # Get members who joined within the time window
  new_members = [m for m in member.guild.members if (member.joined_at - m.joined_at).total_seconds() <= time_threshold]
  new_member_count = len(new_members)

  if new_member_count >= new_member_threshold:
    # Potential raid detected! Take action (e.g., kick, mute, log)
    print(f"Potential raid detected! {new_member_count} new members joined within {time_threshold} seconds.")
    await member.kick(reason="Potential raid member")
    # You can also add logic to mute the member, send an alert to moderators, etc.

# Add these functions to your bot class

# @bot.tree.command(name="slowmode", description="Sets slowmode for a channel")
# @commands.has_permissions(manage_channels=True)
# async def slowmode(self, interaction: discord.Interaction, duration: int):
#   await self.set_slowmode(interaction, duration)

# # (Optional) Add an event listener for member join events
# @bot.event
# async def on_member_join(self, member):
#   await self.anti_raid(member)

@bot.tree.command(name="senddm", description="Send a DM to a user")
# @bot.tree.describe(user="The user to send a DM to", message="The message to send")
async def senddm(interaction: discord.Interaction, user: discord.User, title: str, description: str):
    try:
        embed = discord.Embed(title=title, description=description, color=0xf5c310)
        embed.set_author(name=" Sent by", url="https://twitter.com/RealDrewData", icon_url="https://pbs.twimg.com/profile_images/1327036716226646017/ZuaMDdtm_400x400.jpg")
        embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")

        embed.add_field(name="Field 1 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False)
        embed.add_field(name="Field 2 Title", value="It is inline with Field 3", inline=True)
        embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)

        embed.set_footer(text="This is the footer. It contains text at the bottom of the embed")
        await user.send(embed=embed)
        await interaction.response.send_message(f"DM with embed sent to {user.name}", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I cannot send a DM to this user.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
        
@bot.tree.command(name="countmessages", description="Counts the number of messages in the current channel")
async def count_messages(interaction: discord.Interaction):
    await interaction.response.defer()
    channel = interaction.channel
    message_count = 0
    
    async for _ in channel.history(limit=None):
        message_count += 1
    
    await interaction.followup.send(f'There are {message_count} messages in this channel.', ephemeral=True)
bot.run(os.environ['TOKEN'])
