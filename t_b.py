import telebot
from telebot import types
# Вставьте сюда ваш токен от бота
API_TOKEN = '7320624649:AAEK3qDvTc4UzgeJi3uw9xGZA2fnt7FYuWI'


# Ваш токен от BotFather


# Уровень сложности
LEVEL = None

# Вопросы и ответы для разных уровней сложности
EASY_QUESTIONS = [
    {'question': 'Какой океан является самым большим?', 'answer': 'Тихий океан'},
    {'question': 'Какая страна является самой большой по площади?', 'answer': 'Россия'}
]

MEDIUM_QUESTIONS = [
    {'question': 'В каком городе находится Эйфелева башня?', 'answer': 'Париж'},
    {'question': 'Столицей какой страны является Канберра?', 'answer': 'Австралия'}
]

HARD_QUESTIONS = [
    {'question': 'Самая высокая гора в мире?', 'answer': 'Эверест'},
    {'question': 'Самый длинный пролив в мире?', 'answer': 'Мозамбикский пролив'}
]

# Инициализация бота
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/easy')
    itembtn2 = types.KeyboardButton('/medium')
    itembtn3 = types.KeyboardButton('/hard')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Привет! Выберите уровень сложности:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global LEVEL
    if message.text == '/easy':
        LEVEL = EASY_QUESTIONS
        ask_question(message)
    elif message.text == '/medium':
        LEVEL = MEDIUM_QUESTIONS
        ask_question(message)
    elif message.text == '/hard':
        LEVEL = HARD_QUESTIONS
        ask_question(message)


def ask_question(message):
    current_question = LEVEL.pop(0)
    markup = types.ForceReply(selective=False)
    bot.send_message(
        message.chat.id,
        f'Вопрос: {current_question["question"]}',
        reply_markup=markup
    )
    bot.register_next_step_handler(message, check_answer, current_question)


def check_answer(message, current_question):
    if message.text.lower() == current_question['answer'].lower():
        bot.send_message(
            message.chat.id,
            "Правильно!"
        )
    else:
        bot.send_message(
            message.chat.id,
            f"Неверно. Правильный ответ: {current_question['answer']}"
        )

    if len(LEVEL) > 0:
        ask_question(message)
    else:
        bot.send_message(
            message.chat.id,
            'Викторина завершена!'
        )


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)

