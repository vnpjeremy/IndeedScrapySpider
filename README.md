# IndeedScrapySpider
Spider for scraping Indeed jobs web domain
This crawler works by using seed regions (e.g., Washington, California, etc) and parsing their results domain to generate candidate follow pages.

A lot of it is fairly manual and I'm sure could be done multitudes better...after all, I'm a C++ programmer with precious little Python experience. Things work well so far. Functions exist to pare down results in categories of job title, date since posted, and keyword inclusion/exclusion for the followed html page.

Each candidate primary page is composed of 1)Normal job results and 2)Sponsored job results. Care can be taken to view these accordingly if necessary. Note the strangeness in dealing with company title strings. The website (Indeed.com) is coded incorrectly and yields non-repeatable behavior, which is why you'll see the branch condition in saving that particular string. Company hyperlink status is volatile based on loading/reloading of identical pages.

Be wary in using regex word boundaries in conjunction with special characters, such as "C++". For reasons yet unknown to me, these tend to present difficulty when used in tandem.

Output is defaulted to a .csv file readable by Excel.

Required python packages:
Python 2.7
scrapy framework
BeautifulSoup
html2text
