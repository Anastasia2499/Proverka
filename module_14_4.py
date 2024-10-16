from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *


api = "7939492635:AAFsuuDIDKunLgZvOEJt6a6CgR_bXMhGe8Q"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button3 = KeyboardButton(text='Купить')
kb.add(button1)
kb.add(button2)
kb.add(button3)

kb2 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.add(button3)
kb2.add(button4)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Продукт 1", callback_data="product_buying")],
        [InlineKeyboardButton(text='Продукт 2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Продукт 3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Продукт 4', callback_data="product_buying")]
    ]
)

class UserState(StatesGroup):
     age = State()
     growth = State()
     weight = State()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'files/{i}.png', 'rb') as img:
            await message.answer_photo(img, initiate_db(i, i, i * 100))
    await message.answer("Выберите продукт для покупки:", reply_markup=buy_kb)


@dp.callback_query_handler(text='product_buying')
async def back(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * int(data["weight"]) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма калорий {calories}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)