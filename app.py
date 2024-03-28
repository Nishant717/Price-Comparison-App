# from bs4 import BeautifulSoup
# import requests
# import os
# import json
# from pydantic import BaseModel
# from typing import Optional
# from fastapi import FastAPI

# app = FastAPI()

# class Products(BaseModel):
#     id : Optional[int] = None
#     title : str
#     Price : int
#     Rating : float


# product_name = input("Enter the product name: ")

# print('Enter the minimum price of product:')
# product_price = float(input('=>'))
# print('Enter the minimum rating from the customer:')
# product_review = float(input('=>'))

# url = f'https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
# html_text = requests.get(url).text
# soup = BeautifulSoup(html_text, 'html.parser')

# maintags = soup.find_all('div', class_='_4ddWXP')

# product_data = []

# for index, maintag in enumerate(maintags):
#     price_text = maintag.find('div', class_='_30jeq3').text
#     price = int(price_text.replace('₹', '').replace(',', ''))
#     if price >= product_price:
#         name = maintag.find('a', class_='s1Q9rs').text
#         rating_element = maintag.find('div', class_='_3LWZlK')

#         if rating_element is not None:
#             rating = float(rating_element.text)
#             if rating >= product_review:
#                 product = {
#                     'id': index + 1,
#                     'title': name,
#                     'Price': price_text, 
#                     'Rating': rating
#                 }
#                 product_data.append(product)

# # Write the earpod data to a JSON file
# output_file = 'product_data.json'
# with open(output_file, 'w') as f:
#     json.dump(product_data, f, indent=4)

# print(f'Output merged into file: {output_file}')


from bs4 import BeautifulSoup
import requests
import os
import json
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

class Product(BaseModel):
    id: int
    title: str
    price: int
    rating: float

@app.get("/products/")
async def get_products(product_name: str, min_price: Optional[float] = None, min_rating: Optional[float] = None):
    url = f'https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    maintags = soup.find_all('div', class_='_4ddWXP')

    product_data = []

    for index, maintag in enumerate(maintags):
        price_text = maintag.find('div', class_='_30jeq3').text
        price = int(price_text.replace('₹', '').replace(',', ''))
        if min_price is None or price >= min_price:
            name = maintag.find('a', class_='s1Q9rs').text
            rating_element = maintag.find('div', class_='_3LWZlK')
            if rating_element is not None:
                rating = float(rating_element.text)
                if min_rating is None or rating >= min_rating:
                    product_data.append(Product(id=index + 1, title=name, price=price, rating=rating))

    return product_data


# http://127.0.0.1:8000/products/?product_name=earpods&min_price=1000&min_rating=4.0
