from html.parser import HTMLParser
from bs4 import BeautifulSoup
import requests
import csv
import ast

class Parser(HTMLParser):
    def __init__(self):
        self.tags = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        self.tags.append({'tag':tag, 'attrs':attrs})

    def get(self):
        return self.tags

class Picker:
    def __init__(self, filename = 'input.csv'):
        self.queue = []
        self.ifname = filename

    def loadFile(self, filename = None):
        if filename is None:
            filename = self.ifname
        if not filename.endswith('.csv'):
            filename += '.csv'
        try:
            with open(filename, encoding = 'utf-8-sig', newline = '') as file:
                reader = csv.reader(file, delimiter = ',')
                key = []
                for row in reader:
                    if not key:
                        key = row
                        if key != ['url', 'tags', 'filename', 'args']:
                            print(key)
                            raise Exception('invalid formatting of the document.')
                    else:
                        entry = dict(zip(key, row))
                        entry['tags'] = self.parseTags(entry['tags'])
                        entry['args'] = self.parseArgs(entry['args'])
                        self.queue.append(entry)
        except Exception:
            raise
        except FileNotFoundError:
            raise
        else:
            file.close()

    def writeFile(self, filename, data):
        if not filename.endswith('.csv'):
            filename += '.csv'
        with open(filename, 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        file.close()

    def parseTags(self, rawTags):
        parser = Parser()
        try:
            elements = ast.literal_eval(rawTags)
        except:
            pass
        else:
            if type(elements) is not list:
                raise TypeError('string does not resolve to list.')
            tags = []
            for element in elements:
                parser.feed(element)
                parser.close()
                tags.append(parser.get())
                parser = Parser()
            return tags
        parser.feed(rawTags)
        parser.close()
        tags = parser.get()
        return tags
    
    def parseArgs(self, rawArgs):
        args = {}
        if rawArgs:
            args = ast.literal_eval(rawArgs)
        return args

    def fetchTree(self, url):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        try:
            r = requests.get(url, headers = headers, allow_redirects = False)
            if 300 <= r.status_code < 600:
                raise Exception(str(r.status_code))
        except:
            raise
        else:
            content = r.content
            tree = BeautifulSoup(content, features = 'html.parser')
            return tree

    def findElements(self, tree, tags):
        elements = []
        if type(tags[0]) is not dict:
            for tag in tags:
                if not elements:
                    elements = self.findElements(tree, tag)
                else:
                    temp = []
                    for old, new in zip(elements, self.findElements(tree, tag)):
                        temp.append([old[0], new[0]])
                    elements = temp
        else:
            next_ = tags[1:]
            for element in tree.findAll(tags[0].get('tag'), attrs = tags[0].get('attrs')):
                if next_:
                    elements.extend(self.findElements(element, next_))
                else:
                    elements.append(self.handleElement(element))
        return elements

    def handleElement(self, tree):
        tag = tree.name
        text = tree.getText().strip()
        if tag == 'a':
            href = tree.get('href')
            return [text, href]
        elif tag == 'img' or tag == 'video':
            src = tree.get('src')
            return [text, src]
        else:
            return [text]

    def scrape(self, entry):
        url = entry['url']
        args = entry['args']
        data = []
        print('\nNow scraping ' + url.split('?')[0])
        if 'range' in args:
            if 'append' not in args or len(args['range']) > 2:
                print('Exception: Invalid arguments used.')
                return
            if len(args['range']) == 2:
                begin = args['range'][0]
                end = args['range'][1] + 1
                try:
                    for index in range(begin, end):
                        newUrl = url + args['append'].replace('^R', str(index))
                        try:
                            tree = self.fetchTree(newUrl)
                        except:
                            raise
                        else:
                            data += self.findElements(tree, entry['tags'])
                except Exception as e:
                        print('Exception: ' + str(e) + ' for page ' + str(index) + '.')
                        print(str(index - begin) + ' of ' + str(end - begin) + ' pages scraped.\n')
                else:
                    print(str(end - begin) + ' of ' + str(end - begin) + ' pages scraped.\n')
            else:
                index = args['range'][0]
                while True:
                    newUrl = url + args['append'].replace('^R', str(index))
                    try:
                        tree = self.fetchTree(newUrl)
                    except:
                        break
                    else:
                        data += self.findElements(tree, entry['tags'])
                        index += 1
                print(str(index - 1) + ' pages scraped.\n')
        elif 'append' in args:
            url += args['append']
            try:
                tree = self.fetchTree(url)
            except Exception as e:
                print('Exception: Status code ' + str(e) + '.')
            else:
                data += self.findElements(tree, entry['tags'])
                print('Page scraped.\n')
        else:
            try:
                tree = self.fetchTree(url)
            except Exception as e:
                print('Exception: Status code ' + str(e) + '.')
            else:
                data += self.findElements(tree, entry['tags'])
                print('Page scraped.\n')
        data.sort()
        self.writeFile(entry['filename'], data)

    def scrapeAll(self):
        if not self.queue:
            self.loadFile()
        for entry in self.queue:
            self.scrape(entry)
        self.queue.clear()