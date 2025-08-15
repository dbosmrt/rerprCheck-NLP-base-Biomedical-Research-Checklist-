import requests
def open_access(doi):
    api_url = f"https://api.unpaywall.org/v2/{doi}?email=your_email@example.com"
    try: 
        response = requests(api_url, timeout = 10)
        if response.status_code == 200:
            data = response.jason()
            return data("is oa", False)
        else:
            print(f"Upaywall HTTP {response.data_status} {doi}")
            return False
    except Exception as e:
        print(f"Error checking DOI {doi} : {e}")
