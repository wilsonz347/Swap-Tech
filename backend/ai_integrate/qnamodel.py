from transformers import pipeline
from flask import Flask, jsonify, request
from flask_cors import CORS
import torch

class QAConfig:
    MODEL_NAME = "deepset/roberta-base-squad2"  
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class ChatBotSystem:
    def __init__(self):
        # Initialize the QA pipeline
        self.qa_pipeline = pipeline(
            "question-answering",
            model=QAConfig.MODEL_NAME,
            device=QAConfig.DEVICE
        )

    def get_response(self, context, question):
        """
        Get an answer to the question based on the provided context.
        """
        try:
            # Use the QA pipeline to get the answer
            result = self.qa_pipeline(question=question, context=context)

            return {
                "success": True,
                "response": result["answer"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate response: {str(e)}"
            }
