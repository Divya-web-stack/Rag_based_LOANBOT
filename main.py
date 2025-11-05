from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rules import check_eligibility
from rag import search_policies

app = FastAPI()

# serve static HTML frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatInput(BaseModel):
    user: str
    message: str

@app.post("/chat")
async def chat(input: ChatInput):
    msg = input.message.lower()
    if "apply" in msg or "loan" in msg:
        return {"reply": "Sure! Can I know your monthly income and credit score?"}
    elif "income" in msg or "credit" in msg:
        income = 50000
        credit = 720
        decision = check_eligibility(income, credit)
        if decision == "approve":
            return {"reply": "🎉 Congratulations! Your loan is approved instantly."}
        elif decision == "review":
            return {"reply": "We’ll need to verify your salary slip before approval."}
        else:
            return {"reply": "Sorry, you’re not eligible for this loan at the moment."}
    elif "policy" in msg:
        doc = search_policies(msg)
        return {"reply": f"According to our policy: {doc}"}
    else:
        return {"reply": "Hi! I’m your AI loan assistant. Type 'apply for a loan' to start."}
