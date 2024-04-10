import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import configparser
import utils

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

BOT_TOKEN = config.get('default', 'BOT_TOKEN')


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


# Обработка команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("Привет! Я бот для модерации чата. Отправь мне сообщение, и я проверю его на токсичность или добавь меня в чат для модерации сообщений")


# Обработка всех остальных сообщений
@dp.message()
async def check_toxicity(message: types.Message):

    text = message.text
    toxicity_score = utils.preprocess_and_predict(text)

    threshold = 0.8
    if toxicity_score[1] >= threshold:
        await message.reply("Ваше сообщение было удалено из-за его токсичности.")
        await message.delete()
    else:
        pass

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())