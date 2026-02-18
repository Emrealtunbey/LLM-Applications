import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification



def pipeline_trial():
    checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)  # TOKENIZATION

    raw_input = ["I've been waiting for a HuggingFace course my whole life.",
                 "I hate this so much!"]
    tokenized_input = tokenizer(raw_input,padding=True,truncation=True,return_tensors="pt")

    model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
    pre_postprocessed = model(**tokenized_input)                # MODEL heads

    predictions = torch.nn.functional.softmax(pre_postprocessed.logits,dim=-1)           #Post-Processing
    print(predictions)

pipeline_trial()