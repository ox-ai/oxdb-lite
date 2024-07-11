from typing import List, Dict, Union

from transformers import AutoTokenizer


class Model:

    def __init__(self, model_src:str=None, max_tokens: int = 256):
        self.md_name = model_src or "sentence-transformers/all-MiniLM-L6-v2"
        self.max_tokens = max_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(self.md_name)
    

        self.tokenizer = AutoTokenizer.from_pretrained(self.md_name)

    def count_token(self, data: str):
        return len(self.tokenizer.tokenize(data)) + 2
    
    def is_full(self,data_len,avilable_token):
        if data_len+avilable_token > 256 :
            return True
        else:
            return False
        




