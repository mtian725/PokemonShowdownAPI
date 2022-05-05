
import scrapeScripts.scrapeTierStats as scrapeTierStats
import scrapeScripts.scrapePkmnStats as scrapePkmnStats

def get_db():
    from pymongo import MongoClient
    from os import environ as env
    from dotenv import load_dotenv, find_dotenv
    import certifi

    load_dotenv(find_dotenv("config.env"))
    CONNECTION_STRING = env['ATLAS_URI']
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    return client[env['DB_NAME']]

def get_current_month(db):
    collections = db.list_collection_names()
    if collections:
        return collections[0][0:7]
    else:
        return ""

def get_latest_month():
    from bs4 import BeautifulSoup
    import requests

    root_url = 'https://www.smogon.com/stats/'
    r = requests.get(root_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    branches = soup.find_all('a')
    ref = branches[-1].get('href')

    return f'{root_url}{ref}'

def drop_old_collections(db):
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for col in db.list_collection_names():
            executor.submit(db.drop_collection, col)
        
        executor.shutdown(wait=True)
    print(f'Successfully dropped old data')
    

if __name__ == "__main__":
    dbname = get_db()
    print("Connected DB")
    
    root_url = get_latest_month()
    print("Got latest month")

    prev_month = get_current_month(dbname)
    if prev_month and root_url[-8:-1] != prev_month:
        drop_old_collections(dbname)

    tierUrls = scrapeTierStats.find_data(root_url)
    pkmnUrls = scrapePkmnStats.find_data(f'{root_url}moveset/')
    print("Got URLS")

    scrapeTierStats.parallel_generate_data(tierUrls, dbname)
    scrapePkmnStats.parallel_generate_data(pkmnUrls, dbname)
    print('Finished importing data')