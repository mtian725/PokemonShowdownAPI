
import requests
import re

'''
https://www.smogon.com/forums/threads/weighted-stats-faq.3478570/
- What "weight" means in context of the stats
https://www.smogon.com/forums/threads/viability-ceiling-a-measure-of-how-far-a-pokemon-can-take-you.3546373/
- What viability ceiling is
'''

url = 'https://www.smogon.com/stats/2022-03/moveset/gen8uu-0.txt'
r = requests.get(url)


NUM_LINES_PER_BOX = 9

# clock counters to 
line_clock = 0
usage_clock = 0
c_and_c_switch = True

dist_regex = "(.+) (\d+\.\d+)%"
nature_ev_regex = "(\w+):(\d+)\/(\d+)\/(\d+)\/(\d+)\/(\d+)\/(\d+)"
c_and_c_pkmn = ""

pkmn = {}
for line in r.iter_lines():
    line_str = line.decode('UTF-8').strip(" |")

    if line_str[0] == '+':
        line_clock += 1

        if line_clock % NUM_LINES_PER_BOX == 0:
            print(pkmn)
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
                    usage = round(float(x.group(2))/100, 5)
                    nature_evs = re.search(nature_ev_regex, x.group(1))
                    if nature_evs:
                        pkmn["spreads"].append({
                            "nature": nature_evs.group(1),
                            "hp": nature_evs.group(2),
                            "atk": nature_evs.group(3),
                            "def": nature_evs.group(4),
                            "spatk": nature_evs.group(5),
                            "spdef": nature_evs.group(6),
                            "speed": nature_evs.group(7),
                            "usage": usage,
                        })
                    else:
                        pkmn["spreads"].append({
                            "nature": "Other",
                            "usage": usage,
                        })
                else:   
                    pkmn["spreads"] = []

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