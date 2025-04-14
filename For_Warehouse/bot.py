import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import StateFilter, Command
from utils import TextEquals
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.client.bot import DefaultBotProperties
import config
import handlers as test

# Настройка логирования
logging.basicConfig(
    filename=config.settings.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

bot = Bot(token=config.settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

class OperationState(StatesGroup):
    menu = State()  # состояние главного меню операций
    waiting_for_article = State()      # ожидание ввода артикула
    waiting_for_quantity = State()     # ожидание ввода количества
    waiting_for_comment = State()      # ожидание ввода комментария
    waiting_for_employee = State()     # ожидание ввода имени сотрудника

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    kb = ReplyKeyboardBuilder()
    kb.button(text="Остатки")
    kb.button(text="Поступления")
    kb.button(text="Отгрузки")
    kb.adjust(3)
    await message.answer(f"Здравствуй, {message.from_user.first_name}! Что бы вы хотели узнать?", reply_markup=kb.as_markup())
    logging.info(f"Пользователь {message.chat.id} запустил бота.")

@dp.message(TextEquals(equals="вернуться в главное меню"))
async def return_to_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено. Возвращаемся в главное меню.")
    await cmd_start(message, state)

@dp.message(TextEquals(equals="отмена"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Операция отменена. Возвращаемся в главное меню.")
    await cmd_start(message, state)
    logging.info(f"Пользователь {message.chat.id} отменил операцию.")

@dp.message(OperationState.waiting_for_article)
async def process_article(message: types.Message, state: FSMContext):
    article_input = message.text.strip()
    try:
        prod_info = test.validateProductArticle(article_input)
    except Exception as err:
        logging.error(f"Ошибка в process_article при проверке артикула '{article_input}': {err}")
        await message.answer("Произошла ошибка при проверке артикула. Попробуйте снова.")
        return
    if prod_info == 0:
        await message.answer("Артикул введён неверно, введите заново:")
        return
    else:
        await state.update_data(product_name=prod_info[1])
        await state.update_data(step="enter_quantity")
        await message.answer(f"Найден товар: *{prod_info[1]}*\nВведите количество:", parse_mode="Markdown")
        await state.set_state(OperationState.waiting_for_quantity)

@dp.message(OperationState.waiting_for_quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text.strip())
        await state.update_data(quantity=quantity)
        await state.update_data(step="enter_comment")
        await message.answer("Введите комментарии:")
        await state.set_state(OperationState.waiting_for_comment)
    except ValueError:
        await message.answer("Количество введено некорректно, введите число:")
        return

@dp.message(OperationState.waiting_for_comment)
async def process_comment(message: types.Message, state: FSMContext):
    comment = message.text.strip()
    await state.update_data(comment=comment)
    await state.update_data(step="enter_employee")
    await message.answer("Введите имя сотрудника:")
    await state.set_state(OperationState.waiting_for_employee)

@dp.message(OperationState.waiting_for_employee)
async def process_employee(message: types.Message, state: FSMContext):
    employee = message.text.strip()
    data = await state.get_data()
    await state.update_data(employee=employee)
    operation = data.get("operation", "")
    product_name = data.get("product_name", "")
    quantity = data.get("quantity", 0)
    comment = data.get("comment", "")
    try:
        # Вызов асинхронной функции записи операции
        result = await test.recordWarehouseOperation(product_name, operation, quantity, comment, employee)
        await message.answer(f"Данные внесены:\n{result}")
        logging.info(f"Операция успешно записана для пользователя {message.chat.id} по товару {product_name}")
    except Exception as err:
        logging.error(f"Ошибка в process_employee: {err}")
        await message.answer("🚨 Произошла ошибка при записи данных.")
    await state.clear()
    await cmd_start(message, state)

@dp.message()
async def main_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text.strip()
    data = await state.get_data()

    if text == "Остатки":
        await state.update_data(operation="rest")
        kb = ReplyKeyboardBuilder()
        kb.button(text="Общий остаток в рублях")
        kb.button(text="Остаток определенного товара")
        kb.button(text="Остаток контроллеров")
        kb.button(text="Вернуться в главное меню")
        kb.adjust(1)
        await message.answer("Выберите вариант", reply_markup=kb.as_markup())

    elif text == "Поступления":
        await state.set_state(OperationState.menu)
        await state.update_data(operation="delivery")
        kb = ReplyKeyboardBuilder()
        kb.button(text="Просмотр поступлений")
        kb.button(text="Добавить поступление")
        kb.button(text="Вернуться в главное меню")
        kb.adjust(1)
        await message.answer("Выберите действие для поступлений:", reply_markup=kb.as_markup())

    elif text == "Отгрузки":
        await state.set_state(OperationState.menu)
        await state.update_data(operation="shipment")
        kb = ReplyKeyboardBuilder()
        kb.button(text="Просмотр отгрузок")
        kb.button(text="Добавить отгрузку")
        kb.button(text="Вернуться в главное меню")
        kb.adjust(1)
        await message.answer("Выберите действие для отгрузок:", reply_markup=kb.as_markup())

    elif text == "Вернуться в главное меню":
        await state.clear()
        await cmd_start(message, state)

    elif text == "Общий остаток в рублях":
        result = test.getTotalStockValue()
        await message.answer(f"Остаток товара на складе:\n{result}")

    # При выборе "Остаток определенного товара" переходим в режим проверки артикулов
    elif text == "Остаток определенного товара":
        await state.update_data(operation="rest_specific")
        articles_list = test.listProductArticles()
        await message.answer(f"Доступные артикулы:\n{articles_list}")
        await message.answer("Введите артикул товара для проверки остатка:")
    
    elif text == "Остаток контроллеров":
        result = test.listControllerStocks()
        await message.answer(result)

    # Если пользователь уже находится в режиме проверки артикулов
    elif data.get("operation") == "rest_specific":
        # Если пользователь нажал кнопку для повторного ввода артикула
        if text == "Ввести артикул заново":
            await message.answer("Введите артикул товара для проверки остатка:")
        else:
            article_input = text.strip()
            result = test.getProductStock(article_input)
            if isinstance(result, tuple) and len(result) == 3:
                prod_name, prod_quantity, prod_total = result
                quantity_str = f"🔴 {prod_quantity:,d}" if prod_quantity < 0 else f"{prod_quantity:,d}"
                total_str = f"🔴 {prod_total:,.2f}" if prod_total < 0 else f"{prod_total:,.2f}"
                response = (
                    f"📦 <b>Результаты поиска товара</b>\n\n"
                    f"🔹 <b>Название товара:</b> {prod_name}\n"
                    f"🔹 <b>Остаток:</b> <code>{quantity_str} шт.</code>\n"
                    f"💰 <b>Общая стоимость:</b> <code>{total_str} руб.</code>"
                )
                await message.answer(response)
            else:
                await message.answer("❌ <i>Ошибка:</i> Товар не найден или нет данных.")

            # После вывода результата предлагается выбор дальнейших действий
            kb = ReplyKeyboardBuilder()
            kb.button(text="Ввести артикул заново")
            kb.button(text="Вернуться в главное меню")
            kb.adjust(1)
            await message.answer("Выберите действие:", reply_markup=kb.as_markup())

    elif text in ["Просмотр поступлений"] and data.get("operation") == "delivery":
        kb = ReplyKeyboardBuilder()
        kb.button(text="Поступления за 7 дней")
        kb.button(text="Поступления за 30 дней")
        kb.button(text="Вернуться в главное меню")
        kb.adjust(1)
        await message.answer("За какой промежуток вывести поступления?", reply_markup=kb.as_markup())

    elif text in ["Просмотр отгрузок"] and data.get("operation") == "shipment":
        kb = ReplyKeyboardBuilder()
        kb.button(text="Отгрузки за 7 дней")
        kb.button(text="Отгрузки за 30 дней")
        kb.button(text="Вернуться в главное меню")
        kb.adjust(1)
        await message.answer("За какой промежуток вывести отгрузки?", reply_markup=kb.as_markup())

    elif text in ["Поступления за 7 дней", "Поступления за 30 дней"] and data.get("operation") == "delivery":
        n = 7 if "7 дней" in text else 30
        result = test.listDeliveriesLastNDays(n)
        await message.answer(f"Поступления за {n} дней:\n{result}")
        kb = ReplyKeyboardBuilder()
        kb.button(text="Вернуться в главное меню")
        await message.answer("Вернитесь в главное меню", reply_markup=kb.as_markup())

    elif text in ["Отгрузки за 7 дней", "Отгрузки за 30 дней"] and data.get("operation") == "shipment":
        n = 7 if "7 дней" in text else 30
        result = test.listShipmentsLastNDays(n)
        await message.answer(f"Отгрузки за {n} дней:\n{result}")
        kb = ReplyKeyboardBuilder()
        kb.button(text="Вернуться в главное меню")
        await message.answer("Вернитесь в главное меню", reply_markup=kb.as_markup())

    # Добавление записи поступления
    elif text == "Добавить поступление" and data.get("operation") == "delivery":
        # Сначала выводим список всех артикулов
        articles_list = test.listProductArticles()
        await state.update_data(step="enter_article")
        await message.answer(f"Доступные артикулы:\n{articles_list}")
        await message.answer("Введите артикул товара для поступления:")
        # Переключаем состояние на ожидание ввода артикула
        await state.set_state(OperationState.waiting_for_article)

    # Добавление записи отгрузки
    elif text == "Добавить отгрузку" and data.get("operation") == "shipment":
        # Сначала выводим список всех артикулов
        articles_list = test.listProductArticles()
        await state.update_data(step="enter_article")
        await message.answer(f"Доступные артикулы:\n{articles_list}")
        await message.answer("Введите артикул товара для отгрузки:")
        # Переключаем состояние на ожидание ввода артикула
        await state.set_state(OperationState.waiting_for_article)


    else:
        await message.answer("Команда не распознана. Выберите действие из меню.")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
