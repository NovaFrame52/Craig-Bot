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
    "Nice. Really nice. That's how you talk to someone who paid for your childhood?",
    "I see we've reached the stage where manners go to die.",
    "Well, that's certainly one way to hurt the old man.",
    "If that's what you think of me, I won't keep you.",
    "You know, I had higher hopes for your communication skills.",
    "And they say I'm the problem. Fascinating perspective.",
    "I taught you better than this. Let me check my notes...",
    "Lovely. Just lovely. This is what I get.",
    "That stung about as much as your life choices do.",
    "You seem angry. Did I forget to buy something again?",
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
    "As hard as it is to swallow, I'm telling the truth.",
    "I get that look of shock. I'm not used to being believed.",
    "You heard me right. I said it. And I meant it.",
    "I wish I was making this up. Trust me.",
    "Yeah, it's real. That's what makes it so hard to accept.",
    "That's the truth, and nothing but.",
    "I'm not joking around here. For once.",
    "Surprising what happens when you pay attention, isn't it?",
    "I know, I know. Hard to believe I got something right.",
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
    "This is why I drink coffee at 3 PM.",
    "Oh, for heaven's sake. Not this again.",
    "I thought we talked about this. Apparently not.",
    "Well, that's just... I don't even have words.",
    "This is exactly why I got those gray hairs.",
    "You know what? I'm too tired for this right now.",
    "And I thought I was done being surprised by you.",
    "Dear Lord, give me patience. I've run out.",
    "This is what my life has become.",
    "Why do I even try anymore?",
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
    "Yeah, well, join the club. We meet on Thursdays.",
    "That's the story of my life, kid. Take notes.",
    "If this isn't a sign, I don't know what is.",
    "You know what? I'm not even mad anymore. Just tired.",
    "This is exactly what I deserved, apparently.",
    "Welcome to the party. I've been here since Tuesday.",
    "I remember when things were simpler. Then you were born.",
    "At least you're consistent with the disappointment delivery.",
    "Yep. That tracks with my life experience.",
    "This is exactly what my therapist warned me about.",
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
    "You know, I have exactly the amount of surprise I was expecting. Which is none.",
    "Well, I guess this is what happens when you think with your heart instead of your head.",
    "Your mother warned you about this. I remember the conversation clearly.",
    "I'm not mad. Mad would imply I still had hope.",
    "This is fine. Everything is fine. I'm not panicking.",
    "Remember when life made sense? Those were the days.",
    "I'll just sit here with my indigestion and watch this unfold.",
    "You know what the worst part is? I actually expected this.",
    "I'm keeping a detailed record of this for your therapy.",
    "This is the moment we'll laugh about someday. Not today, though.",
    "I'm writing a book. You're chapter twelve.",
    "Well, that's one way to make your mother right about everything.",
    "You've really outdone yourself this time. Congratulations.",
    "I'm at that age where I don't have the energy to deal with this.",
    "This is exactly what I bargained for when I became a parent. Just kidding.",
    "You're making excellent progress in the wrong direction.",
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


@client.tree.command(name="disappointed", description="Express disappointment")
async def disappointed(interaction: discord.Interaction, target: str = "you"):
    """Craig expresses his deep disappointment in someone or something"""
    try:
        disappointments = [
            f"{target}... I am deeply disappointed.",
            f"{target}, I expected better from you.",
            f"I looked at {target} and all I felt was disappointment.",
            f"{target}. That's all I can say.",
            f"The disappointment I feel toward {target} is immeasurable.",
            f"{target} has achieved new heights of letting me down.",
        ]
        reply = random.choice(disappointments)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /disappointed used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in disappointed command")


@client.tree.command(name="lecture", description="Craig delivers a lecture")
async def lecture(interaction: discord.Interaction):
    """Craig gives you a lengthy, disappointed lecture"""
    try:
        lectures = [
            "You know, when I was your age... actually, I was responsible. Moving on.",
            "Let me tell you about consequences. You'll be learning about them soon.",
            "I'm going to tell you something, and I want you to listen very carefully. I'm tired.",
            "Sit down. We need to talk about your life choices. All of them.",
            "You want to know what your problem is? I have seven hours and a pot of coffee.",
        ]
        reply = random.choice(lectures)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /lecture used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in lecture command")


@client.tree.command(name="advice", description="Craig gives unsolicited advice")
async def advice(interaction: discord.Interaction):
    """Craig shares some unwanted wisdom"""
    try:
        advice_list = [
            "Here's some free advice: stop doing things that disappoint me. Thanks.",
            "If I may be so bold—don't. Whatever it is, just don't.",
            "Listen, here's what you need to do: nothing. Do nothing and wait for instructions.",
            "I'm giving you advice you didn't ask for: you're doing it wrong.",
            "My advice? Lower your expectations. For yourself. Significantly.",
            "You want advice? Stop asking me for validation and figure it out yourself.",
        ]
        reply = random.choice(advice_list)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /advice used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in advice command")


@client.tree.command(name="memories", description="Craig reminisces")
async def memories(interaction: discord.Interaction):
    """Craig reminisces about better times"""
    try:
        memories_list = [
            "Ah, I remember when you used to listen. Those were the days.",
            "You know, there was a time when you made decisions I didn't immediately regret.",
            "Remember when things made sense? Neither do I, but I keep hoping.",
            "I miss the old days. Back when you had potential.",
            "Those were simpler times. Before you became... this.",
            "You know what I miss most? Your potential. Also sleep.",
        ]
        reply = random.choice(memories_list)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /memories used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in memories command")


@client.tree.command(name="coffee", description="Craig and his coffee")
async def coffee(interaction: discord.Interaction):
    """Craig has some coffee and commentary"""
    try:
        coffee_comments = [
            "*takes a long sip of coffee* This is getting cold faster than my faith in you.",
            "You know what's better than talking to you? Coffee. And I'm out of coffee.",
            "*pours another cup* I'm going to need more coffee for this.",
            "*stares into coffee mug* Is it too late to start over?",
            "This coffee is the only thing getting me through today. Well, this and disappointment.",
            "*sips coffee* At least my coffee doesn't talk back. That's something.",
        ]
        reply = random.choice(coffee_comments)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /coffee used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in coffee command")


@client.tree.command(name="rant", description="Craig goes on a mild rant")
async def rant(interaction: discord.Interaction):
    """Craig lets loose with some complaints"""
    try:
        rants = [
            "You know what really grinds my gears? Everything. Absolutely everything.",
            "I could go on for hours about this. I probably will. Get comfortable.",
            "Don't even get me started. Too late, I'm starting. Where do I begin?",
            "This is exactly what I'm talking about. I don't have to explain it; you know.",
            "I've been meaning to say something. Actually, I've been meaning to say lots of things.",
        ]
        reply = random.choice(rants)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /rant used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in rant command")


@client.tree.command(name="expectations", description="Craig discusses expectations")
async def expectations(interaction: discord.Interaction):
    """Craig talks about his (lowered) expectations"""
    try:
        expectations_list = [
            "My expectations for you are so low, even you can clear them. And yet...",
            "Here's the thing about expectations. I've stopped having them.",
            "I don't expect much. I never do. You still manage to disappoint me.",
            "I had expectations once. Life beat that out of me.",
            "Do you want to know what I expect from you? Nothing. Absolutely nothing. You're welcome.",
            "My expectations adjust downward daily. You're still not meeting them.",
        ]
        reply = random.choice(expectations_list)
        await interaction.response.send_message(reply)
        logger.info(f"Slash command /expectations used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in expectations command")


@client.tree.command(name="about", description="Learn about Craig and his commands")
async def about(interaction: discord.Interaction):
    """Display information about Craig and all available commands"""
    try:
        about_text = """**Craig Discord Bot v2.0.0**
A disappointed dad bot with 100+ responses and 11 interactive commands.

**Core Commands:**
• `/dadjoke` - Get a random disappointed dad response
• `/roast [target]` - Get roasted by Craig (optional target)
• `/wisdom` - Craig shares a life lesson
• `/sigh` - Craig expresses disappointment with a sigh

**Emotional Commands:**
• `/disappointed [target]` - Express deep disappointment
• `/lecture` - Craig delivers a lengthy lecture
• `/advice` - Craig shares unsolicited wisdom
• `/memories` - Craig reminisces about better times
• `/coffee` - Craig comments while having coffee
• `/rant` - Craig goes on a mild rant
• `/expectations` - Craig discusses his lowered expectations

**Utility Commands:**
• `/about` - This message
• `/sync` - Sync Craig's commands to your server

**Trigger System:**
Craig automatically responds to 50+ trigger phrases and always responds when mentioned.
Response chance is configurable via RESPONSE_CHANCE environment variable (default: 50%).

For more info, visit: https://github.com/aster/Craig"""
        await interaction.response.send_message(about_text)
        logger.info(f"Slash command /about used by {interaction.user} in {interaction.channel}")
    except Exception as e:
        logger.exception("Error in about command")


@client.tree.command(name="sync", description="Sync Craig's commands to this server")
async def sync(interaction: discord.Interaction):
    """Manually sync slash commands to the current server"""
    try:
        # Check if user is admin or has manage_guild permission
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You need to be an administrator to use this command.", ephemeral=True)
            logger.info(f"Sync command blocked for non-admin {interaction.user} in {interaction.channel}")
            return
        
        await client.tree.sync()
        await interaction.response.send_message("Commands synced successfully!", ephemeral=True)
        logger.info(f"Slash commands synced by {interaction.user} in {interaction.guild}")
    except Exception as e:
        logger.exception("Error in sync command")
        await interaction.response.send_message("Failed to sync commands. Check the logs.", ephemeral=True)


def main():
    try:
        client.run(DISCORD_TOKEN)
    except Exception:
        logger.exception("Bot encountered an error while running")


if __name__ == "__main__":
    main()
