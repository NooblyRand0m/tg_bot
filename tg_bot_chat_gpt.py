import logging
import os
import openai
import re
import random
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


# Create a logger and set its level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and set its level
file_handler = logging.FileHandler('mylog.log')
file_handler.setLevel(logging.INFO)

# Create a formatter and set it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)



# читаем список из файла и заменяем GREETINGS на него
with open('greetings.txt', 'r') as f:
    GREETINGS = [line.strip() for line in f.readlines()]


# Initialize the bot and dispatcher
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

# Initialize OpenAI API with your API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a regex pattern to extract the prompt from user request
PATTERN = r'^/gpt\s+(.+)$'


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Чтобы использовать GPT, отправь мне команду /gpt с запросом.")


@dp.message_handler(commands=['gpt'])
async def process_gpt_command(message: types.Message):
    prompt = extract_prompt(message.text)
    if prompt:
        greeting = random.choice(GREETINGS)
        await bot.send_message(chat_id=message.chat.id, text=greeting)
        response = generate_response(prompt)
        logger.info(f'Response generated for "{prompt}" with greeting "{greeting}"')
        await message.reply(response)
    else:
        await message.reply("Некорректный запрос. Используйте команду /gpt с запросом.")


def extract_prompt(text):
    match = re.match(PATTERN, text)
    if match:
        return match.group(1)
    else:
        return None


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.3,
    )
    return response.choices[0].text.strip()


if __name__ == '__main__':
    executor.start_polling(dp)
