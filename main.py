import telebot
import sqlite3
from telebot import types

API_TOKEN = '5666003785:AAHIZskcV1ezi1b15iulfokSUU9tO12oBq8'

bot = telebot.TeleBot(API_TOKEN)
conn = sqlite3.connect('moment/identifier.sqlite', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, user_name_public: str, state: str):
    cursor.execute(
        'INSERT INTO user (user_id, user_name, user_surname, username, user_name_public, state) VALUES (?, ?, ?, ?, '
        '?, ?)',
        (user_id, user_name, user_surname, username, user_name_public, state))
    conn.commit()


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Как вас зовут?')
    bot.register_next_step_handler(msg, askAge)  # askSource


# Функция регистрации
def askAge(message):
    chat_id = message.chat.id
    text = message.text
    if text.isdigit():
        msg = bot.send_message(chat_id, 'Ник должен состоять из символов')
        bot.register_next_step_handler(msg, askAge)  # askSource
        return

    msg = bot.send_message(chat_id, 'Спасибо, я запомнил что вас зовут ' + text)
    us_text = message.text.strip()

    bot.send_message(message.chat.id, 'Ваше имя добавлено в базу данных! Теперь можете ознакомиться с рецептом /recipe')
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    us_name_public = us_text
    us_state = True

    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username,
                 user_name_public=us_name_public, state=us_state)


# функция для вывода рецептов
@bot.message_handler(commands=['recipe'])
def recipe(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Борщ")
    item2 = types.KeyboardButton("Шашлык")
    item3 = types.KeyboardButton("Пюре")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name}, выбери рецепт! ',
                     reply_markup=markup)

# функция для вывода рецептов
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Если юзер прислал 1, выдаем ему случайный факт
    if message.text.strip() == 'Борщ':
        answer = "Украинский борщ Украинский борщ в полной мере отражает характер кухни страны: суп этот сытный, ароматный, разноцветный, густой, невероятно вкусный. И, кстати, очень полезный, ведь в его состав входит большое количество корнеплодов и овощей. Плюс — зелень с чесноком в самом конце приготовления!  В общем, настоящий подарок и для души, и для тела. Многие не решаются взяться за приготовление украинского борща из-за длительности варки и большого количества тонкостей, которые необходимо учитывать. Спешим успокоить: наш вариант украинского борща довольно прост в исполнении, поэтому с ним справится даже тот, кто делает свои первые шаги к кулинарным вершинам"
    # Если юзер прислал 2, выдаем умную мысль
    elif message.text.strip() == 'Шашлык':
        answer = "Отличный способ замариновать свинину, чтобы она осталась сочной даже после томления на углях."
    elif message.text.strip() == 'Пюре':
        answer = "ИНСТРУКЦИЯ ПРИГОТОВЛЕНИЯ 45 МИНУТ РАСПЕЧАТАТЬ 1Очистите картошку, порежьте на большие куски, положите в кастрюлю, добавьте холодной воды и чайную ложку соли. Вода должна покрывать весь картофель. Доведите до кипения, потом убавьте огонь и варите 20-30 минут, пока картошка не станет мягкой. Слейте воду. 2Растопите масло в другой кастрюле на медленном огне, добавьте картошку и разомните ее — лопаткой или специальным приспособлением. Когда масло полностью впитается, медленно вливайте горячее молоко, все время помешивая смесь деревянной лопаткой. Попробуйте, посолите, если нужно. 3Подавайте сразу — или сохраняйте теплым."
    # Отсылаем юзеру сообщение в его чат
    else:
        answer = "Таких рецептов пока не существует("

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
