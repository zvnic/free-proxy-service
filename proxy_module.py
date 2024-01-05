import asyncio
import os
import time
import aiohttp
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

async def get_free_proxies():
    url = config.get('proxy', 'url')
    proxy_file = config.get('proxy', 'proxy_file')
    checked_proxy_file = config.get('proxy', 'checked_proxy_file')
    check_interval = config.getint('proxy', 'check_interval')

    # Проверяем, был ли файл proxy_check.txt обновлен в последние 5 минут
    if os.path.exists(checked_proxy_file) and (time.time() - os.path.getmtime(checked_proxy_file)) < check_interval:
        print(f"Прошло менее {check_interval} с последнего обновления. Используем существующие проверенные прокси.")
        return get_proxies_from_file(checked_proxy_file)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                with open(proxy_file, "w") as file:
                    file.write(content)
                print(f"Прокси успешно получены и сохранены в файл: {proxy_file}")

                proxy_list = get_proxies_from_file(proxy_file)
                working_proxies = await check_proxies(session, proxy_list)

                if working_proxies:
                    print(f"Всего рабочих прокси: {len(working_proxies)}")

                    # Сохраняем проверенные и доступные прокси в файл
                    with open(checked_proxy_file, "w") as checked_file:
                        checked_file.write("\n".join(working_proxies))

                    return working_proxies
                else:
                    print("Нет рабочих прокси.")
                    return []
            else:
                print(f"Не удалось получить содержимое файла. Код состояния: {response.status}")
                return []


async def check_proxy(session, proxy):
    try:
        async with session.get("http://www.example.com", proxy=f"http://{proxy}", timeout=5) as response:
            if response.status == 200:
                return True
            else:
                return False
    except Exception as e:
        return False


async def check_proxies(session, proxy_list):
    tasks = [check_proxy(session, proxy) for proxy in proxy_list]
    results = await asyncio.gather(*tasks)
    working_proxies = [proxy for proxy, result in zip(proxy_list, results) if result]

    return working_proxies


def get_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies
