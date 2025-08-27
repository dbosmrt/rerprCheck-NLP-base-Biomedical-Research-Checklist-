#First import all of the loaders 
import os
import pandas as pd
import re
from langchain_unstructured import UnstructuredLoader

#Define the folder path
folder_path = r"C:\Users\deepa\Downloads\Deepanshu Bhatt\rerprCheck-NLP-base-Biomedical-Research-Checklist-\Data\raw\pmc_pdfs"

#Create list to store all data
all_data = []

