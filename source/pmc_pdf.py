import os
import pandas as pd
import requests

def download_pdf(pmc_id, save_dir):
    os.makedirs(save_dir, exist_ok = True)

    url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/"

    try:
        response = requests.get(url, stream = True , timeout = 20)

        if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
            filepath = os.path.join(save_dir, f"{pmc_id}.pdf")
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            print(f"[+] PDF saved: {filepath}")
            return filepath
        else:
            print(f"[-] No PDF available for {pmc_id} (Status: {response.status_code})")
            return None
        
    except Exception as e:
        print(f"[!] Error downloading PDF for {pmc_id}: {e}")
        return None 
    

if __name__ == "__main__":
    pmc_csv = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_ids.csv"
    pmc_df = pd.read_csv(pmc_csv)

    pdf_output_dir = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\pdfs"

    for pmc_id in pmc_df["PMC_ID"]:
        download_pdf(pmc_id, pdf_output_dir)