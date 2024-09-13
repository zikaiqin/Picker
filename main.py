from picker import Picker
import sys

def main():
    args = sys.argv[1:]
    if len(args) == 3:
        if args[2].lower() in ['true', 't', 'yes', 'y', 'slow']: args[-1] = True
        else: args[2] = False
    scraper = Picker(*args)
    scraper.loadFile()
    scraper.scrapeAll()

if __name__ == '__main__':
    main()
