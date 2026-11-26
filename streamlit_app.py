import streamlit as st
from app.llm_service import get_llm_response

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
                result = get_llm_response(
                    question=question.strip(),
                    user_role=role,
                )

            # Support either a dict response (like {"answer": ..., "sources": ...}) or a plain string
            if isinstance(result, dict):
                answer = result.get("answer", "No answer returned.")
                sources = result.get("sources", [])
            else:
                answer = result
                sources = []

            st.subheader("Answer")
            st.write(answer)

            st.subheader("Sources")
            if sources:
                for source in sources:
                    if isinstance(source, dict):
                        st.write(
                            f"- {source.get('source', 'Unknown')} "
                            f"(Department: {source.get('department', 'N/A')})"
                        )
                    else:
                        st.write(f"- {source}")
            else:
                st.info("No source documents were returned.")
        except Exception as error:
            st.error("Failed to generate an answer.")
            st.caption(str(error))
