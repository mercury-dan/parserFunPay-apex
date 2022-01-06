import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

from stopgame import StopGame

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('database.sqlite')
ioloop = asyncio.get_event_loop()
# инициализируем парсер
sg = StopGame('lastkey.txt')


# Команда cтарт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
		await message.answer("Привет, бот пошёл в работу")

# проверяем наличие новых игр и делаем рассылки
async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		# проверяем наличие новых игр
		new_games = sg.new_games()

		if new_games:

			cost = sg.find_cost()
			link = sg.find_link()
			price = float(cost)
			print(cost)
			print(price)
			
			subscriptions = db.get_subscriptions()
			if price <= 1500.00:
				for s in subscriptions:
					await bot.send_message(
						s[0],
						text = f"📌 Новая публикация на *FunPay*\n\n📝 {new_games}\n\n💵 *{cost} р*\n\n✅ {link}",
						parse_mode="MARKDOWN"
						)

# запускаем лонг поллинг
if __name__ == '__main__':
	ioloop.create_task(scheduled(3))
	executor.start_polling(dp, skip_updates=True)