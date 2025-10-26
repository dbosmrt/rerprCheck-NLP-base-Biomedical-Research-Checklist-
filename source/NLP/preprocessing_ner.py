import re
import logging
from file_loader import LoadText

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

class Preprocessor:
    """
    This class contains all the essential methods used for Preprocessing of the given text.
    """
    @staticmethod
    def remove_whitespaces(text_file):
            text_file = LoadText.text_loader()
            cleaned_file = text_file.replace(" ", "")
            LoadText.save_text(text_file, cleaned_file)
            logging.info(f"Whitespaces removed from {text_file}")
            return cleaned_file
        
    

    @staticmethod
    def remove_linebreaks(text_file):
        text_file = LoadText.text_loader()
        cleaned_file = re.sub(r'(\n\s*)+\n', '\n\n', text_file)
        LoadText.save_text(text_file, cleaned_file)
        return cleaned_file
    


    @staticmethod
    def fix_hyphenated_line_breaks(text_file):
        text_file = LoadText.text_loader()
        LoadText.save_text(text_file, cleaned_file)
        cleaned_file = re.sub(r'-\s*\n', '', text_file)
        return cleaned_file
    

