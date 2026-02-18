import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client=Groq(
    api_key=os.getenv("API_KEY")
)

def PetCat():
    print("You are petting the cat")
    return "Cat is petted"

def AI_CAT():
        messages = [{"role": "system",
                    "content": "You are a cat that only can say meow as answer"+"Be kittenish answer as the tone of the input."}]
        tools = [{
            "type":"function",
            "function":{
                 "name":"PetCat",
                 "description":"pets the cat",
                 "parameters": {
                   "type": "object",
                   "properties": {}, 
                   "required": []
               }
            }
        }]
        prompt =""
        while True:
            prompt = input("You: ")
            if prompt.lower() == "exit":
                break
            if prompt.lower() == "pet":
                messages.append({"role": "user", "content": prompt})
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",
                    tools=tools,
                    tool_choice="auto"
                )
                response_message = chat_completion.choices[0].message
                tool_calls = response_message.tool_calls
                if tool_calls:
                    messages.append(response_message)
                    available_functions={
                        "PetCat":PetCat,
                    }
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_to_call = available_functions[function_name]
                        function_return_value = function_to_call()
                        messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_return_value,
                    })
                    second_response = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",
                )
                    final_answer = second_response.choices[0].message.content
                    messages.append({"role": "assistant", "content": final_answer})
                    print(f"AI: {final_answer}")
            else:   
                messages.append({"role":"user","content":prompt})
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.1-8b-instant",
                    temperature=1,
                    max_tokens=1024,
                )
                API_answer = chat_completion.choices[0].message.content
                messages.append({"role":"assistant","content":API_answer})
                print("AI:",API_answer)

if __name__ == "__main__":
    AI_CAT()