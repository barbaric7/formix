import requests
import time
from collections import Counter
from config import OPENROUTER_API_KEY

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# 🔥 Best 3 Models (Fast + Stable + Good Reasoning)
MODELS = [
    "openai/gpt-3.5-turbo",
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.2-3b-instruct:free"
]

# Test Question
QUESTION = "What is 2 + 2?"
OPTIONS = """
A) 3
B) 4
C) 5
D) 22
"""

PROMPT = f"""
You are solving a multiple choice question.

Question:
{QUESTION}

Options:
{OPTIONS}

Return ONLY the exact correct option text exactly as written above.
No explanation.
"""


def ask_model(model):
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": PROMPT}
        ]
    }

    start_time = time.time()

    try:
        response = requests.post(URL, json=payload, headers=HEADERS)
        data = response.json()

        if "choices" not in data:
            print(f"\n❌ Error from {model}: {data}")
            return None, 0

        answer = data["choices"][0]["message"]["content"].strip()
        response_time = round(time.time() - start_time, 2)

        return answer, response_time

    except Exception as e:
        print(f"\n❌ Exception from {model}: {e}")
        return None, 0


def majority_vote(results):
    valid_answers = [r for r in results if r is not None]

    if not valid_answers:
        return None, 0

    counter = Counter(valid_answers)
    final_answer, count = counter.most_common(1)[0]

    confidence = round((count / len(valid_answers)) * 100, 2)

    return final_answer, confidence


def main():
    print("🚀 Testing Multi-Model LLM System\n")

    primary = "openai/gpt-3.5-turbo"
    secondary = "meta-llama/llama-3.1-8b-instruct"
    fallback = "google/gemma-3-4b-it:free"

    print(f"→ Querying {primary}...")
    ans1, t1 = ask_model(primary)

    print(f"→ Querying {secondary}...")
    ans2, t2 = ask_model(secondary)

    if not ans1 or not ans2:
        print("❌ One of the main models failed.")
        return

    print(f"\nPrimary: {ans1}")
    print(f"Secondary: {ans2}")

    if ans1.lower() == ans2.lower():
        print("\n✅ Agreement reached")
        print("🔥 Confidence: HIGH (100%)")
        print(f"Final Answer: {ans1}")
    else:
        print("\n⚠ Disagreement detected. Calling fallback model...")

        ans3, t3 = ask_model(fallback)

        if not ans3:
            print("❌ Fallback failed.")
            return

        print(f"Fallback: {ans3}")

        answers = [ans1.lower(), ans2.lower(), ans3.lower()]
        final = max(set(answers), key=answers.count)
        confidence = round((answers.count(final)/3)*100,2)

        print(f"\nFinal Answer: {final}")
        print(f"🔥 Confidence: {confidence}%")

if __name__ == "__main__":
    main()