import os
import logging
import json
from pathlib import Path
from typing import Optional, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  
)

logger = logging.getLogger(__name__)

class FileReader:
    """Handles reading files with encoding fallbacks."""
    
    @staticmethod
    def read_text_file(file_path: Path) -> Optional[str]:
        """
        Read text file with multiple encoding attempts.
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content or None
        """
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                logger.debug(f"Read {file_path.name} with {encoding}")
                return content
            except (UnicodeDecodeError, LookupError):
                continue
            except Exception as e:
                logger.error(f"Error reading {file_path.name}: {e}")
                return None
        
        logger.error(f"Could not read {file_path.name} with any encoding")
        return None
    
    @staticmethod
    def read_json_file(file_path: Path) -> Optional[Dict]:
        """Read JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON {file_path.name}: {e}")
            return None
        

class FileWriter:
    """Handles writing files in different formats."""
    
    @staticmethod
    def write_json(data: Dict, output_path: Path) -> bool:
        """
        Write data to JSON file.
        
        Args:
            data: Dictionary to save
            output_path: Output file path
            
        Returns:
            True if successful
        """
        try:
            os.makedirs(output_path.parent, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved JSON: {output_path.name}")
            return True
        except Exception as e:
            logger.error(f"Error writing JSON: {e}")
            return False
    
    @staticmethod
    def write_text(text: str, output_path: Path) -> bool:
        """Write text to file."""
        try:
            os.makedirs(output_path.parent, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            logger.debug(f"Saved text: {output_path.name}")
            return True
        except Exception as e:
            logger.error(f"Error writing text: {e}")
            return False
