# Discord Translation Bot using Gemini API

This is an open-source Discord bot that provides real-time translation capabilities using Google's Gemini API. Instead of keeping an AI translator open in your browser, this bot seamlessly translates conversations directly in your Discord channels using the gemini-1.5-flash model.

## Features

- Translates text messages using Gemini API.
- Allows users to select the language they want to translate to.
- Works seamlessly in a Discord chat environment.

## Required Packages

The following Python packages are used in this project:

- **discord.py**: A Python library to interact with the Discord API.
  ```bash
  pip install discord.py
  ```

- **google-generativeai**: A library to interact with Google's Gemini API for text generation.
  ```bash
  pip install google-generativeai
  ```

- **python-dotenv**: A library to load environment variables from a .env file.
  ```bash
  pip install python-dotenv
  ```

## Usage

1. Set up your .env file with your GEMINI_API_KEY and DISCORD_TOKEN. The .env file should look like this:
  ```bash
  GEMINI_API_KEY = API_KEY
  DISCORD_TOKEN = API_KEY
  ```
2. Run the bot using the following command:
  ```bash
  python bot.py
  ```

## Bot Commands

Once the bot is running, you can use the following commands in your Discord server:

- **!wordwizard**: Set your interface language.
- **!settranslate [language]**: Set your translation language.
- **!activate**: Enable automatic translation in the current channel.
- **!deactivate**: Disable automatic translation in the current channel.
- **!helpword**: Show the help message in your selected language.

  



