"""
Detravious Jamari Brinkley, Kingdom Man (https://brinkley97.github.io/expertise_and_portfolio/research/researchIndex.html)
UF Data Studio (https://ufdatastudio.com/) with advisor Christan E. Grant, Ph.D. (https://ceg.me/)

Factory Method Design Pattern (https://refactoring.guru/design-patterns/factory-method/python/example#lang-features)
"""

import os

import pandas as pd

from groq import Groq
from typing import Dict, List
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()  # Load environment variables from .env file

class TextGenerationModelFactory(ABC):
    """An abstract base class to load any pre-trained generation model"""
    
    @abstractmethod
    def __init__(self):
        """Initialize the model with necessary parameters"""
        # models: https://console.groq.com/docs/models
        # Groq client
        self.api_key = os.getenv('API_KEY')
        if self.api_key is None:
            raise ValueError("API_KEY environment variable not set")
        # self.client = Groq(api_key=self.api_key)
        self.temperature = 0.3
        self.top_p = 0.9

    def assistant(self, content: str) -> Dict:
        """Create an assistant message.
        
        Parameters:
        -----------
        content: `str`
            The content of the assistant message.
        
        Returns:
        --------
        Dict
            A dictionary representing the assistant message.
        """

        return {"role": "assistant", "content": content}
    
    def user(self, content: str) -> Dict:
        """Create a user message.
        
        Parameters:
        -----------
        content : `str`
            The content of the user message.
        
        Returns:
        --------
        Dict
            A dictionary representing the user message.
        """

        return {"role": "user", "content": content}
    
    def chat_completion(self, messages: List[Dict]) -> str:
        """Generate a chat completion response.
        
        Parameters:
        -----------
        messages: `List[Dict]`
            A list of dictionaries representing the chat history.
        
        model: `str`
            The name of the model to use.
        
        temperature: `float`
            Sampling temperature.
        
        top_p: `float`
            Nucleus sampling parameter.
        
        Returns:
        --------
        `str`
            The generated chat completion response.
        """

        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        return response.choices[0].message.content
    
    def generate_predictions(self, prompt_template: str, label: str, domain: str) -> pd.DataFrame:
        """Generate a completion response and return as a DataFrame.

        Parameters:
        -----------
        prompt_template: `str`
            The prompt template to generate a prediction prompt or a non-prediction prompt.
        
        label: `str`
            The prediction label for the prediction. Either 0 (non-prediction) or 1 (prediction).
        
        domain: `str`
            The domain of the prediction. As of now, the domains are finance, weather, health, and policy.

        template_number: `int`
            The template number to use for the prediction. For non-prediction prompts, the template number is 0 and for prediction prompts, the template number is 1 to 5.
        
        Returns:
        --------
        `pd.DataFrame`
            The generated completion response formatted as a DataFrame.
        """

        # Generate the raw prediction text
        raw_text = self.chat_completion([self.user(prompt_template)])
        
        # Parse the raw text into structured data (assuming a consistent format)
        predictions = []
        for line in raw_text.split("\n"):
            if line.strip():  # Skip empty lines
                predictions.append(line.strip())
        
        # Convert to DataFrame
        df = pd.DataFrame(predictions, columns=['Base Sentence'])
        df['Sentence Label'] = label
        df['Model Name'] = self.model_name
        df['Domain'] = domain
        return df

class LlamaVersatileTextGenerationModel(TextGenerationModelFactory):    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('API_KEY')
        if self.api_key is None:
            raise ValueError("API_KEY environment variable not set")
        self.client = Groq(api_key=self.api_key)
        self.model_name = "llama-3.3-70b-versatile"

class LlamaInstantTextGenerationModel(TextGenerationModelFactory):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('API_KEY')
        if self.api_key is None:
            raise ValueError("API_KEY environment variable not set")
        self.client = Groq(api_key=self.api_key)
        self.model_name = "llama-3.1-8b-instant"

class Llama70B8192TextGenerationModel(TextGenerationModelFactory):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('API_KEY')
        if self.api_key is None:
            raise ValueError("API_KEY environment variable not set")
        self.client = Groq(api_key=self.api_key) 
        self.model_name = "llama3-70b-8192"

class Llama8B8192TextGenerationModel(TextGenerationModelFactory):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('API_KEY')
        if self.api_key is None:
            raise ValueError("API_KEY environment variable not set")
        self.client = Groq(api_key=self.api_key)
        self.model_name = "llama3-8b-8192"

class MixtralTextGenerationModel(TextGenerationModelFactory):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('API_KEY')
        if self.api_key is None:
            raise ValueError("API_KEY environment variable not set")
        self.client = Groq(api_key=self.api_key)  
        self.model_name = "mixtral-8x7b-32768"

# class DeepScaleRTextGenerationModel(TextGenerationModelFactory):
#     """
#     A class to interact with the DeepScaleR model.
    
#     Attributes:
#     -----------

#     """
    
#     def __init__(self):
#         self.model_name = "agentica-org/DeepScaleR-1.5B-Preview"
#         self.pipe = pipeline("text-generation", model=self.model_name)

    

#     def generate_predictions(self, prompt_template: str, label: str, domain: str) -> pd.DataFrame:
#         """
#         Generate a completion response and return as a DataFrame.

#         Parameters:
#         -----------
#         prompt_template: `str`
#             The prompt template to generate a prediction prompt or a non-prediction prompt.
        
#         label: `str`
#             The prediction label for the prediction. Either 0 (non-prediction) or 1 (prediction).
        
#         domain: `str`
#             The domain of the prediction. As of now, the domains are finance, weather, health, and policy.

#         Returns:
#         --------
#         `pd.DataFrame`
#             The generated completion response formatted as a DataFrame.
#         """
#         # Generate the raw prediction text
#         raw_text = self.pipe(prompt_template)[0]["generated_text"]
        
#         # Parse the raw text into structured data (assuming a consistent format)
#         predictions = [line.strip() for line in raw_text.split("\n") if line.strip()]
        
#         # Convert to DataFrame
#         df = pd.DataFrame(predictions, columns=['Base Sentence'])
#         df['Sentence Label'] = label
#         df['Model Name'] = self.model_name
#         df['Domain'] = domain
#         return df





