import asyncio
import aiohttp
import threading

# Основной файл для атаки

async def  get_data(i: int, endpoint: str):
    url = f"http://127.0.0.1:8000/{endpoint}/{i}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f'Закончил выполнение {i}')

async def main():
    # await get_data(1,'async')
    await asyncio.gather(*[get_data(i, 'sync') for i in range(300)])
    # await asyncio.gather()

if __name__ == '__main__':
    asyncio.run(main())

# ручки сбросить в нужный файл

@app.get('/sync/{id}')
def sync_func(id: int):
    print('потоков: ',threading.active_count())
    print(f'sync. Start {id}: {time.time():.2f}')
    time.sleep(3)
    print(f'sync. Finish {id}: {time.time():.2f}')

@app.get('/async/{id}')
async def async_func(id: int):
    print(f'async. Start {id}: {time.time():.2f}')
    await asyncio.sleep(3)
    print('потоков: ', threading.active_count())
    print(f'async. Finish {id}: {time.time():.2f}')

