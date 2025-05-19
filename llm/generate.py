import os
from datetime import datetime
from typing import Optional
from pathlib import Path
import requests
from dotenv import load_dotenv
from engine.prompt_builder import PromptBuilder
from engine.kg_parser import KnowledgeGraphParser

# Load environment variables from .env file
load_dotenv()

class LLMGenerator:
    def __init__(self, model_name: str = "meta-llama/Llama-3.1-8B-Instruct", temperature: float = 0.7):
        """Initialize the LLM generator with a specific model and temperature."""
        self.model_name = model_name
        self.temperature = temperature
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Get Hugging Face token
        self.token = os.getenv("HUGGINGFACE_TOKEN")
        if not self.token:
            raise ValueError("HUGGINGFACE_TOKEN environment variable not set. Please set it in your .env file.")
        
        # Initialize knowledge graph parser
        self.kg_parser = KnowledgeGraphParser("data/philosophers.ttl")

    def generate_response(self, prompt: str, philosopher: str) -> str:
        """Generate a response using the Hugging Face Inference API."""
        # Get philosopher data from knowledge graph
        philosopher_data = self.kg_parser.get_philosopher(philosopher)
        if not philosopher_data:
            raise ValueError(f"Philosopher {philosopher} not found in knowledge graph")
            
        # Use PromptBuilder to format the prompt
        prompt_builder = PromptBuilder(philosopher_data)
        formatted_prompt = prompt_builder.build_prompt(prompt)
        
        # Format the prompt for Llama
        llama_prompt = f"""<s>[INST] {formatted_prompt} [/INST]"""
        
        # Call the Hugging Face Inference API
        API_URL = f"https://api-inference.huggingface.co/models/{self.model_name}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        payload = {
            "inputs": llama_prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": self.temperature,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
                "do_sample": True
            }
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Extract the generated text from the response
            generated_text = response.json()[0]["generated_text"]
            
            # Clean up the response text
            # First remove the prompt
            generated_text = generated_text[len(llama_prompt):].strip()
            
            # Remove any special tokens and URLs
            generated_text = generated_text.replace("<s>", "").replace("</s>", "")
            generated_text = generated_text.replace("[INST]", "").replace("[/INST]", "")
        
            
            if not generated_text:
                generated_text = "I apologize, but I am unable to generate a response at this time. This may be due to the complexity of the question or limitations in my current state."
            

            self._save_response(generated_text, philosopher)
            
            return generated_text
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error calling Hugging Face API: {str(e)}"
            print(error_msg)
            return error_msg

    def _save_response(self, response: str, philosopher: str) -> None:
        """Save the generated response to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{philosopher.lower()}_{timestamp}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, "w") as f:
            f.write(response)

    @classmethod
    def from_env(cls) -> 'LLMGenerator':
        """Create an LLMGenerator instance using environment variables."""
        token = os.getenv("HUGGINGFACE_TOKEN")
        if not token:
            raise ValueError("HUGGINGFACE_TOKEN environment variable not set. Please set it in your .env file.")
        
        model_name = os.getenv("LLM_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        
        return cls(model_name=model_name, temperature=temperature)  