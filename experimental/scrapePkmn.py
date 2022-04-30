
import requests

url = 'https://www.smogon.com/stats/2022-03/moveset/gen8uu-0.txt'
r = requests.get(url)


NUM_LINES_PER_BOX = 9
line_clock = 0
# can guarantee that the first 5 lines are not important
for line in r.iter_lines():
    line_str = line.decode('UTF-8')
    
    if line_str[1] == '+':
        line_clock += 1
        print(line_str)
    else:
        match line_clock % NUM_LINES_PER_BOX:
            case 1:
                print(line_str, "Name")
            case 2:
                print(line_str, "UseCount")
            case 3:
                print(line_str, "Abilities")
            case 4:
                print(line_str, "Items")
            case 5:
                print(line_str, "Spreads")
            case 6:
                print(line_str, "Moves")
            case 7:
                print(line_str, "Teammates")
            case 8:
                print(line_str, "Checks and Counters")
            case _:
                print("something that should not happen")