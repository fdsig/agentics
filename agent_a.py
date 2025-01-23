from openai import OpenAI
import subprocess
import os
import dotenv

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": """
     You are a coding agent your job is to write high quality 
     runnable code that will be ouput to a python file
     
     Please think carefully about the code you are writing and the requirements you are given.
     
     Please ouput code only so that this can be parsed and save to a file -- this should start 
     like a normal python file and not have any other text or comments
     
     eg this ```python
def sum_of_numbers(numbers):
    return sum(numbers)
```
     should simply be 
     def sum_of_numbers(numbers):
        return sum(numbers)
     """
     },
    {"role": "user", "content": 
     """
     write a function that will take a list of numbers and return the sum of the numbers

     Please provide input and have the fuciont call on some input and return the output

     this should be a runnable file.
     """
     },
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

print(response.choices[0].message.content)

def strip_code_block_markers(code_block: str) -> str:
    """
    Removes surrounding ```python or ``` markers from the given code block string.
    """
    # Strip leading/trailing whitespace and split into lines
    lines = code_block.strip().splitlines()
    
    # If the first line starts with ```python or ```
    if lines and (lines[0].startswith("```python") or lines[0].startswith("```")):
        lines.pop(0)
    
    # If the last line starts with ```
    if lines and lines[-1].startswith("```"):
        lines.pop()
    
    return "\n".join(lines)

with open("agent.py", "w") as f:
    f.write(strip_code_block_markers(response.choices[0].message.content))

result = subprocess.run(["python", "agent.py"], input="1,2,3,4,5\n", text=True)

print(result.stdout)

# adnother call to open ai wth result
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"""
     The result of the code was: {result.stdout} \n\n can you reverse this content and give me the original input that was used to generate this output \n\n please provide the input in a list format
     """},
]

response = client.chat.completions.create(model="gpt-4o", messages=messages)
print(response.choices[0].message.content)
