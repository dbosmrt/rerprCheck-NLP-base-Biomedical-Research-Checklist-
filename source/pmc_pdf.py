import os
import requests

# Base URL
base_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/"

def download_pdf(pmc_id, output_dir = "pdfs"):
    os.makedirs(output_dir, exist_ok=True)

    url = f"{base_url}{pmc_id}/pdf/"

    try:
        response = requests.get(url, timeout=20)

        if response.status_code==200 and response.headers.get("Content-Type")== "application/pdf":
            filepath = os.path.join(output_dir, f"{pmc_id}.pdf")
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"[+] PDF saved: {filepath}")
            return filepath
        else:
            print(f"[-] No PDF available for {pmc_id}")
            return None
        
    except Exception as e:
        print(f"[!] Error downloading PDF for {pmc_id} : {e}")
        return None 