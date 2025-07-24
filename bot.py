import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove

# 🔑 Токен от BotFather
API_TOKEN = '8254692806:AAFMTqWDelkdKkDWDA2ArGbiV7vKxGQX1x8'
ADMIN_ID = 6356300440  # Твой Telegram ID

# Состояния
class Form(StatesGroup):
    fio = State()
    react = State()
    status = State()
    reason = State()
    location = State()
    salary = State()
    cypress = State()
    structure = State()
    flaky = State()
    mocks = State()
    test1 = State()
    test2 = State()
    test3 = State()

# Хранилище
storage = MemoryStorage()

# Бот и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=storage)

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Напиши, пожалуйста, своё ФИО и ссылку на резюме:")
    await state.set_state(Form.fio)

@dp.message(Form.fio)
async def process_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Вопрос 1. Расскажите про ваш опыт с React, MobX, TypeScript:")
    await state.set_state(Form.react)

@dp.message(Form.react)
async def process_react(message: Message, state: FSMContext):
    await state.update_data(react=message.text)
    await message.answer("Вопрос 2. Сейчас вы трудоустроены? Когда готовы приступить?")
    await state.set_state(Form.status)

@dp.message(Form.status)
async def process_status(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    await message.answer("Вопрос 3. Почему хотите сменить работу?")
    await state.set_state(Form.reason)

@dp.message(Form.reason)
async def process_reason(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await message.answer("Вопрос 4. Рассматриваете удалёнку или офис?")
    await state.set_state(Form.location)

@dp.message(Form.location)
async def process_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("Вопрос 5. Ваши ожидания по зарплате (в ₽)?")
    await state.set_state(Form.salary)

@dp.message(Form.salary)
async def process_salary(message: Message, state: FSMContext):
    try:
        salary = int(''.join(filter(str.isdigit, message.text)))
    except:
        await message.answer("Пожалуйста, укажите зарплату числом")
        return

    data = await state.get_data()
    await state.update_data(salary=salary)

    if salary > 300000:
        await message.answer("Спасибо за ваш отклик и интерес к вакансии. На текущий момент бюджет по позиции ограничен 300 000 ₽, поэтому мы не можем продолжить процесс. Если в будущем появится подходящая роль, мы обязательно свяжемся с вами. Желаем вам успехов!")
        await state.clear()
        return

    if 'не' in data['location'].lower() and 'рос' not in data['location'].lower():
        await message.answer("Благодарим за интерес к вакансии. К сожалению, на текущий момент мы рассматриваем кандидатов, находящихся в пределах РФ. Если ситуация изменится, будем рады вернуться к общению. Удачи!")
        await state.clear()
        return

    await message.answer("Вопрос 6. Расскажите про опыт с Cypress и e2e-тестами")
    await state.set_state(Form.cypress)

@dp.message(Form.cypress)
async def process_cypress(message: Message, state: FSMContext):
    await state.update_data(cypress=message.text)
    await message.answer("Вопрос 7. Как структурируете тесты? Best practices?")
    await state.set_state(Form.structure)

@dp.message(Form.structure)
async def process_structure(message: Message, state: FSMContext):
    await state.update_data(structure=message.text)
    await message.answer("Вопрос 8. Как оптимизируете flaky-тесты?")
    await state.set_state(Form.flaky)

@dp.message(Form.flaky)
async def process_flaky(message: Message, state: FSMContext):
    await state.update_data(flaky=message.text)
    await message.answer("Вопрос 9. Опыт с mock, stub, intercept и CI/CD?")
    await state.set_state(Form.mocks)

@dp.message(Form.mocks)
async def process_mocks(message: Message, state: FSMContext):
    await state.update_data(mocks=message.text)
    await message.answer("Спасибо! Теперь 3 задачки. Первая:\nЧерепашка лезет на холм 100м, днём +50, ночью -30. На какие сутки заберётся?")
    await state.set_state(Form.test1)

@dp.message(Form.test1)
async def process_test1(message: Message, state: FSMContext):
    await state.update_data(test1=message.text)
    await message.answer("Задача 2: Посчитайте количество рукопожатий между 10 людьми")
    await state.set_state(Form.test2)

@dp.message(Form.test2)
async def process_test2(message: Message, state: FSMContext):
    await state.update_data(test2=message.text)
    await message.answer("Задача 3: Напишите функцию, удаляющую дубли из строки со словами через запятую")
    await state.set_state(Form.test3)

@dp.message(Form.test3)
async def process_test3(message: Message, state: FSMContext):
    await state.update_data(test3=message.text)
    data = await state.get_data()

    # Проверка чисел
    passed = False
    if '4' in data['test1'] and '45' in data['test2']:
        passed = True

    summary = f"\nНовый кандидат:\n\nФИО и резюме: {data.get('fio')}\n\n"
    summary += f"Зарплата: {data.get('salary')}\nЛокация: {data.get('location')}\n\n"
    summary += f"Ответы:\n1: {data.get('react')}\n2: {data.get('status')}\n3: {data.get('reason')}\n"
    summary += f"4: {data.get('location')}\n5: {data.get('salary')}\n6: {data.get('cypress')}\n"
    summary += f"7: {data.get('structure')}\n8: {data.get('flaky')}\n9: {data.get('mocks')}\n"
    summary += f"\nТесты:\n1: {data.get('test1')}\n2: {data.get('test2')}\n3: {data.get('test3')}\n"

    if passed:
        summary += "\n✅ Кандидат прошёл тест!"
        await bot.send_message(ADMIN_ID, summary)
        await message.answer("Спасибо за ответы на вопросы! Я передаю ваше резюме на рассмотрение команде. Пожалуйста, ожидайте фидбека в течение 2–3 (иногда чуть дольше) рабочих дней.")
    else:
        await message.answer("Благодарим за участие и интерес к вакансии. К сожалению, тестовые ответы не соответствуют нашим ожиданиям. Удачи вам в дальнейшем профессиональном пути!")

    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(summary + "\n" + "="*40 + "\n")

    await state.clear()

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
