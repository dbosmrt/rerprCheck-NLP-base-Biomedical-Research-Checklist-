
import requests
import pandas as pd

# URL for fetching 50k PMC IDs related to biomedical research
esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "pmc",
    "term": "biomedical research",
    "retmax": 50000
}

# Get the data from NCBI
response = requests.get(esearch_url, params=params)
response.raise_for_status()  # will raise an error if request failed
xml_text = response.text

# Extract IDs between <Id> and </Id>
pmc_ids = []
start_tag = "<Id>"
end_tag = "</Id>"

start = 0
while True:
    start = xml_text.find(start_tag, start)
    if start == -1:
        break
    start += len(start_tag)
    end = xml_text.find(end_tag, start)
    if end == -1:
        break
    pmc_id_num = xml_text[start:end].strip()
    if pmc_id_num.isdigit():
        pmc_ids.append("PMC" + pmc_id_num)

# Save to CSV — fixed path formatting
save_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\csv file\pmc_ids.csv"

# Ensure directory exists
import os
os.makedirs(os.path.dirname(save_path), exist_ok=True)

df = pd.DataFrame({"PMC_ID": pmc_ids})
df.to_csv(save_path, index=False)

print(f"Extracted {len(pmc_ids)} PMC IDs and saved to '{save_path}'")
