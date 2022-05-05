
def generate_data(url, db):
    import requests, re

    r = requests.get(url)
    collection_name = url[29:-4]

    if collection_name in db.list_collection_names():
        print(f'{collection_name} is already in the DB')
        return

    collection = db[collection_name]

    NUM_LINES_PER_BOX = 9

    # clock counters to 
    line_clock = 0
    usage_clock = 0
    c_and_c_switch = True

    dist_regex = "(.+) (\d+\.\d+)%"
    c_and_c_pkmn = ""

    pkmn = {}
    for line in r.iter_lines():
        line_str = line.decode('UTF-8').strip(" |")

        if line_str[0] == '+':
            line_clock += 1

            if line_clock % NUM_LINES_PER_BOX == 0:
                print(collection_name, pkmn)
                ## PUT INSERT INTO DB HERE


                pkmn = {}
        else:
            match line_clock % NUM_LINES_PER_BOX:
                case 1:
                    pkmn["_id"] = line_str

                case 2:
                    match usage_clock % 3:
                        case 0:
                            x = re.search("\d+", line_str)
                            pkmn["usage"] = {
                                "raw": int(x.group())
                            }
                        case 1:
                            x = re.search("\d.\d+", line_str)
                            pkmn["usage"]["avg_weight"] = float(x.group())
                        case 2:
                            x = re.search("\d+", line_str)
                            pkmn["usage"]["viability_ceiling"] = int(x.group())
                    usage_clock += 1

                case 3:
                    x = re.search(dist_regex, line_str)
                    if x:
                        pkmn["abilities"][x.group(1)] = round(float(x.group(2))/100, 5)
                    else:
                        pkmn["abilities"] = {}

                case 4:
                    x = re.search(dist_regex, line_str)
                    if x:
                        pkmn["items"][x.group(1)] = round(float(x.group(2))/100, 5)
                    else:
                        pkmn["items"] = {}

                case 5:
                    x = re.search(dist_regex, line_str)
                    if x:
                        pkmn["spreads"][x.group(1)] = round(float(x.group(2))/100, 5)
                    else:
                        pkmn["spreads"] = {}

                case 6:
                    x = re.search(dist_regex, line_str)
                    if x:
                        pkmn["moves"][x.group(1)] = round(float(x.group(2))/100, 5)
                    else:
                        pkmn["moves"] = {}

                case 7:
                    x = re.search(dist_regex, line_str)
                    if x:
                        pkmn["teammates"][x.group(1)] = round(float(x.group(2))/100, 5)
                    else:
                        pkmn["teammates"] = {}

                case 8:
                    if c_and_c_switch:
                        x = re.search("(.+) \d+\.\d+ \(.+\)", line_str)
                        if x:
                            c_and_c_pkmn = x.group(1)

                            c_and_c_switch = not c_and_c_switch
                        else:
                            pkmn["checks_and_counters"] = {}
                    else:
                        x = re.search("\((\d+\.\d+)% KOed \/ (\d+\.\d+)% switched out\)", line_str)
                        (KO, switched) = x.group(1, 2)
                        pkmn["checks_and_counters"][c_and_c_pkmn] = {
                            "KO": round(float(KO)/100, 3),
                            "switched": round(float(switched)/100, 3),
                        }
                    
                        c_and_c_switch = not c_and_c_switch

                case _:
                    print("something that should not happen")

def parallel_generate_data(urls, dbname):
    import concurrent.futures

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