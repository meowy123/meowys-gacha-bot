import discord
from discord.ext import commands
import random
from discord.ui import Button, View
from discord.ext.commands import CommandOnCooldown
import json
import os  # For file existence check

# Configure your bot
TOKEN = "MTMyMTAyNzU5NDM5NjYzMTA2MA.GKSGz0.Vo3PdvrCVO_DFdoNnANW81RGjPZCRqoq5D4pOc"
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Gacha pool configuration
RARITIES = [
    ("Common", 35),
    ("Uncommon", 30),
    ("Rare", 20),
    ("Epic", 10),
    ("Mythic", 4),
    ("Legendary", 1),
]

RARITY_EMOJIS = {
    "Common": "<:common:1322156037884608532>",
    "Uncommon": "<:uncommon:1322156070021632052>",
    "Rare": "<:rare:1322156099658580060>",
    "Epic": "<:epic:1322156124958363698>",
    "Mythic": "<:mythic:1322156148274761839>",
    "Legendary": "<:legendary:1322156175784939520>",
}

CHARACTERS = {
     "Common": ["Meowy", "Claw", "Lemony", "Tangerine", "Aligned Gray Fork", "Dumpy"],
    "Uncommon": [
        "Zombie Meowy", "Pirate Claw", "Ghost Lemony", "Bomb Tangerine",
        "Bacon", "Cookie", "Milky", "Limey", "Campfire", "Arachnophobia", "Sun"
    ],
    "Rare": [
        "Santa Meowy", "Peppermint Claw", "Reindeer Lemony",
        "Mistletoe Tangerine", "Wizard Bacon", "Oatmeal Rasin Cookie",
        "Mummy Milky", "UFO Limey", "Planty", "Strawberry", "Coconut", "Geary", "Sign Down Right", "Calculator"
    ],
    "Epic": [
        "Christmas Tree Bacon", "Gingerbread Cookie", "Eggnog Milky",
        "Hot Cocoa Limey", "Thorns Planty", "Masked Strawberry",
        "Spider Coconut", "Cobweb Geary", "Gapple", "Elppag", "Alien Tooth", "Cake", "Loud Incorrect Buzzer", "Xeno"
    ],
    "Mythic": [
        "Present Planty", "Stocking Strawberry", "Ornament Coconut",
        "Star Geary", "Martial Arts Logo", "Faze"
    ],
    "Legendary":
    ["Golden Meowy", "Golden Claw", "Golden Lemony", "Golden Tangerine", "Golden Carrot", "Blue Cat", "Nova", "Deathbringer MAL"],
}

CHARACTER_EMOJIS = {
    "Meowy": "<:meowy:1321038752487047178>",
    "Claw": "<:claw:1321039526973542472>",
    "Lemony": "<:lemony:1321038805406453801>",
    "Tangerine": "<:tangerine:1321039562985701447>",
    "Zombie Meowy": "<:zombiemeowy:1321040489738145793>",
    "Pirate Claw": "<:pirateclaw:1321040601394843699>",
    "Ghost Lemony": "<:ghostlemony:1321040538912424028>",
    "Bomb Tangerine": "<:bombtangerine:1321040646840258622>",
    "Bacon": "<:bacon:1321039613728522291>",
    "Cookie": "<:cookie:1321040331159896125>",
    "Milky": "<:milky:1321040399074332754>",
    "Limey": "<:limey:1321040443492012083>",
    "Santa Meowy": "<:santameowy:1321040831163142146>",
    "Peppermint Claw": "<:peppermintclaw:1321040911383269386>",
    "Reindeer Lemony": "<:reindeerlemony:1321040865556303902>",
    "Mistletoe Tangerine": "<:mistletoetangerine:1321040950172323891>",
    "Wizard Bacon": "<:wizardbacon:1321041011983515740>",
    "Oatmeal Rasin Cookie": "<:oatmealrasincookie:1321041055189045328>",
    "Mummy Milky": "<:mummymilky:1321041111015231592>",
    "UFO Limey": "<:ufolimey:1321041147468054570>",
    "Planty": "<:planty:1321040700837593150>",
    "Strawberry": "<:strawberry:1321040732706045963>",
    "Coconut": "<:coconut:1321040765358440488>",
    "Geary": "<:geary:1321040798028136448>",
    "Christmas Tree Bacon": "<:christmasstreebacon:1321041184839172106>",
    "Gingerbread Cookie": "<:gingerbreadcookie:1321041228405542933>",
    "Eggnog Milky": "<:eggnogmilky:1321041293870104576>",
    "Hot Cocoa Limey": "<:hotcocoalimey:1321041338271006780>",
    "Thorns Planty": "<:thornsplanty:1321041382017601597>",
    "Masked Strawberry": "<:maskedstrawberry:1321047255708471347>",
    "Spider Coconut": "<:spidercoconut:1321047305767616583>",
    "Cobweb Geary": "<:cobwebgeary:1321047340387143700>",
    "Present Planty": "<:presentplanty:1321047380396609536>",
    "Stocking Strawberry": "<:stockingstrawberry:1321802579654742079>",
    "Ornament Coconut": "<:ornamentcoconut:1321802758373773383>",
    "Star Geary": "<:stargeary:1321802817970769930>",
    "Golden Meowy": "<:goldenmeowy:1321902559694295081>",
    "Golden Claw": "<:goldenclaw:1321902667001364480>",
    "Golden Lemony": "<:goldenlemony:1321902715466547250>",
    "Golden Tangerine": "<:goldentangerine:1321902769824858223>",
    "Gapple": "<:gapple:1322655583685574696>",
    "Elppag": "<:elppag:1322659898391007333>",
    "Aligned Gray Fork": "<:alignedgrayfork:1322661262374600785>",
    "Alien Tooth": "<:alientooth:1322667369369305158>",
    "Campfire": "<:campfire:1322674560457379931>",
    "Arachnophobia": "<:arachnophobia:1322674572058824846>",
    "Martial Arts Logo": "<:martialartslogo:1322861800936701952>",
    "Cake": "<:cake:1322869349236609065>",
    "Golden Carrot": "<:goldencarrot:1322870340249976865>",
    "Sun": "<:sun:1322876235893837895>",
    "Dumpy": "<:dumpy:1322876246828257360>",
    "Blue Cat": "<:bluecat:1322956027741868102>",
    "Nova": "<:nova:1322958123081797722>",
    "Sign Down Right": "<:signdownright:1322958143495344218>",
    "Calculator": "<:calculator:1322958151494144053>",
    "Loud Incorrect Buzzer": "<:loudincorrectbuzzer:1322958160365097013>",
    "Faze": "<:faze:1322958168678207568>",
    "Xeno": "<:xeno:1322958175099555871>",
    "Deathbringer MAL": "<:deathbringermal:1322958182653493300>"
}

CREATORS = {
    "Meowy": "<:meowy123:1322150120178843710>",
    "Claw": "<:meowy123:1322150120178843710>",
    "Lemony": "<:meowy123:1322150120178843710>",
    "Tangerine": "<:meowy123:1322150120178843710>",
    "Zombie Meowy": "<:meowy123:1322150120178843710>",
    "Pirate Claw": "<:meowy123:1322150120178843710>",
    "Ghost Lemony": "<:meowy123:1322150120178843710>",
    "Bomb Tangerine": "<:meowy123:1322150120178843710>",
    "Bacon": "<:meowy123:1322150120178843710>",
    "Cookie": "<:meowy123:1322150120178843710>",
    "Milky": "<:meowy123:1322150120178843710>",
    "Limey": "<:meowy123:1322150120178843710>",
    "Santa Meowy": "<:meowy123:1322150120178843710>",
    "Peppermint Claw": "<:meowy123:1322150120178843710>",
    "Reindeer Lemony": "<:meowy123:1322150120178843710>",
    "Mistletoe Tangerine": "<:meowy123:1322150120178843710>",
    "Wizard Bacon": "<:meowy123:1322150120178843710>",
    "Oatmeal Rasin Cookie": "<:meowy123:1322150120178843710>",
    "Mummy Milky": "<:meowy123:1322150120178843710>",
    "UFO Limey": "<:meowy123:1322150120178843710>",
    "Planty": "<:meowy123:1322150120178843710>",
    "Strawberry": "<:meowy123:1322150120178843710>",
    "Coconut": "<:meowy123:1322150120178843710>",
    "Geary": "<:meowy123:1322150120178843710>",
    "Christmas Tree Bacon": "<:meowy123:1322150120178843710>",
    "Gingerbread Cookie": "<:meowy123:1322150120178843710>",
    "Eggnog Milky": "<:meowy123:1322150120178843710>",
    "Hot Cocoa Limey": "<:meowy123:1322150120178843710>",
    "Thorns Planty": "<:meowy123:1322150120178843710>",
    "Masked Strawberry": "<:meowy123:1322150120178843710>",
    "Spider Coconut": "<:meowy123:1322150120178843710>",
    "Cobweb Geary": "<:meowy123:1322150120178843710>",
    "Present Planty": "<:meowy123:1322150120178843710>",
    "Stocking Strawberry": "<:meowy123:1322150120178843710>",
    "Ornament Coconut": "<:meowy123:1322150120178843710>",
    "Star Geary": "<:meowy123:1322150120178843710>",
    "Golden Meowy": "<:meowy123:1322150120178843710>",
    "Golden Claw": "<:meowy123:1322150120178843710>",
    "Golden Lemony": "<:meowy123:1322150120178843710>",
    "Golden Tangerine": "<:meowy123:1322150120178843710>",
    "Gapple": "<:yab:1322655551120998400>",
    "Elppag": "<:yab:1322655551120998400>",
    "Aligned Gray Fork": "<:funni_name2763:1322661186575138886>",
    "Alien Tooth": "<:lindaaring:1322667343297646622>",
    "Campfire": "<:yab:1322655551120998400>",
    "Arachnophobia": "<:lindaaring:1322667343297646622>",
    "Martial Arts Logo": "<:jkay:1322861749132591104>",
    "Cake": "<:slippy:1322869335810904114>",
    "Golden Carrot": "<:lindaaring:1322667343297646622>",
    "Sun": "<:jkay:1322861749132591104>",
    "Dumpy": "<:jkay:1322861749132591104>",
    "Blue Cat": "<:meowy123:1322150120178843710>",
    "Nova": "<:jkay:1322861749132591104>",
    "Sign Down Right": "<:jkay:1322861749132591104>",
    "Calculator": "<:jkay:1322861749132591104>",
    "Loud Incorrect Buzzer": "<:jkay:1322861749132591104>",
    "Faze": "<:jkay:1322861749132591104>",
    "Xeno": "<:jkay:1322861749132591104>",
    "Deathbringer MAL": "<:jkay:1322861749132591104>"
}

STAR_REQUIREMENTS = [1, 5, 15, 40, 100]

# Player data storage
player_inventory = {}

# File to store player data
DATA_FILE = "player_data.json"

# Helper function to save player data to a file
def save_player_data():
    with open(DATA_FILE, "w") as f:
        json.dump(player_inventory, f)

# Helper function to load player data from a file
def load_player_data():
    global player_inventory
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            player_inventory = json.load(f)

# Load data on bot startup
load_player_data()

# Helper function to get stars
def get_stars(count):
    stars = 0
    for req in STAR_REQUIREMENTS:
        if count >= req:
            stars += 1
        else:
            break
    return stars

# Helper function to calculate rarity
def draw_rarity():
    total_weight = sum(weight for _, weight in RARITIES)
    roll = random.randint(1, total_weight)
    current = 0
    for rarity, weight in RARITIES:
        current += weight
        if roll <= current:
            return rarity

# !gacha command - Single pull with cooldown
@bot.command(aliases=['g'])
@commands.cooldown(1, 2, commands.BucketType.user)  # Cooldown for !gacha (1 use per 2 seconds)
async def gacha(ctx):
    player = str(ctx.author.id)
    if player not in player_inventory:
        player_inventory[player] = {rarity: {} for rarity, _ in RARITIES}
    rarity = draw_rarity()
    character = random.choice(CHARACTERS[rarity])
    creator_emoji = CREATORS.get(character, "")
    if character not in player_inventory[player][rarity]:
        player_inventory[player][rarity][character] = 0
    player_inventory[player][rarity][character] += 1
    save_player_data()  # Save data after modification
    await ctx.send(
        f"{ctx.author.mention}, you got **{character}** {CHARACTER_EMOJIS[character]} - {RARITY_EMOJIS[rarity]} {creator_emoji} !"
    )
# !gacha5 command - Pulls from the gacha 5 times at once
@bot.command(aliases=['g5'])
@commands.cooldown(1, 10, commands.BucketType.user)  
async def gacha5(ctx):
    player = str(ctx.author.id)
    if player not in player_inventory:
        player_inventory[player] = {rarity: {} for rarity, _ in RARITIES}

    # Collect results from 10 gacha pulls
    pulls = []
    for _ in range(5):
        rarity = draw_rarity()
        character = random.choice(CHARACTERS[rarity])
        creator_emoji = CREATORS.get(character, "")
        if character not in player_inventory[player][rarity]:
            player_inventory[player][rarity][character] = 0
        player_inventory[player][rarity][character] += 1
        pulls.append(f"**{character}** {CHARACTER_EMOJIS[character]} - {RARITY_EMOJIS[rarity]} {creator_emoji}")

    # Save player data after all 5 pulls
    save_player_data()

    # Merge initial message with the pulls
    await ctx.send(f"{ctx.author.mention}, you used the 5x-gacha and you got...\n" + "\n".join(pulls))
    

# Error handling for !gacha
@gacha.error
async def gacha_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, you're using the gacha too fast! Try again in {round(error.retry_after, 1)} seconds.")

# Error handling for !gacha5
@gacha10.error
async def gacha5_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, you're using the 5x-gacha too fast! Try again in {round(error.retry_after, 1)} seconds.")
        
# !inventory command
@bot.command(aliases=['inv'])
async def inventory(ctx):
    player = str(ctx.author.id)
    if player not in player_inventory:
        await ctx.send(
            f"{ctx.author.mention}, you don't have any characters yet, get one using !gacha."
        )
        return

    # Define pages with their corresponding rarity categories
    pages = [
        ["Common", "Uncommon"],  # Page 1: Common and Uncommon
        ["Rare"],  # Page 2: Rare
        ["Epic"],  # Page 3: Epic
        ["Mythic", "Legendary"],  # Page 4: Mythic and Legendary
    ]

    current_page = 0  # Initialize to the first page
    inventory = player_inventory[player]

    # Helper to generate the page content
    def generate_page_content(page):
        rarities = pages[page]
        response = f"# __{ctx.author.mention}'s Inventory (Page {page + 1})__:\n"
        for rarity in rarities:
            response += f"### {RARITY_EMOJIS[rarity]} **{rarity}**:\n"
            for character in CHARACTERS[rarity]:
                if character in inventory[rarity]:
                    count = inventory[rarity][character]
                    stars = get_stars(count)
                    star_emojis = "⭐" * stars
                    next_star = STAR_REQUIREMENTS[min(stars, len(STAR_REQUIREMENTS) - 1)]
                    creator_emoji = CREATORS.get(character, "")
                    response += f"{CHARACTER_EMOJIS[character]} {character} - {creator_emoji} - {star_emojis} {count}/{next_star}\n"
                else:
                    creator_emoji = CREATORS.get(character, "")
                    response += f"{CHARACTER_EMOJIS[character]} {character} - {creator_emoji} - unobtained\n"
        return response

    # Create the initial page and buttons
    page_content = generate_page_content(current_page)
    button_view = View()
    button_view.add_item(
        Button(label="Previous 2 Pages", style=discord.ButtonStyle.secondary, custom_id="prev_2_pages")
    )
    button_view.add_item(
        Button(label="Previous Page", style=discord.ButtonStyle.primary, custom_id="prev_page")
    )
    button_view.add_item(
        Button(label="Next Page", style=discord.ButtonStyle.primary, custom_id="next_page")
    )
    button_view.add_item(
        Button(label="Next 2 Pages", style=discord.ButtonStyle.secondary, custom_id="next_2_pages")
    )

    message = await ctx.send(page_content, view=button_view)

    def check(interaction):
        return (
            interaction.user == ctx.author
            and interaction.data["custom_id"] in ["prev_page", "next_page", "next_2_pages", "prev_2_pages"]
        )

    while True:
        try:
            interaction = await bot.wait_for('interaction', timeout=60.0, check=check)

            if interaction.data["custom_id"] == "prev_page":
                current_page = (current_page - 1) % len(pages)  # Loop to the last page
            elif interaction.data["custom_id"] == "next_page":
                current_page = (current_page + 1) % len(pages)  # Loop to the first page
            elif interaction.data["custom_id"] == "next_2_pages":
                current_page = (current_page + 2) % len(pages)  # Skip 2 pages
            elif interaction.data["custom_id"] == "prev_2_pages":
                current_page = (current_page - 2) % len(pages)  # Go back 2 pages

            # Update the page content
            page_content = generate_page_content(current_page)

            # Edit the message with the new page content
            await interaction.response.edit_message(content=page_content, view=button_view)

        except asyncio.TimeoutError:
            # Disable buttons after timeout
            for item in button_view.children:
                item.disabled = True
            await message.edit(view=button_view)
            break



@bot.command(aliases=['minf'])
async def m_info(ctx):
    # Create buttons with custom labels
    button1 = Button(label="Gacha", custom_id="gacha")
    button2 = Button(label="Inventory", custom_id="inventory")

    # Create a view to hold the buttons
    view = View()
    view.add_item(button1)
    view.add_item(button2)

    # Send the message with multiple lines of text and the buttons
    await ctx.send(
        "# __Meowy's Gacha Bot Info__:\n\n"
        "How can I help you with?\n\n"
        "Choose an option below:", 
        view=view  # Add the view to the message
    )

    async def gacha_callback(interaction):
        # Edit the message and remove the buttons
        await interaction.response.edit_message(
            content=(
                "# __Meowy's Gacha Bot Info - Gacha__:\n\n"
                "Here's how an example of how the !gacha command shows up:\n\n"
                "[Mention], you got **Meowy** <:meowy:1321038752487047178> - <:common:1322156037884608532> <:meowy123:1322150120178843710>!\n\n"
                "## The gacha message includes:\n"
                "- [Mention] | The Mention - here, the person who initiated the command will be mentioned,\n"
                "- **Meowy** | The Character - this is the character received,\n"
                "- <:meowy:1321038752487047178> | The Character's Emoji - this is the character's emoji that represents them,\n"
                "- <:common:1322156037884608532> | The Rarity - this is the character's rarity, which can be Common <:common:1322156037884608532>, "
                "Uncommon <:uncommon:1322156070021632052>, Rare <:rare:1322156099658580060>, Epic <:epic:1322156124958363698>, "
                "Mythic <:mythic:1322156148274761839> and Legendary <:legendary:1322156175784939520>,\n"
                "- <:meowy123:1322150120178843710> | The Creator - this is the emoji of the creator of the character received.\n\n"
                "## The system for choosing the character received:\n"
                "1. The rarity of the character is chosen, with the chances of 35% for Common <:common:1322156037884608532>, "
                "30% for Uncommon <:uncommon:1322156070021632052>, 20% for Rare <:rare:1322156099658580060>, 10% for Epic <:epic:1322156124958363698>, "
                "4% for Mythic <:mythic:1322156148274761839> and 1% for Legendary <:legendary:1322156175784939520>.\n"
                "2. The specific character is chosen randomly out of the rarity, each character having the same chances."
            ),
            view=None
        )

    async def inventory_callback(interaction):
        # Edit the message and remove the buttons
        await interaction.response.edit_message(
            content=(
                "# __Meowy's Gacha Bot Info - Inventory__:\n\n"
                "Here's how an example of how the !inventory command shows up:\n\n"
                "## <:common:1322156037884608532> **Common**:\n"
                "<:meowy:1321038752487047178> Meowy - <:meowy123:1322150120178843710> - ⭐ ⭐ 6/15\n"
                "<:claw:1321039526973542472> Claw - <:meowy123:1322150120178843710> - unobtained\n\n"
                "## The inventory message includes:\n"
                "- <:common:1322156037884608532> **Common** | The Rarity - characters in the inventory are split up into rarities, "
                "<:common:1322156037884608532> **Common**, <:uncommon:1322156070021632052> **Uncommon**, <:rare:1322156099658580060> **Rare**, "
                "<:epic:1322156124958363698> **Epic**, <:mythic:1322156148274761839> **Mythic** and <:legendary:1322156175784939520> **Legendary**,\n"
                "- <:meowy:1321038752487047178> Meowy & <:claw:1321039526973542472> Claw | The Characters - these are the characters in the specific rarity,\n"
                "- <:meowy123:1322150120178843710> | The Creator - this is the creator of the characters,\n"
                "- ⭐ ⭐ 6/15 | The Stars and The Character Amounts - these represent how many of the character are owned, stars being received for different amounts of characters: "
                "⭐ - 1 character, ⭐⭐ - 5 characters, ⭐⭐⭐ - 15 characters, ⭐⭐⭐⭐ - 40 characters, ⭐⭐⭐⭐⭐ - 100 characters. The other numbers are the amount of characters owned and the amount needed for the next star goal respectively,\n"
                "- If instead of the stars, the text unobtained appears when the person hasn't gotten the character even once."
            ),
            view=None  # Remove the buttons after clicking
        )


    # Link button callbacks to buttons
    button1.callback = gacha_callback
    button2.callback = inventory_callback

@bot.command(aliases=['s'])
async def stats(ctx):
    player = str(ctx.author.id)
    if player not in player_inventory:
        await ctx.send(
            f"{ctx.author.mention}, you don't have any characters yet. Use !gacha to start collecting."
        )
        return

    inventory = player_inventory[player]
    total_gachas = 0
    rarity_counts = {rarity: 0 for rarity, _ in RARITIES}

    # Count the characters and gachas for each rarity
    for rarity, _ in RARITIES:
        for character, count in inventory[rarity].items():
            total_gachas += count
            rarity_counts[rarity] += count

    # Constructing the response message
    stats_message = f"# __{ctx.author.mention}'s Stats__:\n"
    for rarity, count in rarity_counts.items():
        stats_message += f"**{RARITY_EMOJIS[rarity]} {rarity}**: {count} characters.\n"
    stats_message += f"\nTotal: {total_gachas} characters."

    await ctx.send(stats_message)
    
# Run the bot
bot.run(TOKEN)
