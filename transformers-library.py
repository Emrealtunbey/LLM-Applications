from transformers import pipeline

text_generator = pipeline("text-generation",framework="pt")
summarizer = pipeline("summarization",framework="pt")
translator = pipeline("translation",framework="pt",model="ckartal/english-to-turkish-finetuned-model")

generate_input = "In this course, we will teach you how to"
summarize_input = """
Artificial Intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. 
It includes areas such as machine learning, natural language processing, and computer vision. 
AI systems are used in various industries including healthcare, finance, and transportation. 
In recent years, AI has seen rapid growth due to advances in computing power and the availability of large datasets.
"""
translate_input = "Artificial intelligence is transforming the world."

text_result = text_generator(generate_input)
summarized_result = summarizer(summarize_input)
translated_result = translator(translate_input)

print("Generated text:",text_result)
print("summarized text:",summarized_result)
print("translated text:",translated_result)