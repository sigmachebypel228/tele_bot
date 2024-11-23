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
        {'question': 'Как называли царей Египта?', 'answer': 'Фараоны'},
        {'question': 'Где хоронили фараонов?', 'answer': 'В пирамидах'}
    ],
    LEVEL_MEDIUM: [
        {'question': 'Какая самая большая пирамида?', 'answer': 'Пирамида Хеопса'},
        {'question': 'Что было сердцем Афин?', 'answer': 'Акрополь'}
    ],
    LEVEL_HARD: [
        {'question': 'Как назывался древний греческий сосуд?', 'answer': 'Амфора'},
        {'question': 'Как называлось племя древних жителей Скандинавского п-ов?', 'answer': 'Норманны'}
    ]
}


# Функция обработки команды /start или /restart
@bot.message_handler(commands=['start', 'restart'], content_types=['text'])
def start(message):
    # Приветственное сообщение
    bot.send_message(message.chat.id, f'Привет! Давай начнем викторину по истории.')

    # Клавиатура с выбором уровня сложности
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton(LEVEL_EASY)
    itembtn2 = types.KeyboardButton(LEVEL_MEDIUM)
    itembtn3 = types.KeyboardButton(LEVEL_HARD)
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(
        message.chat.id,
        'Выбери уровень сложности: Легкий, Средний, Сложный',
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

    def send_question(index):
        if index >= len(questions_for_level):
            bot.send_message(chat_id, 'Викторина завершена! Чтобы пройти ещё раз, напишите /restart')
            return

        current_question = questions_for_level[index]
        bot.send_message(chat_id, current_question['question'])

        @bot.message_handler(content_types=['text'])
        def wait_for_answer(msg):
            answer = msg.text.strip().lower()
            if answer == current_question['answer'].lower():
                bot.send_message(msg.chat.id, 'Правильно!')
            else:
                bot.send_message(msg.chat.id, 'Неверно. Правильный ответ: {}'.format(current_question['answer']))

            # Переходим к следующему вопросу
            send_question(index + 1)

        bot.register_next_step_handler_by_chat_id(chat_id, wait_for_answer)

    # Начинаем с первого вопроса
    send_question(0)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)