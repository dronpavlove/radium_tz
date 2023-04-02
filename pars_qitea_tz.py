import asyncio
import time
from aiohttp import ClientSession
import hashlib
from bs4 import BeautifulSoup as Soup


file_name_list = list()
file_hash_data = dict()


async def get_content(url, count=1):
    """
    Возвращает файл.html в случае удачного подключения к указанному url
    """
    async with ClientSession() as session:
        async with session.get(url=url) as response:
            if response.status == 200:
                file_name = f"data/{time.strftime('%X')}_{count}.html"
                file_name_list.append(file_name)
                with open(file_name, "w", encoding="utf-8") as f:
                    res = await response.text()
                    f.write(str(Soup(res, 'html.parser').find('head')))


async def main(count, url):
    """
    В соответствии с указанным колличеством выполняет направление в функцию
    get_content(url)
    """
    tasks = []
    for i in range(count):
        tasks.append(asyncio.create_task(get_content(url, i)))
    await asyncio.gather(*tasks)


def get_file_hash(file_path):
    """
    Подсчиттывает sha256 хэши файла
    """
    block_size = 65536
    file_hash = hashlib.sha256(file_path.encode('utf8'))
    with open(file_path, 'rb') as f:
        fb = f.read(block_size)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(block_size)
    file_hash_data[file_path] = file_hash.hexdigest()
    return file_hash.hexdigest()


if __name__ == "__main__":
    request_url = 'https://gitea.radium.group/radium/project-configuration'
    asyncio.run(main(count=3, url=request_url))
    for file in file_name_list:
        get_file_hash(file_path=file)
    print(file_hash_data)
