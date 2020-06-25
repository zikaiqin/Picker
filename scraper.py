import requests
import csv
from bs4 import BeautifulSoup

# name the output file
filename = 'IT'

# number of pages to scrape
no_pages = 51

arr = []

def getData(pageNo):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    # replace page numbers in the URL with '+str(pageNo)+'
    r = requests.get('https://www1.salary.com/Pharmaceuticals-Salaries.html?pageno='+str(pageNo)+'&view=compact', headers=headers)
    content = r.content
    soup = BeautifulSoup(content)

    names = []

    # HTML properties
    for a in soup.findAll('a', attrs={'class':'font-semibold'}):
        name = a.getText()
        if name is not (None or 'View More'):
            print(name)
            names.append(name)
    return names

for x in range(no_pages):
    arr += getData(x)

# print(arr)

with open(filename + '.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for role in arr:
        writer.writerow([role,''])