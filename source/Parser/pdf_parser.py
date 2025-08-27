#First import all of the loaders 
import os
import pandas as pd
from langchain_unstructured import UnstructuredLoader

#Define the folder path
folder_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_pdfs"

#Create list to store all data
all_data = []

#Get all the files from the folder
all_pdfs = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
print(f"Got {len(all_pdfs)} pdf files from {folder_path}")

def pdf_praser(all_pdfs):
    for i, filename in enumerate(all_pdfs):
        print(f"Processing {i+1}/{len(all_pdfs)} : {filename}")

        try:
            file_path = os.path.join(folder_path, filename)
            loader = UnstructuredLoader(file_path, mode= "elements", strategy = "fast")
            document = loader.load()

            full_text = "\n\n".join([doc.page_content for doc in document])

            if not full_text:
                print(f"Error in Processing {filename}")
                continue
            
            all_data.append({"filename": filename, "pdf_text": full_text})
        
        except Exception as e:
            print(f"No content found in {filename}")
    
        
        # Save then in csv file
        output_file = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\parsed\parsed_data.csv"

        df = pd.DataFrame(all_data)
        df.to_csv(output_file, index = False, encoding= "utf-8")

        print("All the data is successfully extracted and saved into the pdf format.")

pdf_praser(all_pdfs)