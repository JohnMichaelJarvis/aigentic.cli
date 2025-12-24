import os
from google import genai
from dotenv import load_dotenv


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    print(api_key)
    if api_key == None:
        raise RuntimeError("API Key missing...")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )

    print(response.text)


if __name__ == "__main__":
    main()
