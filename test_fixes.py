import os
import sys
import logging

# Add source directory to path
sys.path.append(os.path.join(os.getcwd(), 'source', 'NLP'))

from preprocessing_ner import Preprocessor
from file_loader import LoadText

# Setup dummy file
test_file = "test_doc.txt"
with open(test_file, "w", encoding="utf-8") as f:
    f.write("This is a   test file.\nIt has multiple lines.\nAnd some hyphen-\nated words.")

try:
    print("Testing remove_whitespaces...")
    res = Preprocessor.remove_whitespaces(test_file)
    print(f"Result: {res}")
    
    print("\nTesting remove_linebreaks...")
    res = Preprocessor.remove_linebreaks(test_file)
    print(f"Result: {res}")

    print("\nTesting fix_hyphenated_line_breaks...")
    res = Preprocessor.fix_hyphenated_line_breaks(test_file)
    print(f"Result: {res}")

    print("\nTesting boiler_plate_remover...")
    # Note: boiler_plate_remover is an instance method in the original code but defined without self if used as static, 
    # checking usage. It was defined as `def boiler_plate_remover(text_file):` inside class but not static.
    # Assuming it's meant to be static or instance. Let's try calling it on instance.
    p = Preprocessor()
    res = p.boiler_plate_remover(test_file)
    print(f"Result: {res}")

except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
finally:
    if os.path.exists(test_file):
        os.remove(test_file)
