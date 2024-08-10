import requests
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import BaseLLM

class RestLLM(BaseLLM):
    def __init__(self, api_url, api_key, **kwargs):
        super().__init__(**kwargs)
        self.api_url = api_url
        self.api_key = api_key

    def _call(self, prompt, stop=None):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'max_tokens': 150  # Adjust based on your needs
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get('text')

    @property
    def _llm_type(self):
        return "custom_llm"

# Replace with your actual API endpoint and key
api_url = 'https://poligpt.upv.es/api/SmarTenderAI/ollama'
api_key = 'AwywzdkE6czYzoCG2YRvBpcwBbyxmOjsb82gQXEV2ZMPUcgnKtLYXwWD879PlPTo'

# Create an instance of the RestLLM class
llm = RestLLM(api_url=api_url, api_key=api_key)

# Define a simple prompt template
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="Question: {question}\nAnswer:"
)

# Create an LLMChain instance
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

# Query the Llama 3 model via the REST API
question = "What is the capital of France?"
answer = llm_chain.run({"question": question})
print(answer)
