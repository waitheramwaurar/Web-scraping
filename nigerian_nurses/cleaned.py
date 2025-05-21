import re
import pandas as pd
from scrape import fetch_raw_anpa_members

# Paste your scraped text between the triple quotes

paragraph_contents = fetch_raw_anpa_members()

raw_data = '\n'.join(paragraph_contents)

lines = [line.strip() for line in raw_data.splitlines() if line.strip()]
entries = []
current_entry = {"Name": "", "Email": "", "Address": "", "Website": ""}

for line in lines:
    # If line contains an email
    if re.match(r"[^@]+@[^@]+\.[^@]+", line):
        current_entry["Email"] = line
    # If line contains a website
    elif re.match(r"(www\.|http)", line) or ".com" in line:
        current_entry["Website"] = line
    # If line likely to be a name (contains MD, DPM, etc.)
    elif re.search(r"\b(MD|DPM|DDS|FAAP|FACS|MPH|MBA|BDS|RPVI|FACP|FCCP|DABAM|DipABLM|FAAFP|AAHIVS)\b", line):
        if current_entry["Name"]:  # Save previous entry if name is already filled
            entries.append(current_entry)
            current_entry = {"Name": "", "Email": "", "Address": "", "Website": ""}
        current_entry["Name"] = line
    else:
        # Assume this is part of the address
        if current_entry["Address"]:
            current_entry["Address"] += " " + line
        else:
            current_entry["Address"] = line

# Append the last entry
if current_entry["Name"]:
    entries.append(current_entry)

# Create DataFrame
df = pd.DataFrame(entries)
print(df)

# Export to Excel
df.to_excel("members.xlsx", index=False)
