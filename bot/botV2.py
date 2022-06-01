import configg
import telebot
# Подключаем кнопки
from telebot import types

# Подключаем pyowm
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
#------------------------------------------------

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('c16d779e903477e532485d9034029c6f', config_dict)
mgr = owm.weather_manager()


name = ''
surname = ''
age = 0
place = ''

bot = telebot.TeleBot(configg.token)


@bot.message_handler(content_types=["photo"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Классная картинка, мне нравится)')

@bot.message_handler(content_types=["gif"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Мемная гифка')

@bot.message_handler(content_types=["voice"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Напиши пожалуйста')

@bot.message_handler(content_types=["document"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'Оу щищ, зачем мне это?')

@bot.message_handler(commands=['start'])
def ku(message):
    keyboard = types.InlineKeyboardMarkup()
    # Делаем кнопку со ссылкой
    btn = types.InlineKeyboardButton(text='Мой Господин', url='https://vk.com/voodi4ka')
    # Добавляем кнопку в клавиатуру
    keyboard.add(btn)
    bot.send_message(message.chat.id, 'Привет, если хочешь начать, напиши "Погнали!", а если не хочешь начинать,я буду повторять за тобой! ', reply_markup=keyboard)

@bot.message_handler(content_types =['text'])
def welcome(message):
    if message.text == 'Погнали!' or message.text == 'погнали!' or message.text == 'погнали' or message.text == 'Погнали':
        mesg = bot.send_message(message.chat.id,'Как тебя зовут? ')
        bot.register_next_step_handler(mesg,get_name)
    elif message.text == 'Погода' or message.text == 'погода':
        mesg = bot.send_message(message.chat.id,'В каком городе вы хотите узнать погоду? ')
        bot.register_next_step_handler(mesg, Pogoda)
    elif message.text == 'Привет' or message.text == 'привет':
        bot.send_message(message.chat.id, 'Кукусики')
    elif message.text == 'Как дела?' or message.text == 'как дела?' or message.text == 'как дела' or message.text == 'Как дела':
        bot.send_message(message.chat.id, 'Хорошо, а у тебя?')
    elif message.text == 'хорошо' or message.text == 'Хорошо' or message.text == 'Отлично' or message.text == 'отлично':
        bot.send_message(message.chat.id, 'Я рад за тебя)))')
    elif message.text == 'плохо' or message.text == 'Плохо' or message.text == 'ужасно' or message.text == 'Ужасно':
        bot.send_message(message.chat.id, 'Это грустно :(')
    else:
        bot.send_message(message.chat.id, message.text)


def Pogoda(message):
    global place
    global w
    global temp
    global max_temp
    global min_temp
    global feel_like
    global status
    global wind
    place = message.text
    observation = mgr.weather_at_place(place)
    w = observation.weather
    temp = w.temperature('celsius')['temp']
    max_temp = w.temperature('celsius')['temp_max']
    min_temp = w.temperature('celsius')['temp_min']
    feel_like = w.temperature('celsius')['feels_like']
    status = w.detailed_status
    wind = w.wind()['speed']
    mesg = bot.send_message(message.chat.id,'Сегодня в городе - ' + place + ' ' + '- температура воздуха' + ' ' + str(temp) + ' градусов по цельсию, ' + 'ощущается как '+ str(feel_like) + ' градусов по цельсию, ' + status +', порывы ветра достигают ' + str(wind) + ' м/с. Если хотите узнать погоду в другом городе, напишите название города, если не хотите напишите "Выход"')
    bot.register_next_step_handler(mesg, Vihod)

def Vihod(message):
    if message.text != 'Выход' and message.text != 'выход':
        Pogoda(message)
    else:
        mesgag = bot.send_message(message.chat.id, 'Выхожу в главное меню')
        bot.register_next_step_handler(mesgag, welcome)

def check(message):
    mesg = bot.send_message(message.chat.id, 'Как твое имя? ')
    bot.register_next_step_handler(mesg, get_name)

def get_name(message):
    global name
    name = message.text
    mesg = bot.send_message(message.chat.id,'Хорошо, а как твоя фамилия?')
    bot.register_next_step_handler(mesg, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    mesg = bot.send_message(message.chat.id, 'Сколько тебе лет? ')
    bot.register_next_step_handler(mesg, get_age)

def get_age(message):
    global age
    age = str(message.text)

    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебя зовут '+ surname +' '+ name + ' ' + 'и тебе ' +  age + ' ' + 'лет ' + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        mesg = bot.send_message(call.message.chat.id, name + ' если хочешь узнать погоду в интересующем тебя городе, напиши "Погода"')
        bot.register_next_step_handler(mesg, welcome)
    elif call.data == "no":
        mesg = bot.send_message(call.message.chat.id, 'Давай сначала! Как твое имя? ')
        bot.register_next_step_handler(mesg, get_name)


if __name__ == '__main__':
    bot.infinity_polling()
