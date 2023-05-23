import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import time
from discord.ext.commands import has_permissions, MissingPermissions
from discord.embeds import Embed
from pymongo import MongoClient
import datetime
import random
cl = MongoClient("mongodb+srv://skrrtlasagna:squidgy72@cluster0.0vkkzww.mongodb.net/?retryWrites=true&w=majority")
db = cl["pochita"]
coll = db["guilds"]
pics = ["https://media.tenor.com/hW43u6bpnRMAAAAi/capoo-bugcat.gif",
    "https://sportshub.cbsistatic.com/i/2022/10/19/dda81ef8-bc50-44a5-8157-a3e689530e6d/chainsaw-man-pochita.jpg?width=1200",
    "https://preview.redd.it/1pqe5upt8k591.jpg?auto=webp&s=489e5db77eb87455159a79619e2f6aefabf2f6e2",
    "https://static.boredpanda.com/blog/wp-content/uploads/2016/09/cats-toothless-lookalikes-fb.png",
    "https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/46/Begging_Tame_Wolf.png/revision/latest/scale-to-width-down/640?cb=20201021020322"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=";",
                   intents=intents, case_insensitive=True, help_command=None)

async def open(id, author):
    r = coll.find_one({"_id":id})
    if r == None:
        post = {"_id": id,
        "blacklist": []
        }
        coll.insert_one(post)
    try:
        if r[f"{author.id}"]:
            pass
    except:
        coll.update_one({"_id":id},{"$set":{
            f"{author.id}": {
                "name": f"{author.name}'s pet",
                "level": 0,
                "hearts": 0,
                "hunger": 10,
                "fun": 10,
                "energy": 10,
                "health": 100,
                "last_interaction": int(time.time()),
                "gen": 1,
                "bday": str(datetime.datetime.now().strftime("%m/%d/%Y")),
                "poop": False,
                "image": random.choice(pics),
                "death": 1,
                "revives": 0,
                "dabloons": 0,
                "streak": 0,
                "lax": False
                    }
                }
            }
        )

async def petembed(author):
    s = coll.find_one({"_id":author.guild.id})
    r = s[str(author.id)]
    t = r["hunger"] + r["fun"] + r["energy"]
    if r["health"] <= 0:
        mood = "Dead\n(Use /newpet to get\na new one or /revive it)"
        embed = discord.Embed(
        title=r["name"]+" 💀",
        color=discord.Color.from_rgb(255,255,255)
    )
        embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"])+" • Died "+str(r["death"]))
    else:
        if r["poop"] == True:
            mood = "Dirty"
            embed = discord.Embed(
        title=r["name"],
        color=discord.Color.from_rgb(64,44,8)
    )
        elif r["health"] <= 20:
            mood = "Dying"
            embed = discord.Embed(
        title=r["name"],
        color=discord.Color.from_rgb(100,0,0)
    )
        elif r["health"] <= 50:
            mood = "Sick"
            embed = discord.Embed(
        title=r["name"],
        color=discord.Color.from_rgb(0,100,0)
    )
        elif r["hunger"] >= 80 and r["fun"] >= 80 and r["energy"] >= 80:
            mood = "Loved"
            embed = discord.Embed(
        title=r["name"],
        color=discord.Color.from_rgb(255,200,255)
    )
        elif r["hunger"] >= 50 and r["fun"] >= 50 and r["energy"] >= 50:
            mood = "Content"
            embed = discord.Embed(
        title=r["name"],
        color=discord.Color.from_rgb(60,200,50)
    )
        elif t < 250 and t >= 150:
            mood = "Sad"
            embed = discord.Embed(
        title=r["name"],
        color=discord.Color.from_rgb(80,100,130)
    )
        elif t < 150 and t >= 60:
            mood = "Depressed"
            embed = discord.Embed(
        title=r["name"],
        color=discord.Color.from_rgb(200,200,200)
    )
        else:
            mood = "Neglected"
            embed = discord.Embed(
        title=r["name"],
        color=discord.Color.from_rgb(100,100,100)
    )
        embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"]))
    embed.set_image(url=r["image"])
    embed.add_field(name="Level", value=f"`{r['level']}`", inline=True)
    embed.add_field(
        name="Hearts", value=f"`{str(r['hearts'])}` <:pixelheart:877255391472398407>", inline=True)
    embed.add_field(name="Mood", value=f"`{mood}`", inline=True)
    embed.add_field(name="Hunger 🍖", value=f"`{str(r['hunger'])}/100`", inline=True)
    embed.add_field(name="Fun 🎮", value=f"`{str(r['fun'])}/100`", inline=True)
    embed.add_field(name="Energy 💤", value=f"`{str(r['energy'])}/100`", inline=True)
    embed.add_field(name="Health", value=f"`{str(r['health'])}/100`", inline=True)
    embed.add_field(name="\u200b", value=f"\u200b", inline=True)
    embed.add_field(name="Streak", value=f"**{str(r['streak'])} days**", inline=True)
    return embed

async def checkstreak(last_interaction, author):
    day = datetime.datetime.fromtimestamp(last_interaction)
    todays = int(datetime.datetime.today().strftime("%j"))
    if todays - int(day.strftime("%j")) == 1 or 364 < int(day.strftime("%j")) + todays < 367:
        coll.update_one({"_id":author.guild.id}, {"$inc":{f"{author.id}.streak":1}})
        return True
    elif todays - int(day.strftime("%j")) > 1:
        coll.update_one({"_id":author.guild.id}, {"$set":{f"{author.id}.streak":0}})
        return False
    else:
        return True

async def levelup(hearts, level):
    if level > 0:
        if hearts % 50 == 0:
            newlevel = hearts/50
        else:
            newlevel = level
    else:
        if hearts == 10:
            newlevel = 1
        else:
            newlevel = level
    return int(newlevel)

class Actions(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author

        # random (not) stat
        self.rnf = [" picks at its food and promptly walks away",
        " doesn't want to eat right now",
        " stares at you"]
        self.rnp = [" throws the game controller at you",
        " doesn't want to play with you",
        " says you're boring",
        " stares at you"]
        self.rnc = [ " runs away from you",
        " doesn't want to cuddle you",
        " isn't sleepy",
        " is wide awake"]
        self.rf = [ " enjoys a feast you've prepared",
        " wolfs down a slice of pizza",
        " eats the food you prepared with gratitude",
        " slurps the noodles",
        " licks the plate clean"]
        self.rp = [ " plays Minecraft with you",
        " goes bowling with you",
        " hits the gym",
        " paints rocks with you",
        " picks flowers with you",
        " plays Hypixel bedwars with you",
        " tickles you"]
        self.rc = [ " kicks you in their sleep",
        " drifts sound asleep in your embrace",
        " snores the entire time",
        " cuddles you",
        " sleeps calmly beside you"]
        self.ra = [" received a terrible spanking",
        " was burned with a lighter 🔥",
        " was flogged by a whip",
        " cries out in pain",
        " bleeds out slowly 🩸",
        " was beat up by you",
        " writhes in pain",
        " was slit by a razor blade"
        ]


    @discord.ui.button(label="Feed", style=discord.ButtonStyle.green, emoji="🍖", custom_id="hunger",)
    async def feed(self, button, interaction):
        levelmsg = ""
        poopmsg = ""
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(content="This isn't your pet!", ephemeral=True)
        else:
            r = coll.find_one({"_id":self.author.guild.id})[str(self.author.id)]
            if r["hunger"] + 10 > 100:
                button.disabled = True
                await interaction.response.send_message(content=r["name"]+random.choice(self.rnf), ephemeral=True)
            else:
                # adds 20 hunger
                coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.hunger":20, f"{self.author.id}.hearts":1}})
                if r["hunger"] + 20 > 100:
                    coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.hunger":100}})
                s = coll.find_one({"_id":self.author.guild.id})
                r = s[str(self.author.id)]
                streak = r["streak"]
                streakmsg = ""
                x = await checkstreak(r["last_interaction"], self.author)
                if x == False and streak != 0:
                    streakmsg = f"{self.author.mention} you lost your streak of **{streak}** days!"
                coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.last_interaction":int(time.time())}})
                level = await levelup(r["hearts"], r["level"])
                if level != r["level"]:
                    levelmsg = f"**{r['name']} has leveled up to Level {level}**"
                    coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.level":level}})
                if r["poop"] == False and r["hunger"] > 70:
                    lolz = random.randint(0, 4)
                    if lolz == 0:
                        coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.poop":True}})
                        poopmsg = f"**{r['name']} has pooped...**"
                    elif lolz == 4:
                        if r["lax"] == True:
                            c = random.randint(1, 2)
                            coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.dabloons":c}})
                            coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.poop":True}})
                            poopmsg = f"**Wow! {r['name']} has pooped out {c} <:dabloon:1054183679766843422>**"
                embed = await petembed(self.author)
                embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"])+f"\n{r['name']}{random.choice(self.rf)}")
                await interaction.response.edit_message(embed=embed, view=self)
                try:
                    await interaction.channel.send(content=f"{poopmsg}"+f"\n{levelmsg}"+f"\n{streakmsg}")
                except:
                    pass
                if r["hunger"] > 90:
                    if random.randint(0, 4) == 1:
                        c = random.randint(1, 5)
                        coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.dabloons":c}})
                        await interaction.channel.send(content=f"{r['name']} found **{c}** <:dabloon:1054183679766843422>")
                if r["hunger"] == 100:
                    button.disabled = True
    
    @discord.ui.button(label="Play", style=discord.ButtonStyle.red, emoji="🎮", custom_id="fun")
    async def play(self, button, interaction):
        levelmsg = ""
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(content="This isn't your pet!", ephemeral=True)
        else:
            s = coll.find_one({"_id":self.author.guild.id})
            r = s[str(self.author.id)]
            if r["fun"] + 10 > 100:
                button.disabled = True
                await interaction.response.send_message(content=r["name"]+random.choice(self.rnp), ephemeral=True)
            else:
                # adds 20 fun
                coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.fun":20, f"{self.author.id}.hearts":1}})
                if r["fun"] + 20 > 100:
                    coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.fun":100}})
                s = coll.find_one({"_id":self.author.guild.id})
                r = s[str(self.author.id)]
                streak = r["streak"]
                streakmsg = ""
                x = await checkstreak(r["last_interaction"], self.author)
                if x == False:
                    streakmsg = f"{self.author.mention} you lost your streak of **{streak}** days!"
                coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.last_interaction":int(time.time())}})
                level = await levelup(r["hearts"], r["level"])
                if level != r["level"]:
                    levelmsg = f"**{r['name']} has leveled up to Level {level}**"
                    coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.level":level}})
                embed = await petembed(self.author)
                embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"])+f"\n{r['name']}{random.choice(self.rp)}")
                await interaction.response.edit_message(embed=embed, view=self)
                try:
                    await interaction.channel.send(content=f"{levelmsg}"+f"\n{streakmsg}")
                except:
                    pass
                if r["fun"] > 90:
                    if random.randint(0, 4) == 1:
                        c = random.randint(1, 5)
                        coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.dabloons":c}})
                        await interaction.channel.send(content=f"{r['name']} found **{c}** <:dabloon:1054183679766843422>")
                if r["fun"] == 100:
                    button.disabled = True
    
    @discord.ui.button(label="Cuddle", style=discord.ButtonStyle.blurple, emoji="💤", custom_id="energy")
    async def cuddle(self, button, interaction):
        levelmsg = ""
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(content="This isn't your pet!", ephemeral=True)
        else:
            s = coll.find_one({"_id":self.author.guild.id})
            r = s[str(self.author.id)]
            if r["energy"] + 10 > 100:
                button.disabled = True
                await interaction.response.send_message(content=r["name"]+random.choice(self.rnc), ephemeral=True, delete_after=2)
            else:
                # adds 20 energy
                coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.energy":20, f"{self.author.id}.hearts":1}})
                if r["energy"] + 20 > 100:
                    coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.energy":100}})
                s = coll.find_one({"_id":self.author.guild.id})
                r = s[str(self.author.id)]
                streak = r["streak"]
                streakmsg = ""
                x = await checkstreak(r["last_interaction"], self.author)
                if x == False:
                    streakmsg = f"{self.author.mention} you lost your streak of **{streak}** days!"
                coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.last_interaction":int(time.time())}})
                level = await levelup(r["hearts"], r["level"])
                if level != r["level"]:
                    levelmsg = f"**{r['name']} has leveled up to Level {level}**"
                    coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.level":level}})
                embed = await petembed(self.author)
                embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"])+f"\n{r['name']}{random.choice(self.rc)}")
                await interaction.response.edit_message(embed=embed, view=self)
                try:
                    await interaction.channel.send(content=f"{levelmsg}"+f"\n{streakmsg}")
                except:
                    pass
                if r["energy"] > 90:
                    if random.randint(0, 4) == 1:
                        c = random.randint(1, 5)
                        coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.dabloons":c}})
                        await interaction.channel.send(content=f"{r['name']} found **{c}** <:dabloon:1054183679766843422>")
                if r["energy"] == 100:
                    button.disabled = True

    @discord.ui.button(label="Clean", style=discord.ButtonStyle.grey, emoji="🧻")
    async def clean(self, button, interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(content="This isn't your pet!", ephemeral=True)
        else:
            levelmsg = ""
            r = coll.find_one({"_id":self.author.guild.id})[str(self.author.id)]
            if r["poop"]:
                coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.hearts":2}})
                r = coll.find_one({"_id":self.author.guild.id})[str(self.author.id)]
                coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.poop":False}})
                streak = r["streak"]
                streakmsg = ""
                x = await checkstreak(r["last_interaction"], self.author)
                if x == False:
                    streakmsg = f"{self.author.mention} you lost your streak of **{streak}** days!"
                coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.last_interaction":int(time.time())}})
                level = await levelup(r["hearts"], r["level"])
                if level != r["level"]:
                    levelmsg = f"**{r['name']} has leveled up to Level {level}**"
                    coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.level":level}})
                embed = await petembed(self.author)
                await interaction.response.edit_message(embed=embed, view=self)
                await interaction.channel.send(content=f"{r['name']} feels clean and happy!"+f"\n{levelmsg}"+f"\n{streakmsg}")
                
            else:
                await interaction.response.send_message(content=r["name"]+" is not dirty", ephemeral=True)

    @discord.ui.button(label="Abuse", style=discord.ButtonStyle.red, emoji="🥊")
    async def abuse(self, button, interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(content="This isn't your pet!", ephemeral=True)
        else:
            guild = self.author.guild.id
            hp = random.randint(1, 5)
            coll.update_one({"_id":guild}, {"$inc":{f"{self.author.id}.health":-hp}})
            r = coll.find_one({"_id":guild})[str(self.author.id)]
            if r["health"] <= 0:
                button.disabled = True
                coll.update_one({"_id":guild}, {"$set":{f"{self.author.id}.health":0}})
                coll.update_one({"_id":guild}, {"$set":{f"{self.author.id}.death":str(datetime.datetime.now().strftime("%m/%d/%Y"))}})
                embed = await petembed(self.author)
                message = await interaction.channel.fetch_message(interaction.message.id)
                await message.edit(embed=embed)
                await interaction.response.send_message(content="It's dead 💀", ephemeral=True)
            else:
                embed = await petembed(self.author)
                embed.color = discord.Color.from_rgb(200,0,0)
                embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"])+f"\n{r['name']}{random.choice(self.ra)}")
                await interaction.response.edit_message(embed=embed, view=self)
                
class Revive(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def yes(self, button, interaction):
        coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.revives":-1}})
        r = coll.find_one({"_id":self.author.guild.id})[str(self.author.id)]
        coll.update_one({"_id":self.author.guild.id},{"$set":{
                f"{self.author.id}": {
                    "name": r["name"],
                    "level": r["level"],
                    "hearts": r["hearts"],
                    "hunger": 10,
                    "fun": 10,
                    "energy": 10,
                    "health": 100,
                    "last_interaction": int(time.time()),
                    "gen": r["gen"],
                    "bday": r["bday"],
                    "poop": False,
                    "image": r["image"],
                    "death": 1,
                    "revives": r["revives"],
                    "dabloons": r["dabloons"],
                    "streak": 0,
                    "lax": r["lax"]
                        }
                    }
                }
            )
        await interaction.response.send_message(f"{self.author.mention} Your pet has been revived and you now have **{r['revives']}** revives")
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def no(self, button, interaction):
        await interaction.response.send_message("Canceled")

@bot.slash_command(description="Revive your pet when it dies or see how many revives you have")
async def revive(ctx):
    r = coll.find_one({"_id":ctx.guild.id})[str(ctx.author.id)]
    if r["revives"] == 0:
        await ctx.respond("You don't have any revives, you can buy them at the `/shop`")
    else:
        view = Revive(ctx.author)
        if r["health"] == 0:
            await ctx.respond(f"You have **{r['revives']}** revives and will use **1** revive to save your pet", view=view)
        else:
            await ctx.respond(f"You have **{r['revives']}** revives")
@bot.slash_command(description="Get a new pet after it dies")
async def newpet(ctx):
    try:
        r = coll.find_one({"_id":ctx.guild.id})[str(ctx.author.id)]
        if r["health"] <= 0:
            coll.update_one({"_id":ctx.guild.id},{"$set":{
                f"{ctx.author.id}": {
                    "name": f"{ctx.author.name}'s pet",
                    "level": 0,
                    "hearts": 0,
                    "hunger": 10,
                    "fun": 10,
                    "energy": 10,
                    "health": 100,
                    "last_interaction": int(time.time()),
                    "gen": r["gen"]+1,
                    "bday": str(datetime.datetime.now().strftime("%m/%d/%Y")),
                    "poop": False,
                    "image": random.choice(pics),
                    "death": 1,
                    "revives": r["revives"],
                    "dabloons": r["dabloons"],
                    "streak": 0,
                    "lax": False
                        }
                    }
                }
            )
            await ctx.respond("You bring home a new pet and swear you won't neglect it")
        else:
            await ctx.respond("But your pet isn't dead :fearful:", ephemeral = True)
    except:
        await ctx.respond("Use /pet instead")
@bot.slash_command(description="View yours or someone else's pet")
async def pet(ctx, user: discord.Option(discord.Member, "View someone else's pet", required=False)):
    author = ctx.author
    guild = ctx.guild
    if user:
        try:
            r = coll.find_one({"_id":guild.id})
            if r[f"{user.id}"]: #checks if person even has a pet
                z = coll.find({"_id":guild.id}, {"blacklist":user.id}) #checks if they're blacklisted
                i = False
                for x in z:
                    if str(user.id) in str(x):
                        i = True
                if i and user.id == author.id:
                    await ctx.respond("You are blacklisted from using /pet, contact server staff", ephemeral=True)
                elif i:
                    r = coll.find_one({"_id":guild.id})[str(user.id)]
                    if r["health"] <= 0:
                        embed = discord.Embed(
                        title=r["name"]+" 💀",
                        color=discord.Color.from_rgb(255,255,255)
                    )
                        embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"])+" • Died "+str(r["death"]))
                    else:
                        embed = discord.Embed(
                        title=r["name"]
                    )
                        embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"]))
                        embed.set_image(url=r["image"])
                        embed.add_field(name="Level", value=f"`{r['level']}`", inline=True)
                        embed.add_field(
                            name="Hearts", value=f"`{str(r['hearts'])}` <:pixelheart:877255391472398407>", inline=True)
                        embed.add_field(name="Streak", value=f"**{str(r['streak'])} days**", inline=True)
                    await ctx.respond(content="This user is blacklisted", embed=embed, ephemeral=True)
                else:
                    r = coll.find_one({"_id":guild.id})[str(user.id)]
                    if r["health"] <= 0:
                        embed = discord.Embed(
                        title=r["name"]+" 💀",
                        color=discord.Color.from_rgb(255,255,255)
                    )
                        embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"])+" • Died "+str(r["death"]))
                    else:
                        embed = discord.Embed(
                        title=r["name"]
                    )
                        embed.set_footer(text="Gen "+str(r["gen"])+" • Birthday " +str(r["bday"]))
                        embed.set_image(url=r["image"])
                        embed.add_field(name="Level", value=f"`{r['level']}`", inline=True)
                        embed.add_field(
                            name="Hearts", value=f"`{str(r['hearts'])}` <:pixelheart:877255391472398407>", inline=True)
                        embed.add_field(name="Streak", value=f"**{str(r['streak'])} days**", inline=True)
                    await ctx.respond(embed=embed)
        except:
            await ctx.respond("Tell them to get a pet first", ephemeral=True)
            
    else:
        view = Actions(ctx.author)
        await open(ctx.guild.id, author)
        z = coll.find({"_id":guild.id}, {"blacklist":author.id})
        i = False
        streakmsg = ""
        for x in z:
            if str(author.id) in str(x):
                i = True
        if i:
            await ctx.respond("You are blacklisted from using /pet, contact server staff", ephemeral=True)
        else:
            r = coll.find_one({"_id":guild.id})[str(author.id)]
            if r["health"] > 0:
                stats = ["hunger", "fun", "energy"]
                last = r["last_interaction"]
                streak = r["streak"]
                x = await checkstreak(r["last_interaction"], ctx.author)
                if x == False:
                    streakmsg = f"{ctx.author.mention} you lost your streak of **{streak}** days!"
                ct = int(time.time())
                seconds = (ct - last)
                minutes = int(seconds / 60)
                for stat in stats:
                    if minutes >= 240: # longer than 4 hours, dies slower
                        randec = random.uniform(0.761, 0.781)
                        decay = int(minutes ** randec)
                    else: # else, basically subtracts 1 stat in a minute
                        randec = random.uniform(0.27, 0.30)
                        decay = int(minutes * randec)
                    # decays stat by fraction of the minutes since the last interaction
                    coll.update_one({"_id":guild.id}, {"$inc":{f"{author.id}.{stat}":-decay}})
                    # decay each stat
                    coll.update_one({"_id":guild.id}, {"$set":{f"{author.id}.last_interaction":ct}})
                    r = coll.find_one({"_id":guild.id})[str(author.id)]
                    if r[stat] < 0:
                        coll.update_one({"_id":guild.id}, {"$inc":{f"{author.id}.health":int(r[stat] / 10)}})
                        # if a stat is less than 0, take 10% of the negative number and add it to health
                        coll.update_one({"_id":guild.id}, {"$set":{f"{author.id}.{stat}":0}})
                        # also set stat to 0 again
                        r = coll.find_one({"_id":guild.id})[str(author.id)]
                    elif r[stat] >= 50 and r["health"] < 100:
                        #regenerate
                        fifty = r[stat] - 50
                        if r["poop"] == True:
                            pass
                        else:
                            calc = (int(time.time())-last)//60
                            coll.update_one({"_id":guild.id}, {"$inc":{f"{author.id}.health":calc}})
                            r = coll.find_one({"_id":guild.id})[str(author.id)]
                            if r["health"] > 100:
                                coll.update_one({"_id":guild.id}, {"$set":{f"{author.id}.health":100}})
                            r = coll.find_one({"_id":guild.id})[str(author.id)]
                    else:
                        pass
                    
                if r["health"] <= 0:
                    coll.update_one({"_id":guild.id}, {"$set":{f"{author.id}.health":0}})
                    coll.update_one({"_id":guild.id}, {"$set":{f"{author.id}.death":str(datetime.datetime.now().strftime("%m/%d/%Y"))}})
                    embed = await petembed(author)
                    await ctx.respond(embed=embed)
                else: #if it is alive
                    embed = await petembed(author)
                    await ctx.respond(embed=embed, view=view)
                    if ((ct-last)//3600) >= 1:
                        await ctx.send(f"{ctx.author.mention} {r['name']} missed you while you were gone for **{(ct-last)//3600}** hours!")
            else:
                embed = await petembed(author)
                await ctx.respond(embed=embed)
                await ctx.channel.send(streakmsg)


@bot.slash_command(description="Set a pet image")
async def setimage(ctx, url : discord.Option(input_type=str, description="Image url")):
    r = coll.find_one({"_id":ctx.guild.id})
    try:
        if url.startswith("http"):
            if r[f"{ctx.author.id}"]:
                coll.update_one({"_id":ctx.guild.id}, {"$set":{f"{ctx.author.id}.image":url}})
                await ctx.respond("New pet image set!", ephemeral=True)
        else:
            await ctx.respond("This isn't a valid image url", ephemeral=True)
    except Exception as e:
        print(e)
        await ctx.respond("You don't have a pet. Run `/pet`", ephemeral=True)

@bot.slash_command(description="Set a pet name")
async def rename(ctx, name : discord.Option(input_type=str, max_length=30, description="Rename your pet")):
    if ".gg" in name or ".com" in name or "gg/" in name:
        await ctx.respond("Do not add links", ephemeral=True)
    elif "<@" in name:
        await ctx.respond("Do not @ people")
    else:
        r = coll.find_one({"_id":ctx.guild.id})
        try:
            if r[f"{ctx.author.id}"]:
                coll.update_one({"_id":ctx.guild.id}, {"$set":{f"{ctx.author.id}.name":name}})
                await ctx.respond("New pet name set!", ephemeral=True)
        except:
            await ctx.respond("You don't have a pet. Run `/pet`", ephemeral=True)

class Support(discord.ui.View):
    def __init__(self):
        super().__init__()
        s = discord.ui.Button(label="Support", style=discord.ButtonStyle.link, url="https://discord.gg/zkm4Qr5zQH")
        self.add_item(s)

@bot.slash_command(description="Check how many dabloons you have")
async def balance(ctx):
    r = coll.find_one({"_id":ctx.guild.id})[str(ctx.author.id)]
    await ctx.respond(f"You have **{r['dabloons']}** <:dabloon:1054183679766843422>")

@bot.slash_command(description="Mod command to blacklist someone from using /pet")
async def blacklist(ctx, user: discord.Option(discord.Member)):
    if ctx.author.guild_permissions.manage_messages:
        if user.top_role >= ctx.author.top_role:
            await ctx.respond("You can't do that they are a higher or same role as you", ephemeral=True)
        else:
            try:
                coll.update_one({"_id":ctx.guild.id}, {"$addToSet":{"blacklist":user.id}})
                await ctx.respond(f"Blacklisted {user.name}#{user.discriminator} from using /pet")
            except Exception as e:
                print(e)
    else:
        await ctx.respond("You don't have `Manage Message` perms", ephemeral=True)

@bot.slash_command(description="Mod command to unblacklist someone from using /pet")
async def unblacklist(ctx, user: discord.Option(discord.Member)):
    if ctx.author.guild_permissions.manage_messages:
        if user.top_role >= ctx.author.top_role:
            await ctx.respond("You can't do that they are a higher or same role as you", ephemeral=True)
        else:
            try:
                coll.update_one({"_id":ctx.guild.id}, {"$pull":{"blacklist":user.id}})
                await ctx.respond(f"Unblacklisted {user.name}#{user.discriminator} from using /pet")
            except Exception as e:
                print(e)
    else:
        await ctx.respond("You don't have `Manage Message` perms", ephemeral=True)

class Shop(discord.ui.View):
    def __init__(self, author, embed):
        super().__init__()
        self.view = self
        self.author = author
        self.embed = embed
    @discord.ui.select(placeholder="Choose something to buy",
                         min_values=1, max_values=1, options=[
                            discord.SelectOption(
                                 label="Revive", emoji="❤️"),
                             discord.SelectOption(
                                 label="Laxative", emoji="💩")
                         ])
    async def sel(self, select, interaction):
        if self.children[0].values[0]:
            await interaction.response.defer()
    @discord.ui.button(label="Buy", style=discord.ButtonStyle.green)
    async def buy(self, button, interaction):
        await open(self.author.guild.id, self.author)
        try:
            if self.view.children[0].values[0] == "Laxative":
                r = coll.find_one({"_id":self.author.guild.id})[str(self.author.id)]
                if r["lax"] == True:
                    await interaction.response.send_message(content="Your pet already has this..", ephemeral=True)
                else:
                    (m, val) = self.checkbuy("Laxative", 25)
                    if val:
                        coll.update_one({"_id":self.author.guild.id}, {"$set":{f"{self.author.id}.lax":True}})
                        await interaction.response.send_message(content=m+" and your pet can now poop dabloons")
                    else:
                        await interaction.response.send_message(content=m, ephemeral=True)
            elif self.view.children[0].values[0] == "Revive":
                (m, val) = self.checkbuy("Revive", 50)
                if val:
                    coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.revives":1}})
                    r = coll.find_one({"_id":self.author.guild.id})[str(self.author.id)]
                    await interaction.response.send_message(content=m+f" and you now have **{r['revives']}** revives")
                else:
                    await interaction.response.send_message(content=m, ephemeral=True)
        except:
            await interaction.response.send_message(content="Select something to buy lol", ephemeral=True)
    def checkbuy(self, item, cost):
        r = coll.find_one({"_id":self.author.guild.id})[str(self.author.id)]
        if r["dabloons"] >= cost:
            coll.update_one({"_id":self.author.guild.id}, {"$inc":{f"{self.author.id}.dabloons":-cost}})
            return(f"{self.author.mention} You have bought a **{item}** for **{cost}** <:dabloon:1054183679766843422>", True)
        else:
            return(f"You don't have enough dabloons", False)

@bot.slash_command(description="View the shop")
async def shop(ctx):
    embed = discord.Embed(title="Shop", colour=discord.Colour.from_rgb(255,200,75))
    embed.add_field(name="💩 Laxative | **25** <:dabloon:1054183679766843422>",
    value="Permanently allows your pet to occasionally poop dabloons")
    embed.add_field(name="❤️ Revive | **50** <:dabloon:1054183679766843422>",
    value="A one time use revive allowing you to revive your pet if it dies, you can buy multiple")
    view = Shop(ctx.author, embed)
    await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="Support server")
async def support(ctx):
    await ctx.respond("Contact the dev directly, stay updated, test and suggest new features https://discord.gg/zkm4Qr5zQH", ephemeral=True)

@bot.slash_command(description="View commands")
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.from_rgb(255,150,50))
    embed.set_author(name="Help Menu", icon_url=bot.user.avatar.url)
    embed.add_field(name="Pet Commands", value="""
`/pet [@user]` - View your pet or someone else's, creates one if you don't have one
`/rename` - Renames your pet. Max character length is 30
`/setimage` - Sets image of your pet by http image link. Gifs supported
`/newpet` - Get a new pet after it dies
`/revive` - Revive your pet after it dies, preserving its stats
`/balance` - Checks how many dabloons you have
`/shop` - View the shop and buy stuff
`/support` - Support server
`/updates` - See updates
""")
    embed.add_field(name="Mod Commands", value="""
Requires `Manage Messages` permission
`/blacklist @user` - Blocks someone from using /pet if used inappropriately
`/unblacklist @user` - Undoes blacklist
    """)
    view = Support()
    await ctx.respond(embed=embed, view=view)

@bot.slash_command(description="See updates")
async def updates(ctx):
    embed = discord.Embed()
    embed.add_field(name="<t:1671928320>", value="""
`/shop` has been added
Laxatives will give your pet the ability to poop coins sometimes
A revive will revive your pet and preserve all of its stats and set its health back to 100, these are stackable
`/revive` has been added
The number of max random dabloons from raising a stat past 90 has been raised from 3 to 5
Your pets can no longer poop coins, you need to buy the laxatives

Daily streaks will be added soon zzzzz
    """)
    await ctx.respond(embed=embed)

@bot.event
async def on_guild_join(guild):
    await open(guild.id, guild.owner)

@bot.event
async def on_ready():
    print("pochita up!")
    print(len(bot.guilds))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Denji"))
#wvj@=%gohEZ.2q%flE9FdcuFAI1k4?G2

bot.run("ODg2MDQxNjg2ODIyNzYwNDQ5.GNWIUh.QkonCzjmgRpQFLZNr4qmYDrRKmQNNB6669wmdE", reconnect=True)
