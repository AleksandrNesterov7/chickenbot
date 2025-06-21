import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Категории спортивного питания
CATEGORIES = {
    "protein": "Протеины",
    "creatine": "Креатин",
    "vitamins": "Витамины",
    "packs": "Подписка на набор"
}

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f"cat_{key}")]
        for key, name in CATEGORIES.items()
    ])
    await message.answer("Выберите категорию спортивного питания:", reply_markup=kb)

@dp.callback_query(F.data.startswith("cat_"))
async def process_category(callback: CallbackQuery):
    category_key = callback.data.split("_")[1]
    category_name = CATEGORIES.get(category_key, "Неизвестно")
    await callback.message.edit_text(f"Вы выбрали категорию: <b>{category_name}</b>\n\nОформить подписку?", 
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Оформить подписку", callback_data=f"sub_{category_key}")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
        ])
    )

@dp.callback_query(F.data.startswith("sub_"))
async def process_subscription(callback: CallbackQuery):
    category_key = callback.data.split("_")[1]
    category_name = CATEGORIES.get(category_key, "Неизвестно")
    await callback.message.edit_text(f"🎉 Вы успешно оформили подписку на: <b>{category_name}</b>")

@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await cmd_start(callback.message)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
