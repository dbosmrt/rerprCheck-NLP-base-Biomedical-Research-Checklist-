import pandas as pd
from pmc_api import fetch_pmc_xml
from unpaywall import open_access
from xml_praser import parse_xml

pmc_csv = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_ids.csv"
pmc_df = pd.read_csv(pmc_csv)

final_data = []

for pmc_id in pmc_df["PMC_ID"]:
    xml_text = fetch_pmc_xml(pmc_id)
    if xml_text is None:
        continue

    parsed_data = parse_xml(xml_text)
    if parsed_data is None or not parsed_data["DOI"]:
        print(f"No DOI found for {pmc_id}, Skipping...")
        continue

    final_data.append(parsed_data)
    print(f"{pmc_id} processed and Open access confirmed.")

# finally save the final csv
output_csv = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\data.csv"
pd.DataFrame(final_data).to_csv(output_csv, index = False)
print(f"\nFinished! Open Access papers saved to {output_csv}")