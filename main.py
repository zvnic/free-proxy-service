import asyncio
from aiohttp import web
import proxy_module  # Импортируем ваш модуль для работы с прокси
import checker_module

async def handler(request):
    working_proxies = await proxy_module.get_free_proxies()
    return web.json_response({"proxies": working_proxies})

async def check_proxy_handler(request):
    proxy_info = request.match_info['proxy_info']
    proxy_ip, proxy_port = proxy_info.split(":")
    result = await checker_module.check_proxy(proxy_ip, proxy_port)

    # Проверяем, есть ли ключ 'Headers' в результате
    if 'Headers' in result:
        # Преобразование CaseInsensitiveDict в обычный словарь
        result['Headers'] = dict(result['Headers'])
    else:
        result['Headers'] = {}

    return web.json_response(result)

async def periodic_check():
    while True:
        await asyncio.sleep(3)  # Периодичность проверки
        await proxy_module.get_free_proxies()  # Мы можем проигнорировать результат, так как он сохраняется внутри модуля

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # Запускаем периодическую проверку прокси в фоновом режиме
    loop.create_task(periodic_check())

    app = web.Application()
    app.router.add_get('/get_proxy', handler)
    app.router.add_get('/check_proxy/{proxy_info}', check_proxy_handler)

    # Запускаем веб-сервер
    web.run_app(app, port=8080)
