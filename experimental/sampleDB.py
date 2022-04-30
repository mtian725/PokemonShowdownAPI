
def addSampleData(collection):
    # this is taken from datascrape.py
    import requests

    url = 'https://www.smogon.com/stats/2022-03/gen8uu-0.txt'
    r = requests.get(url)

    # can guarantee that the first 5 lines are not important
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
            
            collection.insert_one(item)

def get_database():
    from pymongo import MongoClient
    import certifi
    from os import environ as env
    from dotenv import load_dotenv, find_dotenv

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    load_dotenv(find_dotenv("config.env"))
    CONNECTION_STRING = env['ATLAS_URI']

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[env['DB_NAME']]
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    

    # Get the database
    dbname = get_database()
    collection_name = "2022-03/gen8uu-0"

    if collection_name in dbname.list_collection_names():
        print(f'{collection_name} is already in the DB')
    else:
        collection = dbname["2022-03/gen8uu-0"]
        addSampleData(collection)