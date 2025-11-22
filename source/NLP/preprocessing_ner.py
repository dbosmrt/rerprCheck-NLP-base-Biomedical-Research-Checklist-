import os
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
        content = LoadText.text_loader(text_file)
        if content:
            # Replace multiple spaces with single space and strip leading/trailing
            cleaned_file = re.sub(r'\s+', ' ', content).strip()
            LoadText.save_text(text_file, cleaned_file)
            logging.info(f"Whitespaces removed from {text_file}")
            return cleaned_file
        return None

    @staticmethod
    def remove_linebreaks(text_file):
        content = LoadText.text_loader(text_file)
        if content:
            cleaned_file = re.sub(r'(\n\s*)+\n', '\n\n', content)
            LoadText.save_text(text_file, cleaned_file)
            return cleaned_file
        return None

    @staticmethod
    def fix_hyphenated_line_breaks(text_file):
        content = LoadText.text_loader(text_file)
        if content:
            cleaned_file = re.sub(r'-\s*\n', '', content)
            LoadText.save_text(text_file, cleaned_file)
            return cleaned_file
        return None

    def boiler_plate_remover(text_file):
        """This function remove all the bioler plate template from the text file
        It takes arugement:
                text_file : text file with .txt fromat
                
        and Returns: 
                cleaned_text: returns file with boiler plate removed containing only important data."""
        
        try:
            content = LoadText.text_loader(text_file)
            # Placeholder for boilerplate removal logic
            # For now just return content as is or implement specific logic
            return content
        except Exception as e:
            logger.error(f"Error removing boilerplate: {e}")
            return None
    

