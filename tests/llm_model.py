from langchain_google_genai import ChatGoogleGenerativeAI

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import GOOGLE_API_KEY

model = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.0-flash", temperature=0.1)
# model.max_output_tokens = 10
model_2 = model.bind(generation_config={"max_output_tokens": 10})

async def test_model():
    async for message in model.astream("Write a 10 liner 100 word poem about the beauty of nature"):
        print(message.content)

# Run the test
asyncio.run(test_model())