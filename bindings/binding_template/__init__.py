######
# Project       : GPT4ALL-UI
# File          : binding.py
# Author        : ParisNeo with the help of the community
# Underlying binding : Abdeladim's pygptj binding
# Supported by Nomic-AI
# license       : Apache 2.0
# Description   : 
# This is an interface class for GPT4All-ui bindings.

# This binding is a wrapper to marella's binding

######
from pathlib import Path
from typing import Callable
from api.binding import LLMBinding
import yaml
from api.config import load_config
import re

__author__ = "parisneo"
__github__ = "https://github.com/ParisNeo/gpt4all-ui"
__copyright__ = "Copyright 2023, "
__license__ = "Apache 2.0"

binding_name = "CustomBinding"

class CustomBinding(LLMBinding):
    # Define what is the extension of the model files supported by your binding
    # Only applicable for local models for remote models like gpt4 and others, you can keep it empty 
    # and reimplement your own list_models method
    file_extension='*.bin' 
    def __init__(self, config:dict) -> None:
        """Builds a LLAMACPP binding

        Args:
            config (dict): The configuration file
        """
        super().__init__(config, False)
        
        # The local config can be used to store personal information that shouldn't be shared like chatgpt Key 
        # or other personal information
        # This file is never commited to the repository as it is ignored by .gitignore
        # You can remove this if you don't need custom local configurations
        self._local_config_file_path = Path(__file__).parent/"config_local.yaml"
        self.config = load_config(self._local_config_file_path)

        # Do your initialization stuff
            
    def tokenize(self, prompt):
        """
        Tokenizes the given prompt using the model's tokenizer.

        Args:
            prompt (str): The input prompt to be tokenized.

        Returns:
            list: A list of tokens representing the tokenized prompt.
        """
        return None

    def detokenize(self, tokens_list):
        """
        Detokenizes the given list of tokens using the model's tokenizer.

        Args:
            tokens_list (list): A list of tokens to be detokenized.

        Returns:
            str: The detokenized text as a string.
        """
        return None
    
    def generate(self, 
                 prompt:str,                  
                 n_predict: int = 128,
                 new_text_callback: Callable[[str], None] = bool,
                 verbose: bool = False,
                 **gpt_params ):
        """Generates text out of a prompt

        Args:
            prompt (str): The prompt to use for generation
            n_predict (int, optional): Number of tokens to prodict. Defaults to 128.
            new_text_callback (Callable[[str], None], optional): A callback function that is called everytime a new text element is generated. Defaults to None.
            verbose (bool, optional): If true, the code will spit many informations about the generation process. Defaults to False.
        """
        try:
            output = ""
            count = 0
            generated_text = """
This is an empty binding that shows how you can build your own binding.
Find it in bindings.
```python
# This is a python snippet
print("Hello World")
```

This is a photo
![](/images/icon.png)
"""
            for tok in re.split(r'(\s+)', generated_text):               
                if count >= n_predict:
                    break
                word = tok
                if new_text_callback is not None:
                    if not new_text_callback(word):
                        break
                output += word
                count += 1
        except Exception as ex:
            print(ex)
        return output            
         
    
    # Decomment if you want to build a custom model listing
    #@staticmethod
    #def list_models(config:dict):
    #    """Lists the models for this binding
    #    """
    #    models_dir = Path('./models')/config["binding"]  # replace with the actual path to the models folder
    #    return [f.name for f in models_dir.glob(LLMBinding.file_extension)]
    #
        
    @staticmethod
    def get_available_models():
        # Create the file path relative to the child class's directory
        binding_path = Path(__file__).parent
        file_path = binding_path/"models.yaml"

        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        return yaml_data