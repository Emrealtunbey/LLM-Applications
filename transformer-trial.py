from transformers import pipeline

generator = pipeline("text-generation",framework="pt")
result = generator("In this course, we will teach you how to",num_return_sequences=2,max_length=15)
print(result)