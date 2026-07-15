import json
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from langgraph.types import Command
from workflow import workflow
from fastapi.responses import StreamingResponse


app = FastAPI()


class AskRequest(BaseModel):
    question: str


class ReviewRequest(BaseModel):
    thread_id: str
    decision: Literal["approved", "rejected"]


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/ask")
def ask(request: AskRequest):

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "question": request.question,
        "chunks": [],
        "best_score": 0.0,
        "answer": None,
        "review_decision": None,
        "status": "retrieve"
    }

    def event_generator():

        yield json.dumps({
            "type": "thread",
            "thread_id": thread_id
        }) + "\n"

        for event in workflow.stream(
            initial_state,
            config=config,
            stream_mode="updates",
        ):

            # Handle interrupt
            if "__interrupt__" in event:

                intr = event["__interrupt__"][0]

                yield json.dumps({
                    "type": "interrupt",
                    "value": intr.value,
                }) + "\n"

                continue

            # Normal updates
            yield json.dumps(event) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )


@app.post("/resume")
def resume(request: ReviewRequest):

    config = {"configurable": { "thread_id": request.thread_id} }

    result = workflow.invoke(
        Command(resume=request.decision),
        config=config
    )

    return {
        "thread_id": request.thread_id,
        "status": result["status"],
        "answer": result.get("answer")
    }

