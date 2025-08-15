import requests
import time 

# Lets create a function for prasing xml of the papers. 
def fetch_pmc_xml(pmc_id, sleep_time = 0.34):
    try:
        base_url =  f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/{pmc_id}/unicode"
        response = requests.get(base_url)
        if response.status_code == 200:
            time.sleep(sleep_time)
            return response.text
        else:
            print(f"Skipping {pmc_id} (HTTP {response.status_code})")
            return None
    except Exception as e:
        print(f"Error in Fetching {e}")
        return None
    