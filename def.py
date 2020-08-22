import requests
from requests.auth import HTTPBasicAuth

login = ''
password = ''


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


def add_password(login, password):
    tg_id = '0'
    a = str(tg_id) + ' ' + str(login) + ' ' + str(password) + ' '
    f = open('passwords.txt', 'a')
    f.write(a)
    f.close()


def check_activate():
    answer = []
    tg_id = '0'
    f = open('passwords.txt', 'r')
    ans = f.read()
    f.close()
    ans = ans.split()
    for i in range(len(ans) // 3):
        answer.append([ans[3 * i], ans[3 * i + 1], ans[3 * i + 2]])
    res = [False, '', '']
    for el in answer:
        if el[0] == tg_id:
            res = [True, el[1], el[2]]
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
    return round(answer['balance'], 4)


add_password('1', '1')
add_password('2', '2')
print(check_activate())