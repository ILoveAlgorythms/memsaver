import telebot
import config as g
import json
import admins
from time import sleep

bot = telebot.TeleBot(g.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "я вас категорически приветсвую! отправтье мне стикер и ответьте на него словом доступа (вот так:)")
    bot.send_photo(message.chat.id, open('instruction.png', 'rb'))
    with open("data/" + message.from_user.username + ".json", "w", encoding='utf-8') as file:
        json.dump(dict({0: 0}), file, indent=2)
    print(message.chat.id)


@bot.message_handler(commands=['log'])
def start(message):
    if message.from_user.username in admins.admins:
        bot.send_message(message.chat.id, message.reply_to_message)



@bot.message_handler(commands=['help'])
def buttin_message(message):
    with open("documentation.txt", 'r', encoding='utf-8') as file:
        bot.send_message(message.chat.id, '\n'.join(file.readlines()))


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
    if message.text == "ДААААА!!!!":
        filename = "data/" + message.from_user.username + ".json"
        with open(filename, 'w') as file:
            json.dump(dict({'0': 0}), file, indent=2)
        bot.send_message(message.chat.id, 'удалено')
    else:
        bot.send_message(message.chat.id, 'отменено')


@bot.message_handler(commands=['облизать'])
def start(message):
    try:
        a = int(message.text.split()[1])
        target = message.reply_to_message
        for i in range(a):
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIBumOGbPj-h9-iM893t0t9i2Djv0D_AAKhIgACJ8rhSwXjseyK27zDKwQ', reply_to_message_id=target)
            sleep(0.5)
    except:
        bot.send_message(message.chat.id, 'я не понимаю что тут облизывать')



@bot.message_handler(content_types=['text'])
def buttin_message(message):
    if not message.text.startswith('/'):
        print(message.text)
        filename = "data/" + message.from_user.username + ".json"
        if message.reply_to_message is None:
            with open(filename, "r") as file:
                a = json.load(file)
            if message.text in a.keys():
                try:
                    bot.send_sticker(message.chat.id, a[message.text])
                except:
                    bot.send_photo(message.chat.id, a[message.text])

            else:
                bot.send_message(message.chat.id, 'такого слова ещё не было. ответьте мемом на ваше сообщение чтобы добавить')
        else:
            if message.reply_to_message.content_type in ['sticker', 'animation', 'photo']:
                with open(filename, "r", encoding='utf-8') as file:
                    a = json.load(file)
                if message.text in a.keys():
                    markup = telebot.types.ReplyKeyboardMarkup(True, True)
                    button1 = telebot.types.KeyboardButton("добавить")
                    button2 = telebot.types.KeyboardButton("заменить")
                    markup.add(button1, button2)

                    msg = bot.send_message(message.chat.id, text="такое слово уже существует. добавить или заменить?", reply_markup=markup)
                    bot.register_next_step_handler(msg, add_or_repace, filename, message)
                else:
                    if message.reply_to_message.content_type == 'sticker':
                        a[message.text] = message.reply_to_message.sticker.file_id
                    elif message.reply_to_message.content_type == 'animation':
                        a[message.text] = message.reply_to_message.animation.file_id
                    elif message.reply_to_message.content_type == 'photo':
                        a[message.text] = message.reply_to_message.photo[0].file_id

                with open(filename, "w", encoding='utf-8') as file:
                    json.dump(a, file, indent=2)
            elif message.reply_to_message.content_type == "animation":
                print('animation,', message.from_user.username)
            else:
                bot.send_message(message.chat.id, message.reply_to_message)


def add_or_repace(message, filename, oldmessage):
    if message.text == 'добавить':#допилить!!!!!!!!!!!
        bot.send_message(message.chat.id, 'я пока не добавил это, но это обязательно будет')
    if message.text == 'заменить':
        with open(filename, 'r') as file:
            b = json.load(file)
        loc = oldmessage.reply_to_message.content_type
        if loc == 'sticker':
            b[oldmessage.text] = oldmessage.reply_to_message.sticker.file_id
            print(b[oldmessage.text], "_____")
        elif loc == 'animation':
            b[oldmessage.text] = oldmessage.reply_to_message.animation.file_id
        # elif loc == 'photo':
        #     b[oldmessage.text] = oldmessage.reply_to_message.photo.file_id
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(b, file, indent=2)


@bot.message_handler(content_types=['sticker', 'animation'])
def start(message):
    filename = "data/" + message.from_user.username + ".json"

    if message.reply_to_message is None:
        bot.send_message(message.chat.id, 'теперь ответьте сообщением на этот мем:')
    else:
        if message.reply_to_message.content_type == 'text':
            print("sticker replyed to message")
            with open(filename, "r") as file:
                a = json.load(file)
            print(message.text)

            if message.content_type == 'sticker':
                a[message.reply_to_message.text] = message.sticker.file_id
            elif message.content_type == 'animation':
                a[message.reply_to_message.text] = message.animation.file_id
            # elif message.content_type == 'photo':
            #     a[message.reply_to_message.text] = message.photo.file_id
            with open("data/" + message.from_user.username + ".json", "w", encoding='utf-8') as file:
                json.dump(a, file, indent=2)
        else:
            bot.send_message(message.chat.id, 'это не сообщение')
    #bot.send_sticker(message.chat.id, message.sticker.file_id)


if __name__ == "__main__":
    bot.polling()

