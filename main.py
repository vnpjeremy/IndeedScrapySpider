from scrapy import cmdline
import os

file = "newOutput1.json"
cmd = "scrapy crawl indeedspider -o "
both = cmd + file
if os.path.isfile(file):
    os.remove(file)
cmdline.execute(both.split())
