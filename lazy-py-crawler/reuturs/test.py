import time
from selenium import webdriver
from lxml import html
# Start the Selenium web driver
import json


def get_description(url):
    driver.get(url)
    # Get the HTML content from the page
    html_content = driver.page_source

    # Parse the HTML using lxml
    tree = html.fromstring(html_content)

    # Find all p tags inside the div element with class body-content teaser-content__388dc739
    p_tags = tree.xpath('//div[@class="body-content teaser-content__388dc739"]//p')

    # Print the text content of each p tag
    desc = []
    for p_tag in p_tags:
        desc.append(p_tag.text_content())
    # Close the Selenium web driver
    return ' '.join(desc)


options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# Load the URL with a delay of 2 seconds
url = "https://www.bloomberg.com/lineup-next/api/paginate?id=story_list_2&page=economics-v2&offset=0"
driver.get(url)
time.sleep(2)

# Get the JSON data from the page
json_data = driver.execute_script("return JSON.parse(document.body.innerText)")
data = json_data.get('story_list_2')
nextItemOffset = data['nextItemOffset']

items = data['items']

# Print the headlines and publication dates
data_save = []
for item in items:
    headline = item['headline']['text']
    publishedAt = item['publishedAt']
    author = item['byline']
    url = item['url']
    data_save.append({'title':headline,'author':author,'publishedAt':publishedAt,'url': url})

# Loop through all pages until there are no more pages to load
while nextItemOffset is not None:
    # Make the next page URL and send a request
    next_url = 'https://www.bloomberg.com/lineup-next/api/paginate?id=story_list_2&page=economics-v2&offset={}'.format(nextItemOffset)
    driver.execute_script("window.location.href = '{}';".format(next_url))
    time.sleep(2)

    # Get the JSON data from the page and extract the required information
    json_data = driver.execute_script("return JSON.parse(document.body.innerText)")
    data = json_data.get('story_list_2')
    nextItemOffset = data['nextItemOffset']
    items = data['items']


    # Print the headlines and publication dates from the current page
    for item in items:
        headline = item['headline']['text']
        publishedAt = item['publishedAt']
        author = item['byline']
        url = item['url']
        data_save.append({'title':headline,'author':author,'publishedAt':publishedAt,'url': url})

json_data = json.dumps(data_save)

with open('data.json', 'w') as f:
    f.write(json_data)

# Close the Selenium web driver
driver.quit()


