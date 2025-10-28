import logging
import skweak
import spacy
import scispacy

"""
This file will contain all the classes and methods for the weak supervision of the dataset using:
Skweak Library, using spacy's {"en_core_sci_scibert model"} for ner.
And storing of the labelled or Training dataset in the prescribed folder path.
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class WeakSupervision:
    """
    This class conatains methods for weak supervison of the text file.
    """
    def 