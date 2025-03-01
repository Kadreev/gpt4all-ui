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
from ctransformers import AutoModelForCausalLM

__author__ = "parisneo"
__github__ = "https://github.com/ParisNeo/gpt4all-ui"
__copyright__ = "Copyright 2023, "
__license__ = "Apache 2.0"

binding_name = "CTRansformers"

class CTRansformers(LLMBinding):
    file_extension='*.bin'
    def __init__(self, config:dict) -> None:
        """Builds a LLAMACPP binding

        Args:
            config (dict): The configuration file
        """
        super().__init__(config, False)
        if 'gpt2' in self.config['model']:
            model_type='gpt2'
        elif 'gptj' in self.config['model']:
            model_type='gptj'
        elif 'gpt_neox' in self.config['model']:
            model_type='gpt_neox'
        elif 'dolly-v2' in self.config['model']:
            model_type='dolly-v2'
        elif 'starcoder' in self.config['model']:
            model_type='starcoder'
        elif 'llama' in self.config['model'].lower() or 'wizardlm' in self.config['model'].lower() or 'vigogne' in self.config['model'].lower():
            model_type='llama'
        elif 'mpt' in self.config['model']:
            model_type='mpt'
        else:
            print("The model you are using is not supported by this binding")
            return
        
        
        if self.config["use_avx2"]:
            self.model = AutoModelForCausalLM.from_pretrained(
                    f"./models/c_transformers/{self.config['model']}", model_type=model_type
                    )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                    f"./models/c_transformers/{self.config['model']}", model_type=model_type, lib = "avx"
                    )
            
    def tokenize(self, prompt):
        """
        Tokenizes the given prompt using the model's tokenizer.

        Args:
            prompt (str): The input prompt to be tokenized.

        Returns:
            list: A list of tokens representing the tokenized prompt.
        """
        return self.model.tokenize(prompt.encode())

    def detokenize(self, tokens_list):
        """
        Detokenizes the given list of tokens using the model's tokenizer.

        Args:
            tokens_list (list): A list of tokens to be detokenized.

        Returns:
            str: The detokenized text as a string.
        """
        return self.model.detokenize(tokens_list)
    
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
            #self.model.reset()
            tokens = self.model.tokenize(prompt)
            count = 0
            for tok in self.model.generate(
                                            tokens,
                                            top_k=gpt_params['top_k'],
                                            top_p=gpt_params['top_p'],
                                            temperature=gpt_params['temperature'],
                                            repetition_penalty=gpt_params['repeat_penalty'],
                                            seed=self.config['seed'],
                                            batch_size=1,
                                            threads = self.config['n_threads'],
                                            reset=True,
                                           ):
                

                if count >= n_predict or self.model.is_eos_token(tok):
                    break
                word = self.model.detokenize(tok)
                if new_text_callback is not None:
                    if not new_text_callback(word):
                        break
                output += word
                count += 1
                
                
        except Exception as ex:
            print(ex)
        return output            
            
    @staticmethod
    def get_available_models():
        # Create the file path relative to the child class's directory
        binding_path = Path(__file__).parent
        file_path = binding_path/"models.yaml"

        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        return yaml_data