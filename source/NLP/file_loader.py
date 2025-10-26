import spacy 
import scispacy
import logging
import os
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

class NLP:
    """
    This class contains the method to load spaCy models.
    Models supported: "en_core_sci_scibert", "en_core_sci_sm", etc.
    """
    @staticmethod
    def model(model: str) -> Optional[spacy.language.Language]:
        """
        Load a spaCy model.

        Args:
            model (str): Name of the spaCy model to load

        Returns:
            Optional[spacy.language.Language]: Loaded spaCy model or None if loading fails
        """ 
        try:
            nlp = spacy.load(model)
            logger.info(f"Model '{model}' successfully loaded")
            return nlp
        except OSError as e:
            logger.error(f"Model '{model}' not found: {str(e)}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Unexpected error loading model: {type(e).__name__} - {str(e)}", exc_info=True)
            return None
        

class LoadText:
    """
    This class contains methods by which we can load the file.
    """
    @staticmethod
    def text_loader(text_file, model):
        """
        This function check for the text file and if exist the it loads it in the nlp model"""
        try:
            if not os.path.exists(text_file):
                logger.error(f"No such file exists here.")
                return None
            
            else:
                with open(text_file, 'r', encoding = 'utf-8') as f:
                    text_file = f.read()
                    doc = model(text_file)
                    logger.info(f"Successfully processed file: {text_file}")
                    return doc 
                
        except Exception as e:
            logger.error(f"There was some unexpected error: {type(e).__name__} - {str(e)}", exc_info=True)
            return None
        

    
