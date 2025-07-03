import json
from html2text import html2text
import requests
from bs4 import BeautifulSoup

url = "https://www.singtel.com/personal/products-services/mobile/roaming/faqs"

# get info from URL
response = requests.get(url, timeout=5)
response.raise_for_status()
html_content = response.text

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'lxml')

# search for FAQ page specific component 
texts = soup.find_all('div',class_="sd-component-addon-accordion-singtel aem-GridColumn aem-GridColumn--default--12")

# parse & prepare dictionary for FAQs
faqs = {}
for idx,text in enumerate(texts):
    # find specific subcomponent
    x = text.find_all('div',class_="widget-instance")[0] 
    
    # prep question
    q = x.find_all('ux-addon-accordion')[0].attrs
    qn = json.loads(q['datamodel'])['accordionTitle'].strip()

    # prep answer
    a = x.find_all('ux-heading-text')[0].attrs
    ans = html2text(json.loads(a['datamodel'])['text']).strip()

    # update
    faqs.update({idx:{'q':qn,'a':ans}})

with open('./faqs.json','w') as f:
    json.dump(faqs, f)       