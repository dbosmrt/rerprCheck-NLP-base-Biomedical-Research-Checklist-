import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def is_valid_pmcid(pmcid: str) -> bool:
    return bool(re.match(r"^PMC\d+$", pmcid))


def get_pmcids_from_csv(csv_path, pmc_column="PMC_ID"):
   
    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="latin1")  

    if pmc_column not in df.columns:
        raise ValueError(f"CSV does not have a column named '{pmc_column}'")

    valid_pmcids = [
        str(pmc).strip()
        for pmc in df[pmc_column].tolist()
        if is_valid_pmcid(str(pmc).strip())
    ]
    return valid_pmcids


def download_pdf_from_pmc(pmcid, download_dir):

    url = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/pdf/"

    try:
        driver.get(url)
        time.sleep(2)  # wait for page load

        try:
            pdf_button = driver.find_element(By.LINK_TEXT, "PDF")
            pdf_url = pdf_button.get_attribute("href")

            driver.get(pdf_url)
            time.sleep(3)  # wait for PDF to load

            print(f" Downloaded {pmcid}")
            return True
        except NoSuchElementException:
            print(f" No PDF found for {pmcid}")
            return False

    except Exception as e:
        print(f" Error with {pmcid}: {e}")
        return False



if __name__ == "__main__":
    
    csv_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_id.csv"

    # Directory for downloaded PDF
    download_dir = os.path.join(os.getcwd(), "pmc_pdfs")
    os.makedirs(download_dir, exist_ok=True)

    # Set up Selenium (Chrome)
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True  # force download instead of opening in Chrome
    })
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Extract PMCIDs
    pmc_ids = get_pmcids_from_csv(csv_path, pmc_column="PMC_ID")
    print(f"Found {len(pmc_ids)} PMCIDs in CSV")

    # Loop through and download
    for pmcid in pmc_ids:
        download_pdf_from_pmc(pmcid, download_dir)

    driver.quit()
    print(" All downloads complete.")
