import telebot
import config
import admins
from time import sleep
from database import database

# your token here
bot = telebot.TeleBot()


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != 'private':
        return
    bot.send_message(message.chat.id, "я вас категорически приветсвую! отправтье мне стикер и ответьте на него словом доступа (вот так:)")
    bot.send_photo(message.chat.id, open('instruction.png', 'rb'))
    print(message.from_user.username, "just started")


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
    if message.chat.type != 'private':
        return
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    clear_request = message.text.split()[1:]
    button1 = telebot.types.KeyboardButton("ДААААА!!!!")
    button2 = telebot.types.KeyboardButton("отмена")
    markup.add(button1, button2)
    text = f'{len(clear_request)} своих мемчиков' if len(clear_request) else 'все свои мемчики'
    msg = bot.send_message(message.chat.id, text=f'вы уверены, что хотите удалить {text} ?', reply_markup=markup)
    bot.register_next_step_handler(msg, clearing, clear_request)


def clearing(message, clear_request):
    print(clear_request)
    if message.chat.type != 'private':
        return
    if message.text == "ДААААА!!!!":
        Mydatabase.clear(message.from_user.username, clear_request if len(clear_request) > 0 else '')
        m = bot.send_message(message.chat.id, 'удалено')
        bot.delete_message(message.chat.id, m.id)
        sleep(1.5)
    else:
        m = bot.send_message(message.chat.id, 'отменено')
        sleep(1.5)
        bot.delete_message(message.chat.id, m.id)


@bot.message_handler(commands=['облизать'])
def start(message):
    try:
        a = int(message.text.split()[1])
        target = message.reply_to_message
        for i in range(a % 20):
            bot.send_sticker(message.chat.id, config.LICK, reply_to_message_id=target)
            sleep(0.5)
    except:
        bot.send_message(message.chat.id, 'я не понимаю что тут облизывать')


def send_mem(chat, id, type):
    if type == 'sticker':
        bot.send_sticker(chat, id)
    elif type == 'animation':
        bot.send_animation(chat, id)
    else:
        bot.send_photo(chat, id)


def get_id(message):
    if message.content_type == 'sticker':
        return message.sticker.file_id
    if message.content_type == 'animation':
        return message.animation.file_id
    return message.photo[0].file_id


# проверить, сушествует ли, если да: заменить или оставить, иначе: добавить
def solve_memexisting_conflict(message, mem):
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    button1 = telebot.types.KeyboardButton("заменить")
    button2 = telebot.types.KeyboardButton("отмена")
    markup.add(button1, button2)
    msg = bot.send_message(message.chat.id, text="такое слово уже что-то кодирует. заменить?", reply_markup=markup)
    bot.register_next_step_handler(msg, add_or_replace, message, mem)


def add_or_replace(newmessage, message, mem):
    id, type = mem
    if newmessage.text == 'отмена':
        m = bot.send_message(message.chat.id, 'отменено')
        sleep(1.5)
        bot.delete_message(message.chat.id, m.id)
    if newmessage.text == 'заменить':
        Mydatabase.replace(message.from_user.username, message.text, id, type)
        m = bot.send_message(message.chat.id, '👍')
        sleep(1.5)
        bot.delete_message(message.chat.id, m.id)


@bot.message_handler(content_types=['text'])
def buttin_message(message):
    if message.chat.type != 'private':
        return
    print(message.text, message.from_user.username)
    if message.reply_to_message is None:
        a = Mydatabase.get(message.from_user.username, message.text)
        if a[0] is None:
            bot.send_message(message.chat.id, 'теперь ответьте мемом на это сообщение')
            return
        send_mem(message.chat.id, a[0], a[1])
    else:
        if message.reply_to_message.content_type in ['sticker', 'animation', 'photo']:
            print(Mydatabase.get(message.from_user.username, message.text))
            if Mydatabase.get(message.from_user.username, message.text)[0] is None:
                Mydatabase.add(message.from_user.username, message.text, get_id(message.reply_to_message), message.reply_to_message.content_type)
                return
            solve_memexisting_conflict(message, (get_id(message.reply_to_message), message.reply_to_message.content_type))


@bot.message_handler(content_types=['sticker', 'animation', 'photo'])
def start(message):
    if message.reply_to_message is None:
        bot.send_message(message.chat.id, 'теперь ответьте сообщением на этот мем:')
        return
    if message.reply_to_message.content_type != 'text':
        bot.send_message(message.chat.id, 'это не текстом')
        return
    print("mem replyed to message")
    if Mydatabase.get(message.from_user.username, message.reply_to_message.text)[0] is None:
        Mydatabase.add(message.from_user.username, message.reply_to_message.text, get_id(message), message.content_type)
        return
    print('solving')
    solve_memexisting_conflict(message.reply_to_message, (get_id(message), message.content_type))


if __name__ == "__main__":
    Mydatabase = database()
    bot.polling()
