from bs4 import BeautifulSoup
import requests

'''
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''

# we basically want to do dfs
# this is functionally similar through printing all words in
# in a Trie

# The 2 file types that indicate leaf nodes are
# - .txt files
# - .json files

root_url = 'https://www.smogon.com/stats/'

# April 27, 2022 - 140826 files
file_count = 0

stack = [root_url]
while stack:
    top = stack.pop()
    r = requests.get(top)

    soup = BeautifulSoup(r.content, 'html.parser')
    branches = soup.find_all('a')

    for link in branches:
        ref = link.get('href')
        if ref != "../":
            if ref[-3:] == 'txt' or ref[-3:] == 'son':
                print(f'{top}{ref}')
                file_count += 1
            else:
                stack.append(f'{top}{ref}')

print(f'Total files scraped: {file_count}')
