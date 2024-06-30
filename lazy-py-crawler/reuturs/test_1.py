import requests

base = "https://www.wsj.com/market-data/quotes/company-list/country/united-states/"

headers = {
  "Host" : "www.wsj.com",
  "Referer" : "https://www.wsj.com",
  "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0",
  }

for i in range(1, 114):
  url = base + str(i)
  res = requests.get(url, allow_redirects=False, headers=headers)
  to_parse_html = res.text
  print(to_parse_html)