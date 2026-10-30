#!/usr/bin/env python3
"""
Hermes Black Bird - Tool Calling Verification Script
Validates multi-step function/tool calling with Hermes-3-Llama-3.1-70B-FP8 on vLLM.
"""

import json
from openai import OpenAI

def test_hermes_tools(base_url="http://localhost:8000/v1"):
    client = OpenAI(base_url=base_url, api_key="EMPTY")

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "دریافت دمای فعلی آب و هوای یک شهر بر حسب درجه سانتیگراد",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "نام شهر مورد نظر"}
                    },
                    "required": ["city"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "celsius_to_fahrenheit",
                "description": "تبدیل درجه سانتیگراد (سلسیوس) به فارنهایت",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "celsius": {"type": "number", "description": "دما بر حسب سانتیگراد"}
                    },
                    "required": ["celsius"]
                }
            }
        }
    ]

    messages = [
        {"role": "user", "content": "آب‌وهوای تهران چند درجه فارنهایت است؟ ابتدا از ابزار آب‌وهوا استفاده کن، سپس دما را تبدیل کن."}
    ]

    print("Sending tool-calling request to Hermes-3...")
    res = client.chat.completions.create(
        model="NousResearch/Hermes-3-Llama-3.1-70B-FP8",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.1,
        max_tokens=512
    )

    choice = res.choices[0]
    print(f"Finish Reason: {choice.finish_reason}")
    if choice.message.tool_calls:
        print("✅ Tool calls detected:")
        for tc in choice.message.tool_calls:
            print(f" - Tool: {tc.function.name}")
            print(f"   Args: {tc.function.arguments}")
    else:
        print("Model Text Response:")
        print(choice.message.content)

if __name__ == "__main__":
    test_hermes_tools()
