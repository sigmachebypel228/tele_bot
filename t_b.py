import telebot
from telebot import types
# Вставьте сюда ваш токен от бота
API_TOKEN = '7987816501:AAEBMc6wJtismo4bETfoHjG6SpmOshQ9PHk'



# Создаем объект бота
bot = telebot.TeleBot(API_TOKEN)

# Уровень сложности викторины
LEVEL_EASY = 'Легкий'
LEVEL_MEDIUM = 'Средний'
LEVEL_HARD = 'Сложный'

# Вопросы и ответы для разных уровней сложности
questions = {
    LEVEL_EASY: [
        {'question': 'Какой город является столицей Франции?', 'answer': 'Париж'},
        {'question': 'Какое самое большое озеро в мире?', 'answer': 'Каспийское море'}
    ],
    LEVEL_MEDIUM: [
        {'question': 'В каком городе находится Эйфелева башня?', 'answer': 'Париже'},
        {'question': 'Где находится гора Эверест?', 'answer': 'Непал'}
    ],
    LEVEL_HARD: [
        {'question': 'Столица какого государства — Сан-Марино?', 'answer': 'Сан-Марино'},
        {'question': 'Какие два моря соединяет Суэцкий канал?', 'answer': 'Красное и Средиземное'}
    ]
}


# Функция обработки команды /start или /restart
@bot.message_handler(commands=['start', 'restart'], content_types=['text'])
def start(message):
    # Приветственное сообщение
    bot.send_message(message.chat.id, f'Привет! Давай начнем викторину по географии.')

    # Клавиатура с выбором уровня сложности
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton(LEVEL_EASY)
    itembtn2 = types.KeyboardButton(LEVEL_MEDIUM)
    itembtn3 = types.KeyboardButton(LEVEL_HARD)
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(
        message.chat.id,
        'Выбери уровень сложности:',
        reply_markup=markup
    )


# Обработка ответа на выбор уровня сложности
@bot.message_handler(content_types=['text'])
def handle_level_choice(message):
    if message.text in [LEVEL_EASY, LEVEL_MEDIUM, LEVEL_HARD]:
        level = message.text

        # Запускаем викторину
        run_quiz(level, message.chat.id)
    else:
        bot.reply_to(message, 'Пожалуйста, выберите уровень сложности из предложенных вариантов.')


# Основная функция викторины
def run_quiz(selected_level, chat_id):
    questions_for_level = questions.get(selected_level)

    for question in questions_for_level:
        user_answer = None
        while not user_answer:
            bot.send_message(chat_id, question['question'])

            # Ожидание ответа пользователя
            @bot.message_handler(content_types=['text'])
            def wait_for_answer(msg):
                nonlocal user_answer
                user_answer = msg.text.strip().lower()

                if user_answer == question['answer'].lower():
                    bot.send_message(msg.chat.id, 'Правильно!')
                else:
                    bot.send_message(msg.chat.id, 'Неверно. Правильный ответ: {}'.format(question['answer']))

                bot.register_next_step_handler(msg, wait_for_answer)


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)