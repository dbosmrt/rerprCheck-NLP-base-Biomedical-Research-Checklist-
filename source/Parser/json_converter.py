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
        This function takes the text file and check whether the text file is 
        """