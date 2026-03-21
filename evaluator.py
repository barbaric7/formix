from llm_engine import ask_model
from config import PRIMARY_MODEL, SECONDARY_MODEL


def get_final_answer(question, options):
    print("Querying Primary Model...")
    primary = ask_model(PRIMARY_MODEL, question, options)
    print("Primary:", primary)

    print("Querying Secondary Model...")
    secondary = ask_model(SECONDARY_MODEL, question, options)
    print("Secondary:", secondary)

    if primary and secondary:
        if primary.lower() == secondary.lower():
            print("Agreement reached")
            return primary
        else:
            print("Disagreement — using primary")
            return primary

    return primary or secondary