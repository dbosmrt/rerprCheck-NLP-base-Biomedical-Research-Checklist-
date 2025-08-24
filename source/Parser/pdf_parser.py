from PyPDF2 import PdfReader
import os
import pandas as pd

# Create empty DataFrame
df = pd.DataFrame({"File Name": [],"Title": [], "Authors": [], "Date Published": [], "Subject": []})

folder_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_pdfs"

# Lists to store metadata for all PDFs
filenames = [] 
titles = []
authors = []
dates = []
subjects = []

# Loop through all PDFs
for file in os.listdir(folder_path):
    if file.endswith(".pdf"):
        file_path = os.path.join(folder_path, file)
        
        # Process each file and collect metadata
        try:
            reader = PdfReader(file_path)
            num_pages = len(reader.pages)
            meta = reader.metadata
            
            print(f"Processing: {file}")
            print(f"Pages: {num_pages}")
            
            # Extract metadata safely (handle None values)
            title = meta.title if meta and meta.title else "Unknown"
            author = meta.author if meta and meta.author else "Unknown"
            creation_date = meta.creation_date if meta and meta.creation_date else "Unknown"
            subject = meta.subject if meta and meta.subject else "Unknown"
            
            # Add to lists
            filenames.append(file) 
            titles.append(title)
            authors.append(author)
            dates.append(str(creation_date))
            subjects.append(subject)
            
            print(f"Title: {title}")
            print(f"Author: {author}")
            print("---")
            
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
            # Add empty values for failed files if you want to track them
            filenames.append(file)
            titles.append("Error")
            authors.append("Error")
            dates.append("Error")
            subjects.append("Error")

# Create DataFrame from collected data
df = pd.DataFrame({
    "File Name": filenames,
    "Title": titles,
    "Authors": authors,
    "Date Published": dates,
    "Subject": subjects
})

# Save to CSV
output_file = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\metadata.csv"
df.to_csv(output_file, index=False)

print(f"Saved metadata for {len(df)} PDFs to {output_file}")
print(f"DataFrame shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())