import json
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("💼 Каталог профессий", "📚 Курсы", "💰 Способы заработка")
    kb.add("🔍 Поиск работы", "⚙ Настройки", "ℹ О боте")
    await message.answer("Привет! 👋 Я помогу тебе найти способы заработка в интернете и на фрилансе!", reply_markup=kb)

@dp.message_handler(lambda msg: msg.text == "💼 Каталог профессий")
async def show_professions(message: types.Message):
    with open("data/professions.json", encoding="utf-8") as f:
        professions = json.load(f)

    for p in professions:
        text = f"{p['emoji']} <b>{p['title']}</b>\n\n📋 {p['description']}\n💵 Доход: {p['income']}\n🎓 Навыки: {p['skills']}\n🚀 Как начать: {p['start']}\n🔗 Ресурсы: {p['resources']}"
        await message.answer(text, parse_mode='HTML')

if __name__ == "__main__":
    from aiogram import executor
    dp.loop.run_until_complete(bot.delete_webhook(drop_pending_updates=True))
    executor.start_polling(dp, skip_updates=True)
