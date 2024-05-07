import telebot
from telebot import types
from DataB import conn
from tokken import TOKEN
import datetime

# Создаем объект cursor для выполнения запросов к базе данных
cursor = conn.cursor()
bot = telebot.TeleBot(TOKEN)
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавить задачу")
    markup.add(item1)
    bot.send_message(message.chat.id, "Для запуска бота команда /start, существует  две команды: /add и tsk", reply_markup=markup)

# Обработчик команды "Добавить задачу"
@bot.message_handler(commands=['add'])
def add_task_handler(message):
    bot.send_message(message.chat.id, "Введите текст задачи:")
    bot.register_next_step_handler(message, add_task)
# Функция для добавления задачи в базу данных
def add_task(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Unknown"
    user_last_name = message.from_user.last_name or "Unknown"
    task_text = message.text

    # SQL-запрос для добавления задачи в таблицу
    insert_query = "INSERT INTO tasks (user_id, user_name, user_last_name, task_text) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (user_id, user_name, user_last_name, task_text))
    conn.commit()

    bot.send_message(message.chat.id, "Задача успешно добавлена!")
# Обработчик команды /tasks для вывода списка задач
@bot.message_handler(commands=['tsk'])
def show_tasks(message):
    # SQL-запрос для выборки всех задач из базы данных
    select_query = "SELECT task_id, user_name, user_last_name, task_text, user_id, created_at FROM tasks"
    cursor.execute(select_query)
    tasks = cursor.fetchall()

    if tasks:
        # Создаем текст сообщения со списком задач
        tasks_text = "Список задач:\n\n"
        for task in tasks:
            task_id, user_name, user_last_name, task_text, created_at, user_id = task
            created_at_formatted = datetime.datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S')
            tasks_text += f"Задача #{task_id}\nОт: {user_name} {user_last_name}\nДата: {created_at_formatted}\nТекст: {task_text}\n\n"

        # Отправляем сообщение с списком задач
        bot.send_message(message.chat.id, tasks_text)
    else:
        bot.send_message(message.chat.id, "Список задач пуст.")


bot.infinity_polling()


# Закрытие соединения с базой данных
conn.close()