from PyPDF2 import PdfReader
import os
import pandas as pd

df = pd.DataFrame()
df = df.columns({"Title": [] , "Authors": [] , "Date Published" :[], "Subject" : [] })

folder_path = "C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_pdfs"

# We will make all a loop for all of the pdfs:

for file in os.listdir(folder_path):
    if file.endswith(".pdf"):
        file_path = os.path.join(file, folder_path)

    # Iteriate over all the files and collect the metadata
    try:
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)
        meta = len(reader.metadata)
        print(f"Processing : {file}")
        print(f"Processing : (metadata)")

        #Collect all the metadata into lists 
        
        