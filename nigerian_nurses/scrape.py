import requests
from bs4 import BeautifulSoup
from typing import List

def fetch_raw_anpa_members(url: str = 'https://www.anpantx.org/members-directory/'):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    one_half_md_elements = soup.select('.one_half-md')
    paragraph_contents = []

    for element in one_half_md_elements:
        paragraphs = element.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                paragraph_contents.append(text)

    return paragraph_contents

paragraph_contents = fetch_raw_anpa_members()

# print(paragraph_contents)

# for item in paragraph_contents:
#     print(item)

