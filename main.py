import os

from io import BytesIO
from telebot import *
import cv2

bot = telebot.TeleBot('5357548904:AAFMgLipUcPD8Eo5RSU3aCZwzEF12Odyi1M')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Face2model")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()

        key_about_todo = types.InlineKeyboardButton(text='What can this bot do?', callback_data='about_todo')
        keyboard.add(key_about_todo)

        key_about_author = types.InlineKeyboardButton(text='About author', callback_data='about_author')
        keyboard.add(key_about_author)
        key_about_sponsors = types.InlineKeyboardButton(text='About sponsors', callback_data='about_sponsors')
        keyboard.add(key_about_sponsors)

        key_todo = types.InlineKeyboardButton(text='Send photo', callback_data='todo')
        keyboard.add(key_todo)

        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Choose what do you want to know/do: ', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Type /start")
    else:
        bot.send_message(message.from_user.id, "I don't understand you. Type /help.")


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = "examples/inputs/" + file_id
    open(str(file_path) + ".jpg", 'wb').write(downloaded_file)

    abs_file = os.path.abspath(file_path) + ".jpg"

    bot.send_message(message.from_user.id, "Start converting!")

    os.system(f' python3 demo.py -f {abs_file} -o obj --show_flag=true --onnx;')

    bot.send_message(message.from_user.id, "Take your result!")

    file_to_send = f'examples/results/{file_id}_obj.obj'
    with open(file_to_send, 'rb') as tmp:
        file_obj = BytesIO(tmp.read())
        file_obj.name = 'result.obj'
        bot.send_document(message.from_user.id, file_obj)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "about_todo":
        msg = "I can convert your 2d photo of face into 3d model!"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "about_author":
        msg = "This bot was made by Mikhail Murunov"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "about_sponsors":
        msg = "This bot was sponsored by Digital Garage (Dubna)"
        bot.send_message(call.message.chat.id, msg)
    if call.data == "todo":
        msg = "Waiting..."
        bot.send_message(call.message.chat.id, msg)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

