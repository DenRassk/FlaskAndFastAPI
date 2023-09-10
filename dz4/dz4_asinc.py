"""
Пример передачи аргументов через командную строку:
python dz4_asinc.py --urls https://wow.blizzwiki.ru/images/b/b4/Warcraft_III_TFT_Blood_Elf_Human_Campaign.jpg
следующие URL перечисляются через пробел!!!
"""


import asyncio
import aiohttp
import time
import argparse
import os

URLS = [
    'https://thenerdstash.com/wp-content/uploads/2023/03/the-x-files.jpg',
    'https://wow.blizzwiki.ru/images/8/8a/Warcraft_III_TFT_Scourge_Undead_Campaign.jpg',
    'https://i.pinimg.com/736x/c6/41/72/c64172cfc8f8908d06e731999c8ab195.jpg',
    'https://wow.blizzwiki.ru/images/b/b4/Warcraft_III_TFT_Blood_Elf_Human_Campaign.jpg',
    'https://www.lenbaget.ru/wp-content/uploads/2021/11/full_20387.jpg'
]

start_func_time = time.time()
if not os.path.exists('images'):
    os.makedirs('images')


async def img_saver(url):
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        async with session.get(url) as response:
            cont = await response.read()
            filename = f'{url.split("/")[-1]}'
            with open(f'images/{filename}', 'wb') as f:
                f.write(cont)
                print(f'Файл: {filename} загружен за {(time.time() - start_time):.2f} секунд')


async def main():
    tasks = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs="+")
    args = parser.parse_args()
    if not args.urls:
        args.urls = URLS
    for url in args.urls:
        task = asyncio.ensure_future(img_saver(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f'Время загрузки всех файлов: {(time.time() - start_func_time):.2f} секунд')
