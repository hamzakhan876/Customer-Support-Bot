
import requests
import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Customer Support AI",
    page_icon="💬",
    layout="centered",
)

API_URL = "http://127.0.0.1:8000/chat"

# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Header
# -----------------------------
st.title("💬 Customer Support AI")
st.caption("Your AI assistant for orders, returns, and refunds.")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.subheader("Chat settings")
    st.write("Ask a question about your order, return, or refund.")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Display chat history
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("source"):
            st.caption(
                f"Knowledge base source: {message['source']}"
            )

# -----------------------------
# Chat input
# -----------------------------
if prompt := st.chat_input("How can I help you today?"):
    # Display and save the customer's message.
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the message to FastAPI.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": prompt},
                    timeout=60,
                )
                response.raise_for_status()
                result = response.json()

                answer = result.get(
                    "answer",
                    "Sorry, I couldn't generate a response.",
                )

                st.markdown(answer)

                if result.get("source"):
                    st.caption(
                        f"Knowledge base source: {result['source']}"
                    )

                # Save the answer for future reruns.
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "source": result.get("source"),
                    }
                )

            except requests.exceptions.RequestException:
                answer = (
                    "I couldn't connect to the support service. "
                    "Please check that the FastAPI backend is running "
                    "and try again."
                )

                st.error(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "source": None,
                    }
                )
