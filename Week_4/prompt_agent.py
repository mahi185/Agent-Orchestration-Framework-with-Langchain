# ==============================
# TOOL DEFINITIONS
# ==============================

def web_search(query):
    return f"[Web Search Result] Latest information about: {query}"

def code_executor(query):
    numbers = [int(x) for x in query.split() if x.isdigit()]
    if numbers:
        return f"[Code Execution Result] Sum = {sum(numbers)}"
    return "[Code Execution Result] Nothing to calculate"

def file_creator(query):
    return "[File Created] Document created successfully"


# ==============================
# DYNAMIC REASONING ENGINE
# ==============================

def reasoning_answer(query):
    q = query.lower().strip()

    # Dynamic "what is" questions
    if q.startswith("what is "):
        topic = q.replace("what is ", "").strip()
        return (
            f"{topic.capitalize()} is a commonly used term in technology or academics. "
            f"It refers to a concept, system, or idea related to its domain. "
            f"The exact meaning depends on how {topic} is applied in practice."
        )

    # Dynamic "define" questions
    if q.startswith("define "):
        topic = q.replace("define ", "").strip()
        return (
            f"{topic.capitalize()} is defined as a fundamental concept "
            f"used to explain ideas within a specific field."
        )

    # Dynamic "explain" questions
    if q.startswith("explain "):
        topic = q.replace("explain ", "").strip()
        return (
            f"{topic.capitalize()} can be explained as a process or concept "
            f"that plays an important role in its respective domain."
        )

    # Generic fallback
    return "This is a theoretical question that can be answered using reasoning without external tools."


# ==============================
# AGENT DECISION LOGIC
# ==============================

def ai_agent(user_query):

    print("\n--- USER QUERY ---")
    print(user_query)

    q = user_query.lower()

    if any(word in q for word in ["latest", "current", "today"]):
        print("\n[Agent Decision] Tool required: Web Search")
        return web_search(user_query)

    elif any(word in q for word in ["calculate", "sum", "add"]):
        print("\n[Agent Decision] Tool required: Code Execution")
        return code_executor(user_query)

    elif any(word in q for word in ["create file", "pdf", "document"]):
        print("\n[Agent Decision] Tool required: File Creation")
        return file_creator(user_query)

    else:
        print("\n[Agent Decision] No tool needed")
        return reasoning_answer(user_query)


# ==============================
# MAIN PROGRAM
# ==============================

if __name__ == "__main__":
    while True:
        user_input = input("\nAsk something (or type 'exit'): ")

        if user_input.lower() == "exit":
            print("Agent stopped.")
            break

        result = ai_agent(user_input)

        print("\n--- FINAL ANSWER ---")
        print(result)
