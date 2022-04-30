
def generate_data(url, db):
    import requests

    r = requests.get(url)
    collection_name = url[29:-4]

    if collection_name in db.list_collection_names():
        print(f'{collection_name} is already in the DB')
        return

    collection = db[collection_name]

    for line in r.iter_lines():
        line_str = line.decode('UTF-8')
        if line_str and line_str[1] == '|' and not line_str[3] == 'R':
            values = line_str[2:-2].split("|")

            ranking = int(values[0])
            name = values[1].strip()
            usage = round(float(values[2].strip()[:-1])/100, 5)
            raw_val = int(values[3])

            item = {
                "ranking" : ranking,
                "_id" : name,
                "usage" : usage,
                "raw" : raw_val
            }

            print(collection_name, item)
            collection.insert_one(item)

def parallel_generate_data(urls, dbname):
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(generate_data, url, dbname))

        executor.shutdown(wait=True)

def find_data():
    from bs4 import BeautifulSoup
    import requests

    root_url = 'https://www.smogon.com/stats/'

    routes = []
    r = requests.get(root_url)

    soup = BeautifulSoup(r.content, 'html.parser')
    branches = soup.find_all('a')
    for link in branches:
        ref = link.get('href')

        # only 2022-03 just for storage reasons
        # add to the predicate or remove for more months of data
        if ref != "2022-03/":
            continue

        if ref != "../":
            routes.append(f'{root_url}{ref}')

    output = []
    for route in routes:
        r = requests.get(route)

        soup = BeautifulSoup(r.content, 'html.parser')
        branches = soup.find_all('a')
        for link in branches:
            ref = link.get('href')
            if ref[-3:] == 'txt':
                output.append(f'{route}{ref}')

    return output