import argparse
import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from config import model_name
from functions.call_function import available_functions, call_function


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key missing...")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        done = generate_content(client, args, messages)
        if done:
            return

    print("Error: Prompt failed to produce a result.")
    sys.exit(1)


def generate_content(client, args, messages):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("API response usage metadata is empty")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return True

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, args.verbose)
        if not result.parts:
            raise Exception("Error: function_call_result.parts is empty")
        if not result.parts[0].function_response:
            raise Exception("Error: .parts[0].function_response is empty")
        function_responses.append(result.parts[0])

        if args.verbose:
            print(f"-> {result.parts[0].function_response.response}")
    messages.append(types.Content(role="user", parts=function_responses))
    return False


if __name__ == "__main__":
    main()
