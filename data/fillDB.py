import scrapeScripts.scrapeTierStats as scrapeTierStats

def get_db():
    from pymongo import MongoClient
    from os import environ as env
    from dotenv import load_dotenv, find_dotenv
    import certifi

    load_dotenv(find_dotenv("config.env"))
    CONNECTION_STRING = env['ATLAS_URI']
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    return client[env['DB_NAME']]

if __name__ == "__main__":
    dbname = get_db()
    print("Connected DB")
    
    urls = scrapeTierStats.find_data()
    print("Got URLS")

    scrapeTierStats.parallel_generate_data(urls, dbname)
    print('Finished importing data')