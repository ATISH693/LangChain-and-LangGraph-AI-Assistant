import streamlit as st
import requests
import uuid
import time
import json
from database_load import save_message, load_messages, load_threads, delete_thread


API_URL = "http://16.171.68.41:8000"

st.set_page_config(
    page_title="LangGraph RAG AI Assistant",
    layout="wide"
)


# =========================
# SESSION STATE
# =========================

defaults = {
    
    "thread_id":str(uuid.uuid4()),
    "messages":[],
    "first_question":None,
    "chunks":[],
    "latency":0,
    "workflow":[],
    "history": [],
    
    # HUMAN REVIEW

    "waiting_review":False,
    "review_data":None

}



for key,value in defaults.items():

    if key not in st.session_state:

        st.session_state[key]=value

# =========================
# NEW CHAT
# =========================

def new_chat():

    st.session_state.thread_id = str(uuid.uuid4())

    st.session_state.latency = 0

    st.session_state.messages = []

    st.session_state.first_question = None

    st.session_state.chunks = []

    st.session_state.workflow = []

    st.session_state.waiting_review = False

    st.session_state.review_data = None


def load_chat(thread_id, title):

    st.session_state.thread_id = str(thread_id)

    st.session_state.first_question = title

    st.session_state.messages = load_messages(thread_id)

    st.session_state.chunks = []

    st.session_state.workflow = []

    st.session_state.waiting_review = False

    st.session_state.review_data = None

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    
    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):
        new_chat()
        st.rerun()

    st.divider()
    st.caption("📊 SYSTEM")


    st.write("🤖 LLM")
    st.caption("Llama-3.3-70b-versatile")


    st.write("🔢 Embedding")
    st.caption("BAAI/bge-small-en-v1.5")


    st.write("🗄 Vector DB")
    st.caption("Supabase + pgvector")


    st.write("📄 Chunks")
    st.caption(str(len(st.session_state.chunks)))


    st.write("⚡ Latency")
    st.caption(
        f"{st.session_state.latency:.2f}s"
    )



    st.divider()
    st.caption("🧵 CURRENT CHAT")
    
    if st.session_state.first_question:
        
        st.write(
            st.session_state.first_question[:45]
        )

    else:
        st.caption("New conversation")



    st.markdown("---")
    
    st.caption("💬 PREVIOUS CHATS")
    
    st.session_state.history = load_threads()

    for thread_id, title, _ in st.session_state.history:

        col1, col2 = st.columns([5,1])

        with col1:

            if st.button(title[:35], key=f"chat_{thread_id}"):

                load_chat(thread_id, title)

                st.rerun()

        with col2:

            if st.button("🗑️", key=f"delete_{thread_id}"):

                delete_thread(thread_id)

                st.session_state.history = load_threads()

                if thread_id == st.session_state.thread_id:
                    new_chat()

                st.rerun()

# =========================
# MAIN
# =========================
st.title("🤖 LangGraph RAG AI Assistant")


st.divider()

st.subheader("💬 Conversation")

for msg in st.session_state.messages:

    role = msg["role"]

    if role == "system":

        st.divider()

    else:

        with st.chat_message(role):
            st.write(msg["content"])

# =========================
# ASK
# =========================
question = st.chat_input( "Enter your Question...")

if question:
    
    if st.session_state.first_question is None:
        st.session_state.first_question=question

    st.session_state.messages.append( { "role":"user", "content":question } )



    workflow=[]
    workflow_box=st.empty()
    start=time.time()

    response=requests.post(

        f"{API_URL}/ask",

        json={
            "question":question,
            "thread_id": str(st.session_state.thread_id)
        },

        stream=True,
        timeout=180
    )

    answer=None
    chunks=[]

    for line in response.iter_lines():
        if not line:
            continue

        event=json.loads( line.decode() )
        
        # ======================
        # THREAD
        # ======================
        if event.get("type")=="thread":
            st.session_state.thread_id = ( event["thread_id"] )

            if event.get("type") == "thread":

                st.session_state.thread_id = event["thread_id"]

                workflow.append("📩 Question received")

                save_message(
                    st.session_state.thread_id,
                    question,
                    "user",
                    question
                )

        # ======================
        # RETRIEVAL
        # ======================
        elif "retrieve_docs" in event:
            
            data=event["retrieve_docs"]
            
            chunks=data["chunks"]
            
            workflow.append( f"📄 Retrieved {len(chunks)} chunks" )

        # ======================
        # INTERRUPT
        # ======================
        elif event.get("type")=="interrupt":
            
            review=event["value"]
            
            st.session_state.waiting_review=True

            st.session_state.review_data=review
            
            chunks=review["chunks"]
            
            workflow.append("⚠️ Human review required")

        # ======================
        # ANSWER
        # ======================
        
        elif "generate_answer" in event:
            
            workflow.append( "🤖 Generating answer" )
            
            answer=( event["generate_answer"]["answer"] )

        workflow_box.markdown( "### ⚙️ Workflow\n\n" + "\n\n".join(workflow) )

    st.session_state.latency=time.time()-start

    st.session_state.workflow=workflow

    st.session_state.chunks=chunks

    if answer:
        
        workflow.append("✅ Completed")

        workflow_box.markdown( "### ⚙️ Workflow\n\n" + "\n\n".join(workflow) )

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

        save_message(
            st.session_state.thread_id,
            question,
            "assistant",
            answer
        )

        st.session_state.history = load_threads()

    st.rerun()

# =========================
# HUMAN REVIEW
# =========================

if st.session_state.waiting_review:
    
    st.divider()
    
    st.subheader("⚠️ HUMAN REVIEW REQUIRED")
    
    review = st.session_state.review_data

    st.warning( review["message"] )
    
    st.write( "Question:" )

    st.info( review["question"] )


    st.write( f"Confidence Score: {review['best_score']:.3f}" )
    
    col1, col2 = st.columns(2)

    # =====================
    # APPROVE
    # =====================

    with col1:
        if st.button( "✅ Approve", use_container_width=True):
            
            workflow_box = st.empty()
            
            workflow = []
            
            workflow.append( "✅ Human approved" )

            workflow.append( "🤖 Generating answer" )

            workflow_box.markdown( "### ⚙️ Workflow\n\n" + "\n\n".join(workflow) )
            
            response = requests.post(

                f"{API_URL}/resume",

                json={
                    "thread_id": str(st.session_state.thread_id),
                    "decision":"approved"
                },
                
                timeout=180
            )
            
            data = response.json()
            
            if data.get("status") == "finished":
                
                answer = data["answer"]

                workflow.append( "✅ Completed" )
                
                workflow_box.markdown( "### ⚙️ Workflow\n\n" + "\n\n".join(workflow) )
                
                st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":answer
                }
            )

                save_message(
                    st.session_state.thread_id,
                    question,
                    "assistant",
                    answer
                )

                st.session_state.history = load_threads()
                
            else:
                
                st.session_state.messages.append(

                    {
                    "role":"assistant",
                    "content": "Unable to generate an answer."
                    }
                )
                
                save_message(
                    st.session_state.thread_id,
                    question,
                    "assistant",
                    "I couldn't generate a reliable answer for this question. Please try asking something else related to the available documents."
                )

                st.session_state.history = load_threads()
            
            st.session_state.waiting_review=False

            st.session_state.review_data=None
            
            st.rerun()

    # =====================
    # REJECT
    # =====================

    with col2:
        if st.button( "❌ Reject",  use_container_width=True ):
            
            requests.post(

                f"{API_URL}/resume",

                json={
                    "thread_id": str(st.session_state.thread_id),
                    "decision": "rejected"
                },

                timeout=180
            )


            st.session_state.messages.append(
                {
                "role":"assistant",
                "content":"I couldn't generate a reliable answer for this question. Please try asking something else related to the available documents."
                }
            )

            save_message(
                st.session_state.thread_id,
                st.session_state.first_question,
                "assistant",
                "I couldn't generate a reliable answer for this question. Please try asking something else related to the available documents."
            )

            st.session_state.history = load_threads()
            
            st.session_state.waiting_review=False
            
            st.session_state.review_data=None
            
            st.rerun()

# =========================
# SOURCES
# =========================

if st.session_state.chunks:
    
    st.divider()
    
    st.subheader( "📚 Retrieved Sources" )
    
    for chunk in st.session_state.chunks:
        
        with st.expander( chunk["source"] ):
            
            st.caption( f"Similarity: {chunk['score']:.3f}" )
            
            st.write( chunk["content"][:500] )