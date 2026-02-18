from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
inputWords = ["I've been waiting for a hugging face course entire life ","I hate this so much!"]

tokenizedWords = tokenizer.tokenize(inputWords)
tokenizedIds = tokenizer.convert_tokens_to_ids(tokenizedWords)
print(tokenizedWords)
print(tokenizedIds)
print(tokenizer.decode(tokenizedIds))
