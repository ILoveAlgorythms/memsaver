import telebot
import config as g
import json
import admins
from time import sleep

bot = telebot.TeleBot(g.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='отправьте команду огурец в анусе, чтобы очистить клавиатуру')


@bot.message_handler(commands=['log'])
def start(message):
    if message.from_user.username in admins.admins:
        if message.reply_to_message is None:
            bot.send_message(message.chat.id, 'чтобы получить информацию о сообщении, ответьте на него командой log')
        else :
            bot.send_message(message.chat.id, message.reply_to_message)


@bot.message_handler(commands=['огурецванусе'])
def start(message):
    markup=telebot.types.ReplyKeyboardRemove(selective=True)
    bot.send_message(message.chat.id, text='очищено', reply_to_message_id = message, reply_markup=markup)
    

@bot.message_handler(commands=['date'])
def start(message):
    if message.from_user.username in admins.admins:
        if message.reply_to_message is None:
            bot.send_message(message.chat.id, 'чтобы получить информацию о времени отправки сообщения, ответьте на него командой date')
        else :
            bot.send_message(message.chat.id, message.reply_to_message.date)



@bot.message_handler(commands=['help'])
def buttin_message(message):
    bot.send_message(message.chat.id, 'я пока тут всё отключил потому что мне лень чето придумывать')
#    with open("documentation.txt", 'r', encoding='utf-8') as file:
#        bot.send_message(message.chat.id, '\n'.join(file.readlines()))


@bot.message_handler(commands=['clear'])
def start(message):
    if message.chat.type != 'group':
        markup = telebot.types.ReplyKeyboardMarkup(True, True)
        button1 = telebot.types.KeyboardButton("ДААААА!!!!")
        button2 = telebot.types.KeyboardButton("отмена")
        markup.add(button1, button2)
        msg = bot.send_message(message.chat.id, text="вы уверены, что хотите удалить все свои мемчики?", reply_markup=markup)
        bot.register_next_step_handler(msg, clearing)


def clearing(message):
    if message.chat.type != 'group':
        if message.text == "ДААААА!!!!":
            if message.chat.type != 'group':
                filename = "data/" + message.from_user.username + ".json"
                with open(filename, 'w') as file:
                    json.dump(dict({'0': 0}), file, indent=2)
                bot.send_message(message.chat.id, 'удалено')
        else:
            bot.send_message(message.chat.id, 'отменено')


@bot.message_handler(commands=['облизать'])
def start(message):
    try:
        a = max(int(message.text.split()[1]), 3)
        target = message.reply_to_message
        for i in range(a % 20):
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIBumOGbPj-h9-iM893t0t9i2Djv0D_AAKhIgACJ8rhSwXjseyK27zDKwQ', reply_to_message_id=target)
            sleep(0.5)
    except:
        bot.send_message(message.chat.id, 'я не понимаю что тут облизывать')



@bot.message_handler(content_types=['text'])
def buttin_message(message):
    print(message.from_user.username)
    if message.from_user.username == 'Xattta6bI4':
        bot.send_message(message.chat.id, 'готовь попку, @Xattta6bI4')
    if (message.chat.type != 'group') and (not (message.text.startswith('/')))

if __name__ == "__main__":
    bot.polling()

