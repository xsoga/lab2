import logging
import time
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token="6074259195:AAF2CvNxsB3qiHVmQWlaRVPTq-X931KErLw")
dp = Dispatcher(bot)


logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот для записи к врачу. Чтобы начать, напишите /record")


@dp.message_handler(commands=['record'])
async def process_record_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*["Терапевт", "Гастроэнтеролог ", "Хирург"])
    await message.reply("Выберите врача:", reply_markup=keyboard)

    @dp.message_handler(lambda message: message.text in ["Терапевт", "Гастроэнтеролог ", "Хирург"])
    async def process_doctor_choice(message: types.Message):
        doctor = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"])
        await message.reply("Выберите дату:", reply_markup=keyboard)

        @dp.message_handler(lambda message: message.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"])
        async def process_date_choice(message: types.Message):
            date = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*["10:00", "11:00", "12:00", "13:00", "14:00"])
            await message.reply("Выберите время:", reply_markup=keyboard)


            @dp.message_handler(lambda message: message.text in ["10:00", "11:00", "12:00", "13:00", "14:00"])
            async def process_time_choice(message: types.Message):
                time = message.text
                await message.reply("Введите ФИО пациента:")

                @dp.message_handler()
                async def process_patient_name(message: types.Message):
                    patient_name = message.text
                    await message.reply(f"Вы записались к {doctor} на {date} в {time}. ФИО пациента: {patient_name}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
