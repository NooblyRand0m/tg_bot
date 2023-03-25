This bot allows you to use OpenAI API to generate text responses to user requests. To use the bot, simply send a command "/gpt" followed by your request. The bot will generate a response using OpenAI API's text generation capabilities and send it back to you.

To use this bot, you will need to set up the following:

A Telegram bot token. You can obtain this by creating a new bot through the BotFather on Telegram.

An OpenAI API key. You can obtain this by signing up for OpenAI's GPT-3 beta program.

A list of greetings to randomly choose from when responding to user requests. This can be customized to your needs by modifying the "greetings.txt" file.

Once you have set up the prerequisites, you can run the bot by executing the Python script. The bot will listen for user requests and generate responses using OpenAI API's text generation capabilities.

For more information on the bot and how to set it up, please refer to the documentation in the repository.

To run the bot, execute the "run_tg_bot_chat_gpt.bat" file which contains the following code:

@echo off

call %~dp0venv\Scripts\activate.bat

set TOKEN=<your_telegram_bot_token>

set OPENAI_API_KEY=<your_openai_api_key>

python tg_bot_chat_gpt.py

pause

Make sure to replace "<your_telegram_bot_token>" and "<your_openai_api_key>" with your actual Telegram bot token and OpenAI API key respectively.
