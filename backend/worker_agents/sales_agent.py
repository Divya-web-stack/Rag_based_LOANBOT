def sales_agent(query: str) -> str:
    offers = {
        "personal": "Personal loan @ 10.5% interest, tenure up to 5 years.",
        "home": "Home loan @ 8.2% interest, tenure up to 20 years."
    }
    if "personal" in query.lower():
        return offers["personal"]
    elif "home" in query.lower():
        return offers["home"]
    else:
        return "We have personal and home loans available. Which would you like to explore?"
