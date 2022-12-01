import telebot

bot = telebot.TeleBot('5913562494:AAE1L323FB8mFBpDgxRIhYZxVufZb_eaUx0')


@bot.message_handler(content_types=['text'])
def lalala(message):
    bot.send_message(message.chat.id, message.text)
    print(message.chat.id)


bot.polling(none_stop=True)