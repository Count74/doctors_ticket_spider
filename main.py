import time
import plyer
import urllib3

URL = "https://kdcd.spb.ru/samozapis/doctors_lpu.php?docid=82&docname=%D0%9B%D0%B5%D0%B4%D0%B5%D0%BD%D1%86%D0%BE%D0%B2%D0%B0%20%D0%94.%20%D0%92.&cab=230"
TIMEOUT = 60
SEARCH_STRING = 'count_numbs_yellow'
STRING_COUNT = 2


def call_nady():
    plyer.notification.notify(
        message='Есть талоны на прием',
        app_name='Доктор, ау',
        app_icon='attention.ico',
        title='Надя, Ура', )

headers = {
    'Host': 'kdcd.spb.ru',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://kdcd.spb.ru/samozapis/speciality.php?flag=1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'Cookie': '_ym_d=1599208344; _ym_uid=1593414568137065628; PHPSESSID=1obc7ai9r0so6oq7cb41kuj354'
}


http = urllib3.PoolManager()
check_counter = 1
caught_counter = 0
ticked_caught_string = "и еще не было"

while True:
    print(f'Проверка талонов № {check_counter}')
    r = http.request('GET', URL, headers=headers)

    if r.status != 200:
        print(f'Не могу соединится с сервером, ошибка {r.status}')
    elif str(r.data).count(SEARCH_STRING) < STRING_COUNT:
        print(f'Ошибка парсинга')
    elif str(r.data).count(SEARCH_STRING) > STRING_COUNT:
        call_nady()
        print('Внимание, есть талоны!')
        caught_counter += 1
    else:
        if caught_counter:
            ticked_caught_string = f'но были {caught_counter} раз'
        print(f'Талонов нет, {ticked_caught_string}. Следущая проверка через {TIMEOUT} секунд.')
    check_counter += 1
    time.sleep(TIMEOUT)
