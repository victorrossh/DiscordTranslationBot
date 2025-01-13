import discord
from discord.ext import commands
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Discord configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Gemini configuration
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# Storage dictionaries
user_languages = {}  # Store user translation language preferences
active_channels = set()  # Store active translation channels
interface_languages = {}  # Store user interface language preferences

# Default English messages
DEFAULT_MESSAGES = {
    "bot_online": "Bot is online as: {}",
    "bot_id": "Bot ID: {}",
    "translation_enabled": "Automatic translation enabled in this channel",
    "translation_disabled": "Automatic translation disabled in this channel",
    "language_error": "Error processing language. Please try again.",
    "choose_language": "Please choose your native language for bot interface:",
    "language_set": "Interface language set to: {}",
    "translation_language_set": "Translation language set to: {}",
    "help_message": """
**Available Commands:**
`!wordwizard` - Set your interface language
`!settranslate [language]` - Set your translation language
`!activate` - Enable automatic translation in current channel
`!deactivate` - Disable automatic translation in current channel
`!helpword` - Show this message

**How to use:**
1. Use `!wordwizard` to set the language for bot messages
2. Use `!settranslate` to set the language you want your messages translated to
3. Use `!activate` in the channel you want translation
4. Start chatting normally!
    """
}

# Translate a message to target language using Gemini
async def translate_message(message, target_language):
    if target_language.lower() == 'english':
        return message
    
    prompt = f"Translate to {target_language}: {message}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip().strip('"\'')
    except Exception as e:
        print(f"Translation error: {e}")
        return message

# Event triggered when bot is ready
@bot.event
async def on_ready():
    print(DEFAULT_MESSAGES["bot_online"].format(bot.user.name))
    print(DEFAULT_MESSAGES["bot_id"].format(bot.user.id))
    print('-------------------')

# Set user's interface language for bot messages
@bot.command(name='wordwizard')
async def set_interface_language(ctx):
    prompt = await translate_message(
        DEFAULT_MESSAGES["choose_language"],
        interface_languages.get(ctx.author.id, 'english')
    )
    await ctx.send(prompt)
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        interface_languages[ctx.author.id] = msg.content
        
        confirm_msg = await translate_message(
            DEFAULT_MESSAGES["language_set"].format(msg.content),
            msg.content
        )
        await ctx.send(confirm_msg)
    except Exception as e:
        error_msg = await translate_message(
            DEFAULT_MESSAGES["language_error"],
            interface_languages.get(ctx.author.id, 'english')
        )
        await ctx.send(error_msg)

# Set language for message translations
@bot.command(name='settranslate')
async def set_language(ctx, *, target_language):
    try:
        prompt = f"Identify and return only the standardized English name for this language: {target_language}"
        
        response = model.generate_content(prompt)
        standardized_language = response.text.strip().strip('"\'')
        user_languages[ctx.author.id] = standardized_language
        
        confirm_prompt = f"Translate: Translation language set to {standardized_language}"
        confirm_response = model.generate_content(confirm_prompt)
        confirm_msg = confirm_response.text.strip().strip('"\'')
        
        await ctx.send(confirm_msg)
        
    except Exception as e:
        error_msg = await translate_message(
            DEFAULT_MESSAGES["language_error"],
            interface_languages.get(ctx.author.id, 'english')
        )
        await ctx.send(error_msg)

# Event triggered on every message
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    if message.author == bot.user:
        return
        
    if message.channel.id in active_channels and message.author.id in user_languages:
        try:
            prompt = f"Translate to {user_languages[message.author.id]}: {message.content}"
            
            response = model.generate_content(prompt)
            translated_text = response.text.strip().strip('"\'')
            await message.channel.send(translated_text)
            
        except Exception as e:
            print(f"Translation error: {str(e)}")

# Activate automatic translation in current channel
@bot.command(name='activate')
async def activate_channel(ctx):
    active_channels.add(ctx.channel.id)
    confirm_msg = await translate_message(
        DEFAULT_MESSAGES["translation_enabled"],
        interface_languages.get(ctx.author.id, 'english')
    )
    await ctx.send(confirm_msg)

# Deactivate automatic translation in current channel
@bot.command(name='deactivate')
async def deactivate_channel(ctx):
    active_channels.discard(ctx.channel.id)
    confirm_msg = await translate_message(
        DEFAULT_MESSAGES["translation_disabled"],
        interface_languages.get(ctx.author.id, 'english')
    )
    await ctx.send(confirm_msg)

# Show help message in user's interface language
@bot.command(name='helpword')
async def show_commands(ctx):
    user_interface_language = interface_languages.get(ctx.author.id, 'english')
    
    prompt = f"""
    Translate this help message to {user_interface_language}:
    
    {DEFAULT_MESSAGES['help_message']}
    
    Return only the translated text, keeping the same formatting with ** and ` characters.
    """
    
    try:
        response = model.generate_content(prompt)
        await ctx.send(response.text.strip().strip('"\''))
    except Exception as e:
        print(f"Error translating help message: {e}")
        await ctx.send(DEFAULT_MESSAGES["help_message"])

# Start the bot
bot.run(os.getenv('DISCORD_TOKEN'))