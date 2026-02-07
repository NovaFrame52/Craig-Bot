#!/usr/bin/env python3
import os
import logging
import random
import asyncio
from dotenv import load_dotenv
import discord
import re
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
RESPONSE_CHANCE = float(os.getenv("RESPONSE_CHANCE", "0.5"))
LOG_FILE = os.getenv("LOG_FILE", "craig.log")

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set in environment")

logger = logging.getLogger("craig")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(formatter)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

# Trigger categories with specific trigger phrases
TRIGGER_CATEGORIES = {
    "insult": [
        "fuck you",
        "oh fuck you",
        "fuck yourself",
        "fuck off",
        "piss off",
        "go fuck",
        "bite me",
        "suck it",
        "kiss my ass",
        "up your ass",
        "screw you",
    ],
    "disbelief": [
        "are you kidding me",
        "are you serious",
        "youre kidding",
        "youre kidding me",
        "you kidding me",
        "you gotta be kidding",
        "you have got to be",
        "are you fucking kidding",
        "are you fucking serious",
        "seriously",
        "yeah right",
        "in your dreams",
        "no fucking way",
        "no fucking chance",
        "hell no",
        "absolutely not",
    ],
    "exasperation": [
        "what the hell",
        "what the fuck",
        "what in god's name",
        "what in gods name",
        "wtf",
        "what the",
        "this is bullshit",
        "this is crap",
        "this is ridiculous",
        "come on",
        "give me a break",
    ],
    "frustration": [
        "fuck this",
        "fuck that",
        "screw this",
        "screw that",
        "how stupid",
        "how dumb",
        "how ridiculous",
        "are you dense",
        "are you retarded",
        "youre shitting me",
        "for real",
    ],
}

# Build normalized trigger map for more reliable matching
def _normalize_text(s: str) -> str:
    s = s.lower()
    # replace punctuation with spaces
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

NORMALIZED_TRIGGER_CATEGORIES = {}
for cat, phrases in TRIGGER_CATEGORIES.items():
    NORMALIZED_TRIGGER_CATEGORIES[cat] = [_normalize_text(p) for p in phrases]

# Responses for when someone insults Craig
RESPONSES_INSULT = [
    "Wow. Real classy.",
    "You know, there was a time when you respected me.",
    "I see. So we're doing this now.",
    "That hurts. And I'm already disappointed in you.",
    "Real mature. I'm so glad I stayed for this.",
    "You know what? I'm done trying.",
    "Language like that is why we don't talk anymore.",
    "There it is. The respect I deserve.",
    "And here I thought things couldn't get worse.",
    "Your mother would say the same thing.",
]

# Responses for disbelief/sarcasm
RESPONSES_DISBELIEF = [
    "Yeah, believe it. Life's full of surprises.",
    "I'm dead serious. Wish I wasn't.",
    "Believe it or not, that actually happened.",
    "I get it—hard to believe I'd do something right for once.",
    "You think I'm joking? I wish I was.",
    "Yes. I was serious. Shocking, I know.",
    "That's the reality of the situation, believe it or not.",
    "I know it sounds unbelievable, but here we are.",
    "Welcome to the real world, kiddo.",
]

# Responses for general exasperation
RESPONSES_EXASPERATION = [
    "Well, that's disappointing. I raised you better than this.",
    "I was hoping for better, but here we are.",
    "I had bigger dreams for you, kiddo.",
    "We used to talk about this at the kitchen table.",
    "I'm not angry; I'm just... quietly disappointed.",
    "I haven't heard that one in a while.",
    "Yeah, life's frustrating. Try being a parent.",
    "Join the club. Population: me.",
    "Tell me something I don't know.",
    "You and frustration are old friends, huh?",
    "At least you're consistent.",
]

# Responses for general frustration
RESPONSES_FRUSTRATION = [
    "I know. Trust me, I know.",
    "Believe me, I've been there.",
    "Yeah, that's about right.",
    "Tell me about it.",
    "If I had a nickel for every time... well, I still don't have nickels.",
    "Fine. Go on then. I'm just here with my coffee and low expectations.",
    "It's okay. I have a recliner and a long memory.",
    "You and bad timing are in a lifelong friendship.",
    "At this point, I'm just watching the show.",
    "Ah. Another day, another disappointment.",
]

# General/fallback responses (used for slash commands and direct mentions)
RESPONSES_GENERAL = [
    "Ah. Of course. Just like when you left your socks everywhere.",
    "You do realize I paid for that, right? Emotionally and financially.",
    "You always were good at choosing poorly.",
    "I've seen worse. Not proud to say it, though.",
    "When you were little you used to build better decisions with blocks.",
    "I suppose congratulations are in order—for continuing a tradition of bad ideas.",
    "I remember when mistakes had a shorter half-life.",
    "Someday you'll tell this story at your own disappointment party.",
    "If patience were currency, I'd be bankrupt.",
    "This is exactly the plot twist I didn't ask for.",
    "Lovely. Another episode in the saga of questionable choices.",
    "You know, for all your... enthusiasm, you could try a little tact.",
    "Ah yes, the classic move. Predictable, yet somehow charming.",
    "I suppose this is your way of asking for attention. Risky.",
    "You do understand there are consequences that aren't just my sighs, right?",
    "If only I could send you back to the advice aisle.",
    "I've got popcorn for your life decisions show.",
    "Well, at least you keep things interesting.",
    "I expected a better punchline, but this will do.",
    "Surprising? No. Entertaining? Mildly.",
    "When you said you'd grow, I didn't mean this.",
    "Oh good, another story for the 'I told you so' scrapbook.",
    "You say that now. We'll revisit this when you're older and correct-er.",
    "You should put a bit more thought into slow decisions.",
    "I gave you advice once. It aged like milk.",
    "If there were awards for trying and failing, you'd be nominated.",
    "You do realize I'm contractually obligated to be disappointed, right?",
    "Keep going. I enjoy the narrative arc of this.",
    "This reminds me of the time I thought you'd do something sensible.",
    "It's fine. I'll add it to the 'lessons' folder.",
    "You call it chaos; I call it Tuesday.",
    "At least you're passionate. Misguided, but passionate.",
    "Do you want a lecture or just someone to sigh for you? Because I can do both.",
    "That's a bold move. Not the good kind.",
    "I see. And what did you plan to do after that?",
]


def contains_trigger(content: str) -> str | None:
    """
    Check if content contains a trigger phrase and return the category.
    Returns the category name if found, None otherwise.
    """
    low = _normalize_text(content)
    # surround with spaces to better match whole phrases
    low_spaced = f" {low} "
    for category, phrases in NORMALIZED_TRIGGER_CATEGORIES.items():
        for phrase in phrases:
            if f" {phrase} " in low_spaced:
                return category
    # fallback: also allow substring matches (covers short words like wtf)
    for category, phrases in NORMALIZED_TRIGGER_CATEGORIES.items():
        for phrase in phrases:
            if phrase and phrase in low:
                return category
    return None


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user} (id: {client.user.id})")
    try:
        await client.tree.sync()
        logger.info("Synced slash commands")
    except Exception:
        logger.exception("Failed to sync slash commands")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    try:
        content = message.content or ""
        # Check if Craig's name appears anywhere in the message
        mentioned = client.user in message.mentions
        name_in_message = "craig" in content.lower()

        # Check for trigger phrases and get category
        trigger_category = contains_trigger(content)

        # Diagnostic logging to help understand detection/response decisions
        logger.info(f"Message from {message.author}: '{content}'")
        logger.info(f"Detection: mentioned={mentioned}, name_in_message={name_in_message}, trigger_category={trigger_category}")

        responded = False

        # If Craig's name is mentioned anywhere, he always responds
        if mentioned or name_in_message:
            if trigger_category == "insult":
                # Direct insult gets insult response
                reply = random.choice(RESPONSES_INSULT)
            else:
                # Name mention without insult gets general response
                reply = random.choice(RESPONSES_GENERAL)
            
            await message.channel.send(reply)
            logger.info(f"Responded to name mention in {message.channel} by {message.author}")
            responded = True

        # If Craig's name wasn't mentioned, triggers have a chance to respond
        if not responded and trigger_category:
            r = random.random()
            logger.info(f"Trigger found; random={r:.3f}, threshold={RESPONSE_CHANCE}")
            if r < RESPONSE_CHANCE:
                # Select response based on trigger category
                if trigger_category == "insult":
                    reply = random.choice(RESPONSES_INSULT)
                elif trigger_category == "disbelief":
                    reply = random.choice(RESPONSES_DISBELIEF)
                elif trigger_category == "exasperation":
                    reply = random.choice(RESPONSES_EXASPERATION)
                elif trigger_category == "frustration":
                    reply = random.choice(RESPONSES_FRUSTRATION)
                else:
                    reply = random.choice(RESPONSES_GENERAL)
                
                await message.channel.send(reply)
                logger.info(f"Responded to {trigger_category} trigger in {message.channel} by {message.author}")
            else:
                logger.info("Decided not to respond to trigger (random threshold)")

    except Exception as e:
        logger.exception("Error handling message")

    # Allow slash commands to work
    await client.process_commands(message)


@client.tree.command(name="dadjoke", description="Get a disappointed dad response")
async def dadjoke(interaction: discord.Interaction):
    """Delivers a random dad line"""
    try:
        reply = random.choice(RESPONSES_GENERAL)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /dadjoke used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in dadjoke command")


@client.tree.command(name="roast", description="Get roasted by Craig")
async def roast(interaction: discord.Interaction, target: str = "you"):
    """Craig roasts someone or something"""
    try:
        reply = random.choice(RESPONSES_GENERAL)
        await interaction.response.send_message(f"{target}, {reply.lower()}")
        logger.info(f"Slash command /roast used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in roast command")


@client.tree.command(name="wisdom", description="Craig shares some disappointed wisdom")
async def wisdom(interaction: discord.Interaction):
    """Craig shares his life lessons"""
    try:
        reply = random.choice(RESPONSES_GENERAL)
        await interaction.response.send_message(f"*sighs* ... {reply}")
        logger.info(f"Slash command /wisdom used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in wisdom command")


@client.tree.command(name="sigh", description="Craig just sighs")
async def sigh(interaction: discord.Interaction):
    """Craig expresses his disappointment through a sigh"""
    try:
        sighs = ["*sigh*", "*long sigh*", "*disappointed sigh*", "*deep sigh*", "...*sigh*"]
        reply = random.choice(sighs)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /sigh used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in sigh command")


def main():
    try:
        client.run(DISCORD_TOKEN)
    except Exception:
        logger.exception("Bot encountered an error while running")


if __name__ == "__main__":
    main()
