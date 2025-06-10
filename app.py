# Frontend: app.py
# ----------------
"""import streamlit as st
from Backend import configure, create_agents

configure()
agents = create_agents()

st.set_page_config(page_title="AI Profile Evaluator", layout="centered")
st.title("AI Profile Evaluator: Split Backend/Frontend")

profile_text = st.text_area("Paste profile text:", height=300)
if st.button("Evaluate Profile"):
    if not profile_text.strip():
        st.error("Enter profile text.")
    else:
        with st.spinner():
            results = {}
            for key, (agent, scorer) in agents.items():
                items = agent.run(profile_text)
                score = scorer.run(items)
                results[key] = {"items": items, "score": score}
        # Display
        mapping = {"Rec":"Reach","Mag":"Magnitude","Imp":"Impact"}
        for k, data in results.items():
            st.subheader(mapping[k])
            for it in data["items"]:
                st.write(f"- {it}")
            st.json(data["score"])"""

import streamlit as st
from Backend import configure, create_agents

configure()
agents = create_agents()

st.set_page_config(page_title="AI Profile Evaluator", layout="centered")
st.title("AI Profile Evaluator")

profile_text = st.text_area("Paste profile text:", height=300)

if st.button("Evaluate Profile"):
    if not profile_text.strip():
        st.error("Please enter profile text.")
    else:
        with st.spinner("Analyzing profile..."):
            results = {}
            for key, (agent, scorer) in agents.items():
                categorized = agent.run(profile_text)
                score = scorer.run(categorized)
                results[key] = {"categorized": categorized, "score": score}

        label_map = {"Rec": "Reach", "Mag": "Magnitude", "Imp": "Impact"}

        for key, result in results.items():
            st.subheader(f"{label_map[key]} Categorization")
            st.json(result["categorized"])

            st.subheader(f"{label_map[key]} Scoring")
            st.json(result["score"])

