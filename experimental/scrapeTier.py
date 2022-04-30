
import requests

'''
# https://docs.python-requests.org/en/latest/user/quickstart/
# https://stackoverflow.com/questions/16870648/python-read-website-data-line-by-line-when-available
# https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
'''
url = 'https://www.smogon.com/stats/2022-03/gen8uu-0.txt'
r = requests.get(url)

'''
Note: The data in the standard dataset as far as I can see follow the same trend 
The only time this breaks is when you go down the "chaos" or "monotype" folders
all the way down to the base. So like '*/chaos/chaos/*'
'''

'''
Usage % seems to match Raw %
not sure what is the difference between raw and real % are

As this is usage statistics, all that is imporant is % and ranking number

Just doing rank, pokemon, usage, and raw as following 
https://www.smogon.com/forums/threads/usage-stats-api.3661849/
'''

# can guarantee that the first 5 lines are not important
for line in r.iter_lines():
    line_str = line.decode('UTF-8')
    if line_str and line_str[1] == '|' and not line_str[3] == 'R':
        values = line_str[2:-2].split("|")

        ranking = values[0]
        pokemon = values[1]
        usage = values[2]
        raw = values[3]

        print(f'{ranking} : {pokemon} | Usage: {usage} | Raw: {raw}')