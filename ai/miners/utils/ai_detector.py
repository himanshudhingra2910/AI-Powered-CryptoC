from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

class AIGeneratedTextDetector:
    def __init__(self):
        model_name = "roberta-base-openai-detector"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)

    def is_ai_generated(self, text):
        result = self.classifier(text)[0]
        label = result["label"]
        score = result["score"]
        return label == "LABEL_1", score  # LABEL_1 = AI-Generated
