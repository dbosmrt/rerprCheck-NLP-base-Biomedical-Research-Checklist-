from PyPDF2 import PdfReader
import os
import pandas as pd

# Create empty DataFrame
df = pd.DataFrame({"Title": [], "Authors": [], "Date Published": [], "Subject": []})

folder_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_pdfs"

# Lists to store metadata for all PDFs
titles = []
authors = []
dates = []
subjects = []

# Loop through all PDFs
for file in os.listdir(folder_path):
    if file.endswith(".pdf"):
        file_path = os.path.join(folder_path, file)  # Fixed: correct order of arguments
        
        # Process each file and collect metadata
        try:
            reader = PdfReader(file_path)
            num_pages = len(reader.pages)
            meta = reader.metadata  # Fixed: metadata is not a length, it's the actual metadata object
            
            print(f"Processing: {file}")
            print(f"Pages: {num_pages}")
            
            # Extract metadata safely (handle None values)
            title = meta.title if meta and meta.title else "Unknown"
            author = meta.author if meta and meta.author else "Unknown"  # Note: it's 'author', not 'authors'
            creation_date = meta.creation_date if meta and meta.creation_date else "Unknown"
            subject = meta.subject if meta and meta.subject else "Unknown"
            
            # Add to lists
            titles.append(title)
            authors.append(author)
            dates.append(str(creation_date))  # Convert to string for CSV compatibility
            subjects.append(subject)
            
            print(f"Title: {title}")
            print(f"Author: {author}")
            print("---")
            
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
            # Add empty values for failed files if you want to track them
            titles.append("Error")
            authors.append("Error")
            dates.append("Error")
            subjects.append("Error")

# Create DataFrame from collected data
df = pd.DataFrame({
    "Title": titles,
    "Authors": authors,
    "Date Published": dates,
    "Subject": subjects
})

# Save to CSV
output_file = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\metadata.csv"
df.to_csv(output_file, index=False)  # Fixed: use df.to_csv(), not pd.to_csv()

print(f"Saved metadata for {len(df)} PDFs to {output_file}")
print(f"DataFrame shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())