import asyncio
from aiohttp import web
import proxy_module  # Импортируем ваш модуль для работы с прокси

async def handler(request):
    working_proxies = await proxy_module.get_free_proxies()
    return web.json_response({"proxies": working_proxies})

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

    # Запускаем веб-сервер
    web.run_app(app, port=8080)
