#First import all of the loaders 
import os
import pandas as pd
import re
from langchain_unstructured import UnstructuredLoader

#Define the folder path
folder_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_pdfs"

#Create list to store all data
all_data = []

#Get all the files from the folder
all_pdfs = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
print(f"Got all the pdf files from {folder_path}")

def pdf_praser(all_pdfs):
    for i, filename in enumerate(all_pdfs):
        print(f"Processing {i+1}/len{all_pdfs} : {filename}")

        try:
            file_path = os.path.join(folder_path, filename)
            loader = UnstructuredLoader(file_path, mode= "elements", strategy = "fast")
            document = loader.lazy_load()

            full_text = "\n\n".join([doc.page_content for doc in document])

            if not full_text:
                print(f"Error in Processing {filename}")
                continue

            doi = ""
            doi_match = re.search(r'10\.\d{4}/[^\s\n]+', full_text)
            if doi_match:
                doi = doi_match.group()

            title = ""
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            for line in lines[:5]:
                if 10< len(line) < 200:
                    title = line
                    break

            abstract = "" 
            abstract_match = re.search(r'(?i)abstract[:\s]+(.*?)(?=\n.*?(introduction|method|background))', full_text, re.DOTALL)
            if abstract_match:
                abstract = abstract_match.group(1).strip()
            
            introduction = ""
            introduction_match = re.search(r'(?i)introduction[s]?[:\s]+(.*?)(?=\n.*?(material|method|result|discussion))', full_text, re.DOTALL)
            if introduction_match:
                introduction = introduction_match.group(1).strip()

            
            material = ""
            material_match = re.search(r'(?i)material[s]?[:\s]+(.*?)(?=\n.*?(method|result|discussion))', full_text, re.DOTALL)
            if material_match:
                material = material_match.group(1).strip()

            methodology = ""
            methodology_match = re.search(r'(?i)method[s]?[:\s]+(.*?)(?=\n.*?(result|discussion|conclusion))', full_text, re.DOTALL)
            if methodology_match:
                methodology = methodology_match.group(1).strip()

            results = ""
            result_match = re.search(r'(?i)results?[:\s]+(.*?)(?=\n.*?(discussion|conclusion|reference))', full_text, re.DOTALL)
            if result_match:
                results = result_match.group(1).strip()[:500]
        
        # Find conclusion (text after "conclusion" word)
            conclusion = ""
            conclusion_match = re.search(r'(?i)conclusion[s]?[:\s]+(.*?)(?=\n.*?(reference|acknowledge))', full_text, re.DOTALL)
            if conclusion_match:
                conclusion = conclusion_match.group(1).strip()[:500]
        
        # Find authors (simple pattern)
            authors = ""
            author_match = re.search(r'(?i)authors?[:\s]+([^\n]+)', full_text[:1000])
            if author_match:
                authors = author_match.group(1).strip()
        
        # Find keywords (simple pattern)
            keywords = ""
            keyword_match = re.search(r'(?i)keywords?[:\s]+([^\n]+)', full_text)
            if keyword_match:
                keywords = keyword_match.group(1).strip()
        
        # Store data in dictionary
            paper_data = {
                'pdf_name': filename,
                'doi': doi,
                'title': title,
                'authors': authors,
                'keywords': keywords,
                'abstract': abstract,
                'introduction': introduction,
                'methodology': methodology,
                'results': results,
                'conclusion': conclusion,
                'text_length': len(full_text),
                'status': 'success'
            }
        
            all_data.append(paper_data)
            print(f"  ✓ Extracted data from {filename}")
        
        except Exception as e:
            print(f"  ✗ Error with {filename}: {e}")
            # Still add the file with error info
            all_data.append({
                'pdf_name': filename,
                'doi': '',
                'title': '',
                'authors': '',
                'keywords': '',
                'abstract': '',
                'introduction': '',
                'methodology': '',
                'results': '',
                'conclusion': '',
                'text_length': 0,
                'status': f'error: {e}'
            })
        
        # Save then in csv file
        output_file = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\parsed\parsed_data.csv"

        df = pd.DataFrame(all_data)
        df.to_csv(output_file, index = False)

        print("All the data is successfully extracted and saved into the pdf format.")

pdf_praser(all_pdfs)