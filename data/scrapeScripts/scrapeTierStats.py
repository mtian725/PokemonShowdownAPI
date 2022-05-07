
from turtle import update


def generate_data(url, db):
    import requests
    import re

    r = requests.get(url)
    collection_name = url[29:-4]

    elo_regex = "(.+)-(\d+)$"
    elo = re.search(elo_regex, collection_name)

    collection = db[elo.group(1)]

    for line in r.iter_lines():
        line_str = line.decode('UTF-8')
        if line_str and line_str[1] == '|' and not line_str[3] == 'R':
            values = line_str[2:-2].split("|")

            ranking = int(values[0])
            name = values[1].strip()
            usage = round(float(values[2].strip()[:-1])/100, 5)
            raw_val = int(values[3])
            rating = int(elo.group(2))
            item = {
                "_id" : f'{name}-{rating}',
                "ranking" : ranking,
                "name" : name,
                "usage" : usage,
                "raw" : raw_val,
                "rating": rating
            }

            res = collection.update_one(
                {"_id" : item["_id"]},
                {"$set": item},
                upsert=True
            )
            print(elo.group(1), elo.group(2), res.upserted_id)                                

def parallel_generate_data(urls, dbname):
    import concurrent.futures, random
    
    random.shuffle(urls)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for url in urls:
            executor.submit(generate_data, url, dbname)

        executor.shutdown(wait=True)

def find_data(url):
    from bs4 import BeautifulSoup
    import requests

    output = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    branches = soup.find_all('a')
    for link in branches:
        ref = link.get('href')
        if ref[-3:] == 'txt':
            output.append(f'{url}{ref}')

    return output