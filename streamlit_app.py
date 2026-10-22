
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="FinSolve AI Assistant",
    page_icon="💼",
    layout="centered",
)

st.title("FinSolve AI Assistant")
st.write("Ask questions about FinSolve company documents.")

role = st.selectbox(
    "Choose a department role",
    [
        "employee",
        "engineering",
        "finance",
        "hr",
        "marketing",
        "executive",
    ],
)

question = st.text_area(
    "Enter your question",
    placeholder="Example: What are FinSolve's marketing campaign results?",
)

if st.button("Ask FinSolve", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner(
                "Searching documents and generating an answer..."
            ):
                response = requests.post(
                    API_URL,
                    headers={"x-user-role": role},
                    json={
                        "question": question.strip(),
                    },
                    timeout=120,
                )

            if response.ok:
                result = response.json()

                st.subheader("Answer")
                st.write(
                    result.get("answer", "No answer returned.")
                )

                st.subheader("Sources")
                sources = result.get("sources", [])

                if sources:
                    for source in sources:
                        st.write(
                            f"- {source['source']} "
                            f"(Department: {source['department']})"
                        )
                else:
                    st.info("No source documents were returned.")

            else:
                st.error(
                    f"API error ({response.status_code})"
                )
                st.write(response.text)

        except requests.RequestException as error:
            st.error(
                "Could not connect to the API. "
                "Check that FastAPI is running in the first terminal."
            )
            st.caption(str(error))
