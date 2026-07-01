import discord
from discord.ext import commands
import datetime
from discord import app_commands

TOKEN = "Enter your bot token here"

#perms
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# replace ei with other name if you want but have to change the name in the code below too(thats alot of work ngl)
ei = commands.Bot(command_prefix = '!', intents = intents)

#channels/id
leave_channel = None
role_channel = None
logs_channel = None
My_id = None #needed for the ticketing bot to send embed to your dms or replace it with a channel id ig

#Status
@ei.event
async def on_ready():
    print("Ei is online!")
    activity = discord.Activity(
    type=discord.ActivityType.playing,
    name="With Sura"
)
    await ei.change_presence(
        status=discord.Status.online,
        activity=activity
    )
    await ei.tree.sync()
    print("Synced slash commands!")

#embed fixer
@ei.event
async def on_message(message):
    if message.author == ei.user:
        return
    
    link_found = message.content.lower()

    if "https://www.instagram.com/reel" in link_found:

        await message.channel.send(
            f"Hey {message.author.mention}, please use 'kk' before instagram to view the reel in Discord itself! <:nerd:1515707085310922883>\n"
            f"It should look like: `https://www.kkinstagram.com/reel/example`"
        )
        
    await ei.process_commands(message)

#purge
@ei.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, count: int):
    await ctx.channel.purge(limit = count +1)

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send(f"You don't have perms {ctx.author.mention} <:pants:1515707092009484469>")

#list
@ei.command()
async def elscmd(ctx):
    await ctx.channel.send(f"Here are my commands {ctx.author.mention}\n[1] `Embed fix notifer` Notifies users when they post normal reels link, so use Embed in it\n[2] `!purge` To delete certain number of text in chat\n[3] `Member Left` To log when a member leaves\n[4] `Self roles` Assigns members roles upon reaction\n[5] `Edited message logs`Records any edited message\n[6] `Ticketing`Used to forward compaints to staff or owner on use\n[7] `Slash Ban` to ban members\n[8] `Slash timeout` to timeout members <:akwa:1515708453740609656>")

#idhu leave ana message anupa
@ei.event
async def on_member_remove(member):
    channel = ei.get_channel(leave_channel)

    embed = discord.Embed(title = "Member left!", color = discord.Color.red())
    embed.add_field(name = "Member", value = member.mention, inline = True)
    embed.add_field(name = "Date Left", value = datetime.datetime.utcnow().strftime("%b %d, %Y"), inline = True)
    
    #time in server ku idhu
    duration = datetime.datetime.utcnow() - member.joined_at.replace(tzinfo = None)
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    embed.add_field(name = "Time spent in server", value = f"{duration.days}d {hours}h {minutes}m")
    embed.set_thumbnail(url = member.display_avatar.url)
    await channel.send(embed = embed)

#auto roles ku embed
@ei.command()
@commands.has_permissions(manage_messages = True)
async def role(ctx):
    await ctx.channel.send("Please choose creator roles here!:")
    embed = discord.Embed(
        title = "Assign yourself roles!",
        description = "Please react to exact roles below to get that specific role!\n[1] <@&1515645430904520875> = 🎨\n[2] <@&1515645457924362361> = ✍️\n[3] <@&1515645509350592522> = 🎮\n[4] <@&1515645623733325824> = 🎬",
        color = discord.Color.purple()
    )
    message1 = await ctx.send(embed = embed)
    await message1.add_reaction("🎨")
    await message1.add_reaction("✍️")
    await message1.add_reaction("🎮")
    await message1.add_reaction("🎬")
    
    #2nd 
    await ctx.channel.send("Please choose age roles here!:")
    embed2 = discord.Embed(
        title = "Assign yourself roles!",
        description = "Please react to exact roles below to get that specific role!\n[1] <@&1515645872044507258> = ⛓️‍💥\n[2] <@&1515645911848456263> = 🪅",
        color = discord.Color.green()
    )
    message2 = await ctx.send(embed = embed2)
    await message2.add_reaction("⛓️‍💥")
    await message2.add_reaction("🪅")

    #3rd
    await ctx.channel.send("Please choose color roles here!:")
    embed3 = discord.Embed(
        title = "Assign yourself roles!",
        description = "Please react to exact roles below to get that specific role!\n[1] <@&1519014314881712149> = 1️⃣\n[2] <@&1519014600530727122> = 2️⃣\n[3] <@&1519014393495552141> = 3️⃣\n[4] <@&1519014442522902558> = 4️⃣\n[5] <@&1519014368795168900> = 5️⃣\n[6] <@&1519022474635771975> = 6️⃣\n[7] <@&1519014345382825984> = 7️⃣\n[8] <@&1519014416333410475> = 8️⃣\n[9] <@&1519014706239635697> = 9️⃣",
        color = discord.Color.green()
    )
    message3 = await ctx.send(embed = embed3)
    await message3.add_reaction("1️⃣")
    await message3.add_reaction("2️⃣")
    await message3.add_reaction("3️⃣")
    await message3.add_reaction("4️⃣")
    await message3.add_reaction("5️⃣")
    await message3.add_reaction("6️⃣")
    await message3.add_reaction("7️⃣")
    await message3.add_reaction("8️⃣")
    await message3.add_reaction("9️⃣")

#auto roles add ku
@ei.event
async def on_raw_reaction_add(payload):
    reaction_roles = {
        "🎨": 1515645430904520875,
        "✍️": 1515645457924362361,
        "🎮": 1515645509350592522,
        "🎬": 1515645623733325824,
        "⛓️‍💥": 1515645872044507258,
        "🪅": 1515645911848456263,
        "1️⃣": 1519014314881712149,
        "2️⃣": 1519014600530727122,
        "3️⃣": 1519014393495552141,
        "4️⃣": 1519014442522902558,
        "5️⃣": 1519014368795168900,
        "6️⃣": 1519022474635771975,
        "7️⃣": 1519014345382825984,
        "8️⃣": 1519014416333410475,
        "9️⃣": 1519014706239635697,
    }

    if str(payload.emoji) in reaction_roles:
        guild = ei.get_guild(payload.guild_id)
        role_id = reaction_roles[str(payload.emoji)]
        role = guild.get_role(role_id)

        member = guild.get_member(payload.user_id)
        await member.add_roles(role)
#role eduka
@ei.event
async def on_raw_reaction_remove(payload):
    reaction_roles = {
        "🎨": 1515645430904520875,
        "✍️": 1515645457924362361,
        "🎮": 1515645509350592522,
        "🎬": 1515645623733325824,
        "⛓️‍💥": 1515645872044507258,
        "🪅": 1515645911848456263,
        "1️⃣": 1519014314881712149,
        "2️⃣": 1519014600530727122,
        "3️⃣": 1519014393495552141,
        "4️⃣": 1519014442522902558,
        "5️⃣": 1519014368795168900,
        "6️⃣": 1519022474635771975,
        "7️⃣": 1519014345382825984,
        "8️⃣": 1519014416333410475,
        "9️⃣": 1519014706239635697,
    }

    if str(payload.emoji) in reaction_roles:
        guild = ei.get_guild(payload.guild_id)
        role_id = reaction_roles[str(payload.emoji)]
        role = guild.get_role(role_id)

        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)
    
#edit message logs ku
@ei.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if before.content == after.content:
        return
    channel = ei.get_channel(logs_channel)
    embed = discord.Embed(title = "Message Edited", color = discord.Color.purple())
    embed.add_field(name = "Message sent by: ", value = before.author.mention)
    embed.add_field(name = "Original message: ", value = before.content, inline = False)
    embed.add_field(name = "Edited message: ",value = after.content, inline = False)
    await channel.send(embed = embed)

#Modal for ticket
class TicketModal(discord.ui.Modal, title = "Submit a Complaint"):
    complaint = discord.ui.TextInput(
        label = "Your complaint",
        style = discord.TextStyle.long,
        placeholder = "Type your complaint here...",
        required = True
    )
    async def on_submit(self, interaction: discord.Interaction):
        user = await ei.fetch_user(My_id)
        await user.send(f"New complaint from {interaction.user.mention}:\n{self.complaint.value}")
        await interaction.response.send_message("Your complaint has been sent!", ephemeral = True)

#complaint embed
class TicketView(discord.ui.View):
    @discord.ui.select(placeholder = "Select an option", options =[
        discord.SelectOption(label = "Submit a Complaint", description = "Will be sent to staff or owner")
    ])
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(TicketModal())
        await interaction.message.edit(view=TicketView())
        def __init__(self):
            super().__init__(timeout=None)

#slash anupa
@ei.tree.command(name = "ticket", description = "Submit a complaint")
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(title = "Please use the drop down menu below to send a complaint",
                          description = "Use it only if the issue needs quick action or is serious! (Don't abuse it as joke)",
                          color = discord.Color.blue())
    await interaction.response.send_message(embed = embed, view = TicketView(), ephemeral = False)

#slash timeout ku
@ei.tree.command(name = "timeout", description = "To timeout a member")
@app_commands.checks.has_permissions(moderate_members = True)
@app_commands.describe(member = "Target", minutes = "How many minutes")
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int):
    await member.timeout(datetime.timedelta(minutes = minutes))
    await interaction.response.send_message(f"{member.mention} is in timeout for {minutes} minute(s)")

#slash ban ku
@ei.tree.command(name = "ban", description = "To ban a member")
@app_commands.checks.has_permissions(ban_members = True)
@app_commands.describe(member = "Target", reason = "State your reason")
async def ban_members(interaction: discord.Interaction, member: discord.Member, reason: str):
    await member.ban(reason = reason)
    await interaction.response.send_message(f"{member.mention} has been banned for {reason}")

    #logs ku
    channel = ei.get_channel(logs_channel)
    embed = discord.Embed(title = "Member banned", color = discord.Color.orange)
    embed.add_field(name = "Member: ", value = member.mention, inline = True)
    embed.add_field(name = "Reason: ", value = reason)
    embed.set_thumbnail(url = member.display_avatar.url)
    await channel.send(embed = embed)


ei.run(TOKEN, reconnect = True)
