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