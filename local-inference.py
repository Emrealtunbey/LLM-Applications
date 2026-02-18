import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

checkpoint = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

raw_text = "I don't hate this"
tokenized_text = tokenizer(raw_text,return_tensors="pt",padding=True,truncation=True)

model_output = model(**tokenized_text)
predictions = torch.nn.functional.softmax(model_output.logits, dim=-1)
print(predictions)
predicted_class_id = torch.argmax(predictions,dim=-1).item()
label = model.config.id2label[predicted_class_id]
print(label)