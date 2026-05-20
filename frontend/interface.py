import streamlit as st
import requests
import json

st.set_page_config(page_title="Banking AI Agent", layout="centered")
st.title("Banking Customer Support")
st.subheader("Powered by Multimodal AI & gRPC")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("AI is analyzing and drafting response...")
        
        try:
            response = requests.post(
                "http://localhost:8000/run-agent",
                json={"message": prompt},
                timeout=120 
            )
            
            if response.status_code == 200:
                result = response.json()
                full_response = result.get("response", "I'm sorry, I couldn't generate a response.")
                message_placeholder.markdown(full_response)
                
                # Display trace information
                if result.get("intent"):
                    st.divider()
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Intent", result.get("intent", "Unknown"))
                    with col2:
                        confidence = result.get("confidence", 0)
                        st.metric("Confidence", f"{confidence:.2%}")
                    with col3:
                        st.metric("Status", result.get("action", "Unknown").replace("_", " ").title())
                # Lưu vào lịch sử
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                message_placeholder.markdown(error_msg)
                
        except requests.exceptions.Timeout:
            message_placeholder.markdown(" **Timeout:** The AI model is taking too long to respond. Please check your Colab status.")
        except requests.exceptions.ConnectionError:
            message_placeholder.markdown(" **Connection Error:** Backend (run.py) is not running or port 8000 is blocked.")
        except Exception as e:
            message_placeholder.markdown(f" **Unexpected Error:** {e}")

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()