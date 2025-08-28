import os
from langchain_unstructured import UnstructuredLoader

# giving path for extracting the data from pdfs
pdf_folder = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_pdfs"

txt_folder_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\text files"

pdfs = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
print(f"All {len(pdfs)} was successfully collected.")

#create a loop for the pdfs
def txt_loader(files_to_process):
    for i, filename in enumerate(files_to_process):
        print(f"Processing {i+1}/{len(pdfs)} : {filename} ")
        
        try:
            file_path = os.path.join(pdf_folder, filename)

            #laod the ustructured loader
            loader = UnstructuredLoader(file_path, mode = "elements", strategy = "fast")
            doc = loader.load()

            full_text = "\n\n".join([d.page_content for d in doc if d.page_content])
            
            if not full_text.strip():
                print(f"No data found in  {filename}")
                continue

            # Now save the txt file into a folder
            text_path = os.path.join(txt_folder_path, filename.replace(".pdf", ".txt"))
            with open(text_path, "w", encoding = "utf-8") as f:
                f.write(full_text)
        except Exception as e:
            print(f"Error in processing the file {filename} : {e}")

            return 

txt_loader(pdfs)

