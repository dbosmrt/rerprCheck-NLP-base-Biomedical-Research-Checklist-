import logging
from os import mkdir
from pathlib import Path
from tqdm import tqdm
from typing import Optional

#import other modules
from file_handler import FileReader, FileWriter
from llm_handler import LLMSectionSplitter, OllamaHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  
)

logger = logging.getLogger(__name__)

class FileProcessor:

    def __init__(
        self,
        splitter: LLMSectionSplitter,
        reader: FileReader,
        writer: FileWriter
    ):
        self.splitter = splitter
        self.reader = reader
        self.writer = writer

    def process(self, input_path, output_path):
        try:
            text = self.reader.read_text_file(input_path)
            if not text or not text.strip():
                logger.error(f"Empty file: {input_path.name}")
                return False
            
            sections = self.splitter.split(text)

            success = self.writer.write_json(sections, output_path)

            if success:
                logger.info(f"Processed: {input_path.name}")

            return success
        except Exception as e:
            logger.error(f"Error Processing {input_path.name}: {e}")
            return False
        


class BatchProcessor:

    def __init__(
        self,
        input_folder: str,
        output_folder: str,
        llm_handler: OllamaHandler,
        file_extension: str = '.txt',
        max_text_length: Optional[int] = None,
        include_metadata: bool = False,
        include_file_metadata: bool = False
    ):
        
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.file_extension = file_extension
        self.include_file_metadata = include_file_metadata


        self.splitter = LLMSectionSplitter(
            llm_handler,
            max_text_length = max_text_length,
            include_metadata = include_metadata
        )

        self.reader = FileReader()
        self.writer = FileWriter()
        self.processor = FileProcessor(self.splitter, self.reader, self.writer)

        #create an output folder
        self.output_folder.mkdir(parents=True, exist_ok = True)


        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
        }

    def get_files(self):
        pattern = f"*{self.file_extension}"
        files = list(self.input_folder.glob(pattern))
        logger.info(f"Found {len(files)} {self.file_extension} files")
        return files
        
    def process_all(self, max_files: Optional[int] = None, skip_existing: bool = True):
        files = self.get_files()
        self.stats['total'] = len(files)

        if max_files:
            files = files[:max_files]
            logger.info(f"Limiting to {max_files} files")

        if not files:
            logger.warning("No files found")
            return
            

        #process each file
        for file_path in tqdm(files, desc="Processing", unit='file'):
            output_path = self.output_folder / f"{file_path.stem}.json"

            if skip_existing and output_path.exists():
                logger.info(f"Skipping {file_path.name} (exists)")
                self.stats['skipped'] +=1
                continue

            success = self.processor.process(
                file_path, 
                output_path  
            )

            if success:
                self.stats['success'] += 1
            else:
                self.stats['failed'] += 1 
            
        self.print_summary()
    
    def print_summary(self):
        logger.info("=" * 60)
        logger.info("Summary")
        logger.info(f"Toatal: {self.stats['total']}")
        logger.info(f"Success: {self.stats['success']}")
        logger.info(f"Failed: {self.stats['failed']}")
        logger.info(f"Skipped : {self.stats['skipped']}")


        if self.stats['total'] > 0:
            rate = (self.stats['success'] / self.stats['total']) *100
            logger.info(f"Success rate: {rate:.2f}%")
        
        logger.info("="* 60)


