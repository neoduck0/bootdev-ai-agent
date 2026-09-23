import argparse
import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            temperature=0,
            messages=messages,
            tools=available_functions,
        )

        if response.usage == None:
            raise RuntimeError("response.usage is None, likely failed API request")

        if args.verbose:
            print(f"User prompt: {response.usage.prompt_tokens}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        tool_calls = message.tool_calls
        if tool_calls != None:
            for tool_call in tool_calls:
                arguments: dict[str, str] = json.loads(
                    tool_call.function.arguments or "{}"
                )
                print(f"- Calling function: {tool_call.function.name}")
                result = call_function(tool_call, args.verbose)
                messages.append(result)
                if args.verbose:
                    print(f"-> {result['content']}")

        if message.content != None:
            print(message.content)

        if tool_calls == None:
            exit(0)

    print("Error: something went wrong")
    exit(1)


if __name__ == "__main__":
    main()
