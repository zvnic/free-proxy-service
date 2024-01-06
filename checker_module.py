import requests
import time


async def check_proxy(proxy_ip, proxy_port):
    proxy = {
        "http": f"http://{proxy_ip}:{proxy_port}",
        "https": f"https://{proxy_ip}:{proxy_port}"
    }

    url = "http://www.example.com"  # Замените на адрес, который вы хотите использовать для проверки

    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxy, timeout=10)
        end_time = time.time()

        response_time = end_time - start_time
        anonymity = check_anonymity(response)

        report = {
            "Proxy IP": proxy_ip,
            "Proxy Port": proxy_port,
            "Response Time (s)": response_time,
            "Anonymity": anonymity,
            "Status Code": response.status_code,
            "Headers": response.headers,
            "Content": response.text
        }

        return report

    except requests.RequestException as e:
        return {"error": str(e)}

def check_anonymity(response):
    # Ваш код для определения уровня анонимности на основе ответа
    # Это может включать анализ заголовков ответа или других параметров

    # Пример: проверка заголовка 'Via'
    if 'Via' in response.headers:
        return "Transparent"
    else:
        return "Anonymous"

# if __name__ == "__main__":
#     proxy_ip = "135.181.221.83"
#     proxy_port = "3128"
#     result = check_proxy(proxy_ip, proxy_port)
#
#     print(result)
