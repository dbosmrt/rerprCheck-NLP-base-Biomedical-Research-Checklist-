import logging
import json
from langchain_community.llms import Ollama  
from langchain.prompts import PromptTemplate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  
)

logger = logging.getLogger(__name__)

class OllamaHandler:
    """
    Handles interaction with Ollama LLM
    """
    def __init__(self, model_name, temperature):  
        """
        Initialize ollama handler.
        It takes arugements:
            model_name: Ollama model name
            temperature: Generation temperature
        """
        try:
            self.llm = Ollama(model=model_name, temperature=temperature)  
            self.model_name = model_name
            logger.info(f"Initialized Ollama: {model_name}")
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
    


 
class TextPreprocessor:
    """
    Preprocess text before sending to LLM
    """
    @staticmethod
    def clean(text):
        lines = [line for line in text.split("\n") if line.strip()]
        return '\n'.join(lines)
    
    @staticmethod
    def estimate_tokens(text):
        return len(text) // 4
    

class JSONParser:
    """Parse and validate JSON from LLM responses."""
    @staticmethod
    def parse(response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return JSONParser._clean_and_parse(response)
        
    
    @classmethod  
    def _clean_and_parse(cls, response):  
        cleaned = response.strip()

        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        elif cleaned.startswith('```'):
            cleaned = cleaned[3:]

        
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.error("Could not parse JSON from LLM response")
            return None
        


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
            max_text_length: int = None,
            include_metadata: bool = False  
    ):
        self.llm_handler = llm_handler
        self.include_metadata = include_metadata  

        if max_text_length is None:  
            model_name = getattr(llm_handler, 'model_name', 'default')
            #extract base model name.
            base_model = model_name.split(':')[0]
            self.max_text_length = self.model_limits.get(base_model, self.model_limits['default'])
            logger.info(f"Auto-detected max_text_length: {self.max_text_length} characters for {model_name}")
        else:
            self.max_text_length = max_text_length
            logger.info(f"Using custom max_text_length: {max_text_length} characters.")

        
        self.preprocessor = TextPreprocessor()
        self.parse = JSONParser()
        self.prompt_template = PromptManager.get_section_prompt()

    
    def split(self, text):
        try:
            cleaned_text = self.preprocessor.clean(text)

            text_length = len(cleaned_text)
            estimated_tokens = self.preprocessor.estimate_tokens(cleaned_text)

            if text_length > self.max_text_length:
                logger.warning(
                    f"Text is {text_length:,} chars (~{estimated_tokens:,} tokens),"
                    f"Exceeds recommended {self.max_text_length:,} chars."
                    f"Processing full text anyway (may be slow or fail)."
                
                )

            else:
                logger.info(f"Text size: {text_length:,} chars (~{estimated_tokens:,} tokens.)")

            prompt = self.prompt_template.format(text = cleaned_text)

            logger.info("Calling LLM for section extraction...")
            response = self.llm_handler.generate(prompt)

            sections = self.parse.parse(response)  

            if sections:
                logger.info(f"Successfully extracted {len(sections)} sections")
                return sections
            else:
                logger.error("Failed to parse LLM response")
                return self.fallback_result(text)
            
        except Exception as e:
            logger.error(f"Error during splitting: {e}")
            return self.fallback_result(text)
        

    @staticmethod
    def fallback_result(text):
        # Returns fallback result when textraction fails.
        return {"Content": text}





