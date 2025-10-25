import os
import logging
import json
from pathlib import Path
from langchain_community.llms import ollama
from langchain.prompts import prompt
from langchain.chains.llm import LLMChain

logging.basicConfig(
    level= logging.INFO,
    format= "%(asctime)s - %(names)s -%(levlename)s - %(message)s"
)

logger = logging.getLogger(__name__)

class FileReader:
    """
    This class contains methods which reads different types of files
    """
    @staticmethod
    def text_reader(text_path: str) -> bool:
        """
        This function takes the text file and check whether the text file has .txt extension or not.
        It takes arguement:
        text_path : takes the path where the text file is saved

        and returns:
        True if the file has extension .txt otherwise False.
        """
        try:
            text_file = os.path.split(text_path)
            if text_file[1].endswith('.txt'):
                return text_file[1]
            else:
                return None
        
        except FileNotFoundError as e:
            logger.error(f"The text file was not found in path :{text_path} - {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Some unexpected error occured {type(e).__name__} - {str(e)}", exc_info=True)
            return None
        
