import requests
import threading
import json
import time

start = time.perf_counter()
semaphore = threading.Semaphore(20)


def fetch_data(product_id, products_list):
    url = f"https://dummyjson.com/products/{product_id}"
    try:
        with semaphore:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            products_list.append(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for product {product_id}: {e}")


products = []
threads = []

for product_id in range(1, 101):
    thread = threading.Thread(target=fetch_data, args=(product_id, products))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end = time.perf_counter()

products_dict = {"products": products}

with open('products.json', 'w') as file:
    json.dump(products_dict, file, indent=2)

print("All products fetched and saved to 'products.json'")
print("Needed time to fetch and save the data:", end - start)
