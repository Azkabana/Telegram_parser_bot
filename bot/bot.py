import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("API_TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher()  # просто диспетчер
