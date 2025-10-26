import logging
from langchain_community.llms import ollama
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Fixed spacing
)

logger = logging.getLogger(__name__)

class OllamaHandler:
    """
    Handles interaction with Ollama LLM
    """
    def __init__(self, mode_name, temperature):
        """
        Initialize ollama handler.
        It takes arugements:
            model_name: Ollama model name
            temperature: Generation temperature
        """
        try:
            self.llm = ollama(mode = mode_name, temperature= temperature)
            self.model_name = mode_name
            logger.info(f"Initialized Ollama: {mode_name}")
        except Exception as e:
            logger.error(f"Failed to Initialize Ollama: {e}")
            raise
    
    def generate(self, prompt):
        # Generate response from Ollama.
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            logger.error(f"Error genrating response: {e}")
            raise


class PromptManager:
    """Mangages prompts for different extraction tasks."""

    section_extraction_prompt = """ You are an expert at Analyzing academic papers.

    Important: Extraxt the EXACT orginial text from each section. DO NOT summarize, paraphrase, or modify the content in any way. Copy the text exactly as it appears.
    
    Given the following academic paper text, identify and extract these sections with their EXACT ORIGINAL TEXT:
    - Abstract
    - Keywords
    - Introduction
    - Literature Review (or Related Work, Background)
    - Methodology (or Methods, Materials and Methods)
    - Results
    - Discussion
    - Conclusion 
    - References

    Some Sections may not exist - that's okay. Include subsections if they exist.

    Return ONLY a valid JSON object with this structure:
    {{
    "Abstract": "EXACT text from abstract section",
    "Keywords": "EXACT keywords as written",
    "Introduction": {{
        "main_text": "EXACT introduction text",
        "subsections": {{
        "Background": "EXACT background text"
        }}
    }},
    "Methodology": "EXACT methodology text",
    "Results": "EXACT results text",
    "Discussion": "EXACT discussion text",
    "Conclusion": "EXACT conclusion text",
    "References": "EXACT references text"
    }}

    Paper Text:
    {text}

    JSON Output:"""

    @staticmethod
    def get_section_prompt() -> PromptTemplate:
        return PromptTemplate(
            input_variables=["text"],
            template = PromptManager.section_extraction_prompt
        )
    


class LLMSectionSplitter:
    """
    It uses LLM to split academic papers into structured sections
    It is reusable component for section extraction.
    """

    model_limits = {
        'llama3.2': 100000,
        'llama3.1': 100000,
        'llama2': 8000,
        'default': 8000
    }

    def __init__(
            self,
            llm_handler: OllamaHandler,
            max_text_lenght: int= None
    ):
        sefl.llm_handler = llm_handler

        if max_text_lenght is None:
            model_name = getattr(llm_handler, 'model_name', 'default')
            #extract base model name.
            base_model = model_name.split(':')[0]
            self.max_text_length = self.model_limits.get(base_model, self.model_limits['default'])
            logger.info(f"Auto-detected max_text_length: {self.max_text_length} characters for {model_name}")
        else:
            self.max_text_length = max_text_lenght
            logger.info(f"Using custom max_text_length: {max_text_length} characters.")

        
        self.prompt_template = PromptManager.get_section_prompt()

