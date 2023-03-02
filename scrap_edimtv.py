import requests
from bs4 import BeautifulSoup
import json

# url = 'https://www.edim.tv/cocktails/'
# page = requests.get(url)

# coctail_url_list = []

# print('status =', page.status_code)

# soup = BeautifulSoup(page.content, 'lxml')
# # ссылка на карточку коктейля находится в объекте класса "post-img"
# coctail_cards = soup.find_all(class_="post-img")

# собираем ссылки на карточки с коктейлями (комментирую это после выполнения 1 раз)
# for card in coctail_cards:
#     count += 1
#     card_url = card.get('href')
#     print(card_url)
#     coctail_url_list.append(card_url)

# и записываем их в файл
# with open('coctail_card_urls.txt', 'w') as file:
#     for line in coctail_url_list:
#         file.write(f'{line}\n')

###

url_prefix = "https://www.edim.tv"

with open('coctail_card_urls.txt', 'r') as file:
    cards = [card.strip() for card in file.readlines()]

    coctail_names = []
    coctail_recipes = []
    coctail_ingredients = []

    data_dict = []


    for card in cards:
        #print('\n'+'-'*50+'\n'+'-'*50+'\n')
        url_card = url_prefix + card
        print(url_card)
        q = requests.get(url_card)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')

        names_list = soup.find_all("h4", class_="info")
        ingredients_lsit = soup.find_all(class_="list-style")

        #print(f'coctail names = {len(names_list)}')
        #print(f'coctail ingredients = {len(ingredients_lsit)}')

        try:
            # Если коктейлей несколько
            if (len(names_list) > 0 and len(names_list) != 1):
                for name, ingredients in zip(names_list, ingredients_lsit):
                    name = name.text
                    coctail_names.append(name)
                    recipe_str = ingredients.text.strip()
                    coctail_recipes.append(recipe_str)
                    ingredients = ingredients.text.strip().split("\n")
                    components = []
                    for i in ingredients:
                        #print('*', i.strip())
                        #print('*', i.split('—')[0].strip())
                        components.append(i.split('—')[0].strip())
                    ingredients = ", ".join(components)
                    coctail_ingredients.append(ingredients)
                    data = {
                        'coctail_name': name,
                        'coctail_ingredients': ingredients,
                        'coctail_recipe': recipe_str
                    }
                    data_dict.append(data)
            # Если коктейль один и название в заголовке
            else:
                name = soup.find(class_="col-md-10").find('h1').text
                #print(f'### {name} ###')
                coctail_names.append(name)
                recipe_str = soup.find(class_="list-style").text.strip()
                coctail_recipes.append(recipe_str)
                recipe_list = recipe_str.split("\n")
                components = []
                for i in recipe_list:
                    #print('*', i.strip())
                    #print('*', i.split('—')[0].strip())
                    components.append(i.split('—')[0].strip())
                ingredients = ", ".join(components)
                coctail_ingredients.append(ingredients)

                data = {
                    'coctail_name': name,
                    'coctail_ingredients': ingredients,
                    'coctail_recipe': recipe_str
                }
                data_dict.append(data)
        except Exception as e:
            print(e)

    with open('data.json', 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)