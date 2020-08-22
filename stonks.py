import telebot
from telebot import TeleBot, types
from random import randint
import requests
import time
from requests.auth import HTTPBasicAuth

answer = requests.get('http://stonks.goto.msk.ru/api/robot/stocks/', auth=HTTPBasicAuth('fathutnik', 'Superpapa1'))

token = ""
# Обходим блокировку с помощью прокси
# telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
# подключаемся к телеграму
bot = telebot.TeleBot(token=token)

pictures = {
    0: "https://avatars.mds.yandex.net/get-zen_doc/1661927/pub_5e5010916617c37cfdda1c23_5e501233f2bc623242237b29/scale_1200",
}
states = {}
inventories = {}
user_id = []
state = 1
real_news_ad = []
ans = None
login = 'fathutnik'


@bot.message_handler(commands=["start"])
def start_game(message):
    user = message.chat.id
    user_id.append(message.from_user.id)
    states[user] = 0
    inventories[user] = []
    print(user_id[0])
    bot.send_message(user, "Добро пожаловать")

    process_state(user, states[user], inventories[user])


def process_state(user, state, inventory):
    kb = types.ReplyKeyboardMarkup()

    bot.send_photo(user, pictures[state])
    ans, login, password = check_activate()
    #print(ans, login, password)
    if ans:
        state = 1
    else:
        state = 1

    if state == 0:
        kb.add(types.KeyboardButton(text="Новости"))
        kb.add(types.KeyboardButton(text="Купить продать "))
        kb.add(types.KeyboardButton(text="Подписаться на рассылку с ценами"))
        bot.send_message(user, "Что вы хотите сделать?", reply_markup=kb)
    if state == 1:
        kb.add(types.KeyboardButton(text="Цены"))
        kb.add(types.KeyboardButton(text="Купить продать "))
        kb.add(types.KeyboardButton(text="Подписаться на рассылку с ценами"))
        kb.add(types.KeyboardButton(text="Войти"))
        bot.send_message(user, "Что вы хотите сделать?", reply_markup=kb)


@bot.message_handler(content_types=['text'])
def process_answer(message):
    a = []
    user = message.chat.id
    kb = types.ReplyKeyboardMarkup()

    if message.text == 'Купить продать':
        kb.add(types.KeyboardButton(text="Купить"))
        kb.add(types.KeyboardButton(text="Продать"))
        kb.add(types.KeyboardButton(text="Назад"))
        bot.send_message(user, 'Выберите дейстиве', reply_markup=kb)
        # if message.text == 'Купить':

    if message.text == 'Подписаться на рассылку с ценами':
        bot.send_message(user, 'Выберите дейстиве', reply_markup=kb)

    if '#stonksAD' in message.text:
        real_news_ad.append(message.text.replace('#stonksAD', ''))
        print(real_news_ad)
    if '#stonksPJ' in message.text:
        real_news_ad.append(message.text.replace('#stonksAD', ''))
        print(real_news_ad)
    if '#stonks' in message.text:
        real_news_ad.append(message.text.replace('#stonksAD', ''))
        print(real_news_ad)
    if '#stonksAD' in message.text:
        real_news_ad.append(message.text.replace('#stonksAD', ''))
        print(real_news_ad)

    if message.text == 'Цены':
        for l in get_info(login,password):
            bot.send_message(user, l, reply_markup=kb)

    if message.text == 'Войти':
        kb.add(types.KeyboardButton(text="У меня есть акк"))

        kb.add(types.KeyboardButton(text="Назад"))
        bot.send_message(user, 'Зарегистрируйтесь ' + 'https://stonks.goto.msk.ru/register', reply_markup=kb)

    if message.text == 'Назад':
        return process_state(user, state=0, inventory=1)

''''
def login_get(message):
    chat_id = message.chat.id
    login = message.text

    password_req = bot.send_message(chat_id, "Мудила, шли пароль!")
    bot.register_next_step_handler(password_req, password_get)

def password_get(message):
    chat_id = message.chat.id
    password = message.text

'''''

# функции обработки
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def check_password(login, password):
    a = requests.get('http://stonks.goto.msk.ru/api/robot/stocks/', auth=HTTPBasicAuth(login, password))
    a = a.json()
    try:
        if a['detail'] == 'Недопустимые имя пользователя или пароль.':
            return False
        else:
            return True
    except:
        return True

def add_password(login, password,message):
    chat_id = message.chat.id
    text = message.text
    tg_id = user_id[0]
    a = str(tg_id) + ' ' + str(login) + ' ' + str(password) + ' '
    f = open('passwords.txt', 'a')
    f.write(a)
    f.close()
    bot.send_message(chat_id, text)



def check_activate():
    answer = []
    print(user_id[0])
    tg_id = user_id[0]

    f = open('passwords.txt', 'r')
    ans = f.read()
    f.close()
    ans = ans.split()
    for i in range(len(ans) // 3):
        answer.append([ans[3 * i], ans[3 * i + 1], ans[3 * i + 2]])
    res = [False, '', '']
    for el in answer:
        if el[0] == tg_id:
            res = (True, el[1], el[2])
            break
    return res


def get_info(login, password):
    answer = requests.get('http://stonks.goto.msk.ru/api/robot/stocks/', auth=HTTPBasicAuth(login, password))
    answer = answer.json()
    ans = []
    for el in answer:
        el['price'] = round(el['price'], 3)
        ans.append(el['price'])
    return ans


def write_price(ans):
    a = ''
    for el in ans:
        a += str(el) + ' '
    f = open('price.txt', 'w')
    f.write(a)
    f.close()


def read_price():
    f = open('price.txt', 'r')
    ans = f.read()
    f.close()
    ans = ans.split()
    for i in range(len(ans)):
        ans[i] = int(ans[i][2:]) / (10 ** 3) + int(ans[i][:1])
    return ans


def changed_price(login, password):
    old_price = read_price()
    new_price = get_info(login, password)
    n = len(old_price)
    res = [None] * n
    c_0 = 0
    for i in range(n):
        res_i = (new_price[i] * 100 / old_price[i]) - 100
        if res_i == 0:
            c_0 += 1
        res[i] = res_i
        print(new_price[i], old_price[i], res_i)
    if c_0 == n:
        return (False, res)
    else:
        return (True, res)


def buy_act(login, password, course, number):
    ans = requests.get('http://stonks.goto.msk.ru/api/robot/stocks/', auth=HTTPBasicAuth(login, password))
    ans = ans.json()
    ID = ans[course]['id']
    answer = requests.get('http://stonks.goto.msk.ru/api/robot/stocks/' + ID + '/buy?number=' + number,
                          auth=HTTPBasicAuth(login, password))
    answer = answer.json()
    return answer


def sell_act(login, password, course, number):
    ans = requests.get('http://stonks.goto.msk.ru/api/robot/stocks/', auth=HTTPBasicAuth(login, password))
    ans = ans.json()
    ID = ans[course]['id']
    answer = requests.get('http://stonks.goto.msk.ru/api/robot/stocks/' + ID + '/sell?number=' + number,
                          auth=HTTPBasicAuth(login, password))
    answer = answer.json()
    return answer


def get_balance(login, password):
    answer = requests.get('http://stonks.goto.msk.ru/api/robot/balance/', auth=HTTPBasicAuth(login, password))
    answer = answer.json()
    return round(answer['balance'], 3)


bot.polling(none_stop=True)
