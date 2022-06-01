import configg
import telebot
# Подключаем кнопки
from telebot import types

bot = telebot.TeleBot(configg.token)

name = '';
surname = '';
age = 0;

@bot.message_handler(commands=['start'])
def repeat_all_messages(message): # Название функции не играет никакой роли
    # Создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    # Делаем кнопку со ссылкой
    btn = types.InlineKeyboardButton(text = 'Мой папочка', url='https://vk.com/voodi4ka')
    # Добавляем кнопку в клавиатуру
    keyboard.add(btn)
    bot.send_message(message.chat.id, 'Привет! Я бот-повторюшка!', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == 'Привет' or message.text == 'привет':
        bot.send_message(message.chat.id, 'Кукусики')
    elif message.text == 'Как дела?' or message.text == 'как дела?' or message.text == 'как дела' or message.text == 'Как дела':
        bot.send_message(message.chat.id, 'Хорошо, а у тебя?')
    elif message.text == 'хорошо' or message.text == 'Хорошо' or message.text == 'Отлично' or message.text == 'отлично':
        bot.send_message(message.chat.id, 'Я рад за тебя)))')
    elif message.text == 'плохо' or message.text == 'Плохо' or message.text == 'ужасно' or message.text == 'Ужасно':
        bot.send_message(message.chat.id, 'Это грустно :(')
    else:
        bot.send_message(message.chat.id, message.text)

@bot.message_handler(content_types=["photo"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Классная картинка, мне нравится)')

@bot.message_handler(content_types=["gif"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Мемная гифка')

@bot.message_handler(content_types=["voice"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Напиши сука')

@bot.message_handler(content_types=["document"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'оу щит')



if __name__ == '__main__':
     bot.infinity_polling()