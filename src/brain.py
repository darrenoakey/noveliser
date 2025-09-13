import json
import hashlib
import os
from pathlib import Path
from typing import Any, Optional, Type
import sys
sys.path.append(os.path.expanduser('~/src/dazllm'))
from dazllm import Llm
from pydantic import BaseModel

class Brain:
    """
    Caching wrapper for dazllm that stores LLM responses to avoid redundant API calls.
    """
    
    def __init__(self, llm: Llm):
        self.llm = llm
        self.cache_dir = Path("output/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _hash_input(self, *args, **kwargs) -> str:
        """Create a hash from the input arguments."""
        input_str = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
        return hashlib.sha256(input_str.encode()).hexdigest()
    
    def _get_cache_path(self, hash_key: str) -> Path:
        """Get the cache file path for a given hash."""
        return self.cache_dir / f"{hash_key}.json"
    
    def _load_from_cache(self, hash_key: str) -> Optional[dict[str, Any]]:
        """Load cached response if it exists."""
        cache_path = self._get_cache_path(hash_key)
        if cache_path.exists():
            with open(cache_path, 'r') as f:
                return json.load(f)
        return None
    
    def _save_to_cache(self, hash_key: str, inputs: dict, output: Any):
        """Save response to cache."""
        cache_path = self._get_cache_path(hash_key)
        cache_data = {
            "inputs": inputs,
            "output": output
        }
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=2, default=str)
    
    def chat(self, messages: list[dict[str, str]], **kwargs) -> str:
        """Cached wrapper for llm.chat()"""
        hash_key = self._hash_input(messages, **kwargs)
        
        cached = self._load_from_cache(hash_key)
        if cached:
            return cached["output"]
        
        result = self.llm.chat(messages, **kwargs)
        self._save_to_cache(hash_key, {"messages": messages, "kwargs": kwargs}, result)
        return result
    
    def chat_structured(self, messages: list[dict[str, str]], model_class: Type[BaseModel], **kwargs) -> BaseModel:
        """Cached wrapper for llm.chat_structured() - only accepts Pydantic BaseModel types"""
        hash_key = self._hash_input(messages, model_class.__name__, **kwargs)
        
        cached = self._load_from_cache(hash_key)
        if cached:
            # Reconstruct the model from cached dict data
            return model_class(**cached["output"])
        
        result = self.llm.chat_structured(messages, model_class, **kwargs)
        
        # Cache the dict representation
        self._save_to_cache(
            hash_key, 
            {"messages": messages, "model_class": model_class.__name__, "kwargs": kwargs}, 
            result.model_dump()
        )
        return result
    
    def clear_cache(self):
        """Clear all cached responses."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()