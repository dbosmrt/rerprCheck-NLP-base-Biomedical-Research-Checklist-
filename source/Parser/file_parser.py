import os
import logging
import tempfile
from typing import Optional
from pathlib import Path
from langchain_unstructured import UnstructuredLoader

logging.basicConfig(
    level= logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

class PDFParser:
    """
    This class contians Parser for converting PDF files to text.
    It used LangChain UnstructuredLoader.
    """
    supported_extensions = ('.pdf',)
    mode = 'elements'
    strategy = 'fast'

    @staticmethod
    def validate_file(file_path: str) -> bool:
        """
        This function validates if the file is having .pdf extension or if it exists.
        It takes argurements (file_path) and returns:
        True if valid, Otherwise False
        """
        try:
            if not isinstance(file_path, str):
                logger.error(f"Invalid file path type: {type(file_path)}. Expected string")
                return False
            
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False
            
            file_extension = Path(file_path).suffix.lower()
            if file_extension not in PDFParser.supported_extensions:
                logger.error(f"Unsupported file type: {file_extension}. Expected PDF file.")
                return False
            
            logger.info(f"File is valid: {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error during file validation: {type(e).__name__} - {str(e)}")
            return False
        
    @staticmethod
    def parse(pdf_file_path: str, mode: str = "elements", strategy: str = "fast") -> Optional[str]:
        """
        Parse a PDF file and returns a extrated text content.
        It takes arguements:
        pdf_file_path: Path to the PDF file (can be uploaded file path)
        mode: UnstructuredLoader mode ('single', 'elements', or 'paged')
        strategy: Parsing strategy ('fast', 'hi_res', or 'ocr_only')

        Then it returns:
        Extracted text as string, or None if parsing failed
        """
        logger.info(f"Starting PDF parsing: {pdf_file_path}")
        
        if not PDFParser.validate_file(pdf_file_path):
            return None
        
        try:
            logger.debug(f"Loading PDF with mode = {mode}, strategy = {strategy}")
            loader = UnstructuredLoader(
                pdf_file_path,
                mode= mode,
                strategy = strategy
            )

            documents = loader.load()
            logger.info(f"Successfully loaded {len(documents)} document elements")

            text_content = "\n\n".join([
                doc.page_content
                for doc in documents
                if doc.page_content and doc.page_content.strip()
            ])

            if not text_content.strip():
                logger.warning(f"No text content extracted from: {pdf_file_path}")
                return None
            logger.info(f"Successfully parsed PDF. Extracted {len(text_content)} Characters")
            return text_content
        
        except FileNotFoundError as e:
            logger.error(f"File not found during parsing: {str(e)}")
            return None
        
        except PermissionError as e:
            logger.error(f"Permission denied while reading file: {str(e)}")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected error during PDF parsing: {type(e).__name__} - {str(e)}", exc_info= True)
            return None
    
    @staticmethod
    def parse_from_bytes(pdf_bytes: bytes, filename: str = "uploaded.pdf", mode: str = 'elements', strategy: str = 'fast') -> Optional[str]:
        """This function is optional won't be used much
        It parses PDF from bytes (useful for direct file uploads).
        
        It takes Arguements:
        pdf_bytes: PDF file content as bytes
        filename: Original filename(for logging purposes)
        mode: UnstructuredLoader mode ('single', 'elements', or 'paged')
        strategy: Parsing strategy ('fast', 'hi_res', or 'ocr_only')
        
        And it returns:
        Extracted text as string, or Noe if parsing failed
        """
        logger.info(f"Parsing PDF form bytes: {filename}")

        temp_path = None
        try:
            # Create temporary file to pass to Unstructured Loader
            with tempfile.NamedTemporaryFile(suffix= '.pdf', delete=False) as temp_file:
                temp_file.write(pdf_bytes)
                temp_path = temp_file.name

            result = PDFParser.parse(temp_path, mode = mode, strategy= strategy)

            return result
        
        except Exception as e:
            logger.error(f"Error parsing PDF from bytes: {type(e).__name__} - {str(e)}", exc_info = True)
            return None
        
        finally: 
            # Clean up temproary file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                    logger.debug(f"Temproary file cleaned up: {temp_path}")
                except Exception as e:
                    logger.warning(f"Could not delete temp file {temp_path}: {e}")
