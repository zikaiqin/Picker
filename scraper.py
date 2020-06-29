import requests
import csv
from bs4 import BeautifulSoup
import urllib

queue = []

# loads scraping targets from "filename".csv to the queue
# the first row should be formatted as follows: 'url', 'pageno', 'filename'
def loadFromFile(filename):
    global queue
    with open(filename + '.csv', encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        key = []
        hasKey = False
        for row in reader:
            if hasKey is False:
                key = row
                hasKey = True
                # print(key)
                if key != ['url', 'pageno', 'filename']:
                    return
            else:
                entry = dict(zip(key, row))
                entry['pageno'] = int(entry['pageno'])
                # print(entry)
                queue.append(entry)
    file.close()
    return

# replaces placeholder substring ('__pageno__') with the actual page number
def getUrl(notUrl, pageNo):
    url = notUrl.replace('__pageno__', str(pageNo))
    return url

# fetches all elements of type specified in the HTML properties
def fetchPage(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    r = requests.get(url, headers=headers)
    content = r.content
    soup = BeautifulSoup(content, features='html.parser')
    elements = []

    # HTML properties
    for a in soup.findAll('a', attrs={'class':'font-semibold'}):
        element = a.getText()
        if element is not None:
            # print(element)
            elements.append(element)
    return elements

# writes data to "filename".csv
def writeToFile(filename, data):
    with open(filename + '.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow([row])
    return

# scrapes the targeted site and outputs to the targeted file
def scrapeSite(entry):
    data = []
    print('\nScraping ' + entry['url'].split('?')[0] + '\n')
    for pageNo in range(entry['pageno']):
        url = getUrl(entry['url'], pageNo + 1)
        data += fetchPage(url)
        print('Page ' + str(pageNo + 1) + ' of ' + str(entry['pageno']) + '.')
    print('\n' + entry['url'].split('?')[0] + ' has been scraped.')
    data.sort()
    writeToFile(entry['filename'], data)
    return

# scrapes the entire queue
def scrape():
    global queue
    loadFromFile('input')
    for entry in queue:
        scrapeSite(entry)
    return

scrape()