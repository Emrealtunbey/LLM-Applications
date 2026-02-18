from datasets import load_dataset
from transformers import AutoTokenizer

checkpoint = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

raw_datasets = load_dataset("glue","mrpc")
trainSet = raw_datasets["train"]
validationSet = raw_datasets["validation"]

print(trainSet[14])
print(validationSet[86])

tokenized = tokenizer(trainSet[14]["sentence1"],trainSet[14]["sentence2"],padding=True,return_tensors="pt")
tokenized2 = tokenizer(trainSet[14]["sentence1"],return_tensors="pt")
tokenized3 = tokenizer(trainSet[14]["sentence2"],return_tensors="pt")

print(tokenized)
print(tokenized2)
print(tokenized3)


