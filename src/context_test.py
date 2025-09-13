#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.expanduser('~/src/dazllm'))
from dazllm import Llm
from brain import Brain


class TestContext:
    """Shared test context with centralized brain configuration"""
    
    _instance = None
    _brain = None
    
    # Configure the model for all tests here
    MODEL_NAME = "ollama:gpt-oss:20b"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TestContext, cls).__new__(cls)
        return cls._instance
    
    def brain(self) -> Brain:
        """Get the shared brain instance for all tests"""
        if self._brain is None:
            print(f"🧠 Initializing test brain with model: {self.MODEL_NAME}")
            llm = Llm.model_named(self.MODEL_NAME)
            self._brain = Brain(llm)
        return self._brain
    
    def reset_brain(self):
        """Reset the brain (useful for tests that need a fresh state)"""
        self._brain = None


# Global test context instance
test_context = TestContext()


def get_test_brain() -> Brain:
    """Convenience function to get the test brain"""
    return test_context.brain()