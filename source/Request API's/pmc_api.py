import requests
import pandas as pd
import time 
import xml.etree.ElementTree as ET

# Load the csv file
input_csv = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_ids.csv"
pmc_df = pd.read_csv(input_csv)

# Lets create a function for prasing xml of the papers. 
meta_list = []
# Loop through PMC ID
for pmc_id in pmc_df["PMC_ID"]:
    try:
        # Get API url
        base_url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/{pmc_id}/unicode"
        response = requests.get(base_url, timeout= 10)
        if response.status_code != 200:
            print(f"Skipping{pmc_id} (HTTP {response.status_code})")
            continue

        # Now Prase XML
        root = ET.fromstring(response.text)

        # Extract the desired metadata
        title = ""
        authors = []
        date = ""
        license_use = ""
        can_use = "No"

        for infon in root.iter("infon"):
            key = infon.attrib.get("key", "").lower()
            if key == "title":
                title = infon.text or ""
            elif key == "authors":
                authors.append(infon.text or "")
            elif key == "publication date":
                date = infon.text or ""
            elif key == "license":
                license_use = infon.text or ""
                if any(keyword in license_use.lower() for keyword in ["cc-by", "cc0", "public domain", "cc by", "cc-by-4.0"] ):
                    can_use = "Yes"
        meta_list.append({
            "PMC ID" : pmc_id,
            "Title" : title,
            "Authors" : ";" .join(authors),
            "Publication Date" : date,
            "License" : license_use, 
            "Can Use" : can_use
        })
        print(f"Processed {pmc_id}")
        # Sleep to avoid NCBI blocking
        time.sleep(0.34)  # ~3 requests/sec limit
    except Exception as e:
        print(f"Error Processing {pmc_id}: {e}")


output_csv = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_metadata.csv"
pd.DataFrame(meta_list).to_csv(output_csv, index=False)

print(f"Metadata extraction complete. Saved to {output_csv}")
