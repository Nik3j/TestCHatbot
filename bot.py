
import logging
from aiogram import Bot, Dispatcher, executor, types
from api_req import get_lates_list, exchange

logging.basicConfig(level=logging.INFO)

API_TOKEN = "1742549270:AAFJKwHGyC-QPxvsBjmuHonjBh_0vEPwhgE"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("This is test exchange bot \n \
        available commands:\n\
        /list or /lst to get currency list\n\
        /exchange *value* *currency from* to *currency to*")

@dp.message_handler(commands=['list', 'lst'])
async def send_list(message: types.Message):
    await message.answer(get_lates_list())

@dp.message_handler(commands=['exchange'])
async def send_exhange(message: types.Message):
    await message.answer(exchange(message['text']))
@dp.message_handler()
async def message(message: types.Message):
    await message.answer('Choose one of commands please')
if __name__ == '__main__':
    executor.start_polling(dp)