import telebot

# Вставьте сюда ваш токен от бота
API_TOKEN = '7320624649:AAEK3qDvTc4UzgeJi3uw9xGZA2fnt7FYuWI'

# Создаем объект бота
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def send_message(message):
    bot.reply_to(message, "Привет. И тебе всего хорошего!!!")

if __name__ == '__main__':
    # Запускаем бесконечный цикл обработки сообщений
    bot.polling()
