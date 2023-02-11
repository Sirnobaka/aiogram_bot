import asyncio
import time
import requests
import os
from aiohttp import ClientSession
import json


cocktail_api_token: str = os.getenv('CKOCKTAIL_API_TOKEN')
bot_token: str = os.getenv('CKOCKTAIL_BOT_TOKEN')
print(f'API token: {cocktail_api_token}')
print(f'Bot token: {bot_token}')

async def sleep_func():
    print('sleep function start')
    await asyncio.sleep(3)
    print('sleep function end')


# async def get_translation(text, source, target):
#     print('Translation start')
#     async with ClientSession() as session:
#         url = 'https://libretranslate.com/translate'
#         data = {'q': text, 'source': source, 'target': target, 'format': 'text'}

#         async with session.get(url, json=data) as response:
#             #translate_json = await response.json()
#             translation = await response.read()
#             print(translation)
#             translation_text = json.loads(translation)
#             print(translation_text)
#             try:
#                 #return translate_json['translatedText']
#                 return translation_text
#             except error:
#                 return error

async def coktail_by_ingredients(ingredients):
    ingredients_str = ','.join(ingredients)
    print(ingredients_str)
    async with ClientSession() as session:
        url = f'https://api.api-ninjas.com/v1/cocktail?ingredients={ingredients_str}'
        headers = {'X-Api-Key': cocktail_api_token}

        async with session.get(url=url, headers=headers) as response:
            coktail_json = await response.json()
            try:
                for cockt in coktail_json:
                    name = cockt['name']
                    ingredients_list = cockt['ingredients']
                    instructions = cockt['instructions']
                    print(f'### {name} ###')
                    for i in ingredients_list:
                        print(f' * {i}')
                    print(f'Instructions: {instructions}')
            except:
                print("Error:", response.status)

async def main():

    ingredients_list_en = ['bourbon', 'wine']

    task1 = asyncio.create_task(sleep_func())
    task2 = asyncio.create_task(coktail_by_ingredients(ingredients_list_en))

    await task1
    await task2


print(time.strftime('%X'))

asyncio.run(main())

print(time.strftime('%X'))
