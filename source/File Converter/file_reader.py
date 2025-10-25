import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Fixed spacing
)

logger = logging.getLogger(__name__)

class FileReader:
    """
    This class contains methods which reads different types of files
    """
    @staticmethod
    def text_reader(text_path: str) -> str | None:
        """
        This function takes the text file and check whether the text file has .txt extension or not.
        
        Args:
            text_path (str): Path where the text file is saved

        Returns:
            str | None: Returns filename if the file has extension .txt, None otherwise
        """
        try:
            if not os.path.exists(text_path):
                logger.error(f"File not found at path: {text_path}")
                return None
            
            text_file = os.path.split(text_path)
            if text_file[1].endswith('.txt'):
                text_file = text_file[1]
                return text_file
            else:
                logger.info(f"File {text_file[1]} is not a .txt file.")  # Fixed to show only filename
                return None
            
        except Exception as e:
            logger.error(f"Some unexpected error occurred {type(e).__name__} - {str(e)}", exc_info=True)
            return None