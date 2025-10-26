import logging
from llm_handler import OllamaHandler
from processor import BatchProcessor

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processing.log'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    """
    You are required to install Ollama from : https://ollama.ai
    After that just pull the model llama3.2
    """

    #Initialize LLm
    llm = OllamaHandler(model_name = "llama3.2", temperature = 0.1)

    #initialize batch processor
    processor = BatchProcessor(
        input_folder= " ",
        output_folder = ".",
        llm_handler = llm
    )

    print("Testing on 3 files...")
    processor.process_all(max_files=3)