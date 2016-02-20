from scrapy import cmdline
import os

file = "newOutput.csv"
cmd = "scrapy crawl indeed_spider -o "
both = cmd + file
if os.path.isfile(file):
    os.remove(file)
cmdline.execute(both.split())
