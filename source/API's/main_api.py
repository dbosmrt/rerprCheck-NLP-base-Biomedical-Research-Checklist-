import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pmc_id_api import fetch_pmc_ids
from pmc_pdf import get_pmcids_from_csv
from pmc_pdf import download_pdf_from_pmc



if __name__ == "__main__":
    fetch_pmc_ids() # Fetch PMC IDS and save it into a csv file
    
    csv_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_ids.csv"

    # Directory for downloaded PDF
    download_dir = os.path.join(os.getcwd(), "pmc_pdfs")
    os.makedirs(download_dir, exist_ok=True)

    # Set up Selenium (Chrome)
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True  # force download instead of opening in Chrome
    })
    service = Service(r"C:\path\to\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Extract PMCIDs
    pmc_ids = get_pmcids_from_csv(csv_path, pmc_column="PMC_ID")
    print(f"Found {len(pmc_ids)} PMCIDs in CSV")

    # Loop through and download
    for pmcid in pmc_ids:
        download_pdf_from_pmc(pmcid, download_dir)

    driver.quit()
    print(" All downloads complete.")
