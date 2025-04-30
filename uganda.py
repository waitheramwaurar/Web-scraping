import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://mpsdb.parliament.go.ug"
data = []

def get_mp_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    info = {
        "Name": "",
        "Constituency": "",
        "District": "",
        "Political Party": "",
        "Profession/Occupation": "",
        "Marital Status": "",
        "Phone number": "",
        "Date of Birth": "",
        "Email": "",
        "Profile Link": url,
        "Image URL": ""
    }

    name_tag = soup.find('h5', class_='met-user-name')
    if name_tag:
        info["Name"] = name_tag.get_text(strip=True)

    table = soup.find('table')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                label = cells[0].get_text(strip=True).replace(":", "").upper()
                value = cells[1].get_text(strip=True)

                if "CONSTITUENCY" in label:
                    info["Constituency"] = value
                elif "DISTRICT" in label:
                    info["District"] = value
                elif "POLITICAL PARTY" in label:
                    info["Political Party"] = value
                elif "PROFESSION" in label:
                    info["Profession/Occupation"] = value
                elif "MARITAL STATUS" in label:
                    info["Marital Status"] = value
                elif "PHONE" in label:
                    info["Phone number"] = value
                elif "DATE OF BIRTH" in label:
                    info["Date of Birth"] = value
                elif "EMAIL" in label:
                    info["Email"] = value

    # img_tag = soup.find('img', src=True)
    # if img_tag and "identification_photos" in img_tag['src']:
    #     info["Image URL"] = img_tag['src']

    return info

# Loop through all 24 pages
for page in range(1, 25):
    print(f"Scraping list page {page}...")
    page_url = f"{base_url}/?page={page}"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags (the cards are wrapped in them)
    a_tags = soup.find_all('a', href=True)

    for a_tag in a_tags:
        # Look inside the <a> tag for a card body
        card_body = a_tag.find('div', class_='card-body text-center')
        if card_body:
            profile_link = base_url + a_tag['href']
            try:
                mp_data = get_mp_details(profile_link)
                data.append(mp_data)
                print(f"Scraped: {mp_data['Name']}")
            except Exception as e:
                print(f"Error scraping {profile_link}: {e}")
            time.sleep(0.5)

# Save data
df = pd.DataFrame(data)
# print(df)
df.to_csv("ugandan_mps.csv", index=False)
print("✅ Done! Check 'ugandan_mps.csv'")
