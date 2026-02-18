import torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification

checkPoint = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(checkPoint)
model = AutoModelForSequenceClassification.from_pretrained(checkPoint)

sequence = "Hello this is a trial for handling multiple sequences"

tokenized = tokenizer.tokenize(sequence)

inputIds = tokenizer.convert_tokens_to_ids(tokenized)
tensors = torch.tensor([inputIds])
batch = [inputIds,inputIds]
batchtensor = torch.tensor(batch)

print(tensors)
print(batchtensor)
output = model(tensors)
output2 = model(batchtensor)
print(output.logits)
print(output2.logits)
