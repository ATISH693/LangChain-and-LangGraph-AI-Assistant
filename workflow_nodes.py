from state import FlowState
from rag.retriever import retrieve
from llm import llm
from requests.exceptions import ConnectionError, Timeout
from groq import RateLimitError, AuthenticationError, APIConnectionError, APIStatusError
from langgraph.types import interrupt
from prompt import prompt
import traceback


final_prompt = prompt

def retrieve_docs(state: FlowState):
    """
    Retrieve the most relevant document chunks.
    """

    try:
        chunks, best_score = retrieve(state["question"])

        if not chunks:
            return {
                "chunks": [],
                "best_score": 99999,
                "answer": "No relevant documentation was found for your question.",
                "status": "review",
            }

        return {
            "chunks": chunks,
            "best_score": best_score,
            "status": "retrieve",
        }

    except Exception:
        traceback.print_exc()
        raise
    
THRESHOLD = 0.35

def threshold_check(state: FlowState):

    if state["best_score"] <= THRESHOLD:
        return "generate"

    return "review"

def call_llm(state: FlowState):

    context = "\n\n".join(
        f" Source: { chunk['source'] } \n\n { chunk['content'] } " for chunk in state["chunks"]
        )

    prompt = final_prompt.invoke({"context" : context , "question" : state["question"]})

    try:
        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "status": "finished",
        }

    except RateLimitError:
        return {
            "answer": (
                "The Groq API rate limit has been exceeded. "
                "Please wait a few moments and try again."
            ),
            "status": "error",
        }

    except AuthenticationError:
        return {
            "answer": (
                "Unable to authenticate with the Groq API. "
                "Please check your API key."
            ),
            "status": "error",
        }

    except (APIConnectionError, ConnectionError, Timeout):
        return {
            "answer": (
                "Unable to connect to the Groq API. "
                "Please try again shortly."
            ),
            "status": "error",
        }

    except APIStatusError as e:
        return {
            "answer": (
                f"Groq API returned an error ({e.status_code}). "
                "Please try again later."
            ),
            "status": "error",
        }

    except Exception as e:
        return {
            "answer": (
                f"Unexpected error while generating the answer.\n\n{str(e)}"
            ),
            "status": "error",
        }

def human_review(state: FlowState):

    review_request = {
        "message": "Retrieved documents have low confidence. Human review required.",
        "question": state["question"],
        "best_score": state["best_score"],
        "chunks": state["chunks"]
    }

    decision = interrupt(review_request)

    return {
        "review_decision": decision,
        "status": "review"
    }

def check_human_review(state: FlowState):

    if state["review_decision"] == "approved":
        return "approved"

    return "rejected"

