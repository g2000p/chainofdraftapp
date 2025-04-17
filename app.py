import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# Set the title of the Streamlit app
st.title("ChainOfDraftApp")

# Sidebar for configuration options
st.sidebar.header("Configuration")

# Sample parameter for number of reasoning steps
num_steps = st.sidebar.slider("Number of Reasoning Steps", min_value=1, max_value=10, value=5, step=1)
token_limit = st.sidebar.slider("Token Limit per Step", min_value=1, max_value=10, value=5, step=1)
show_comparison = st.sidebar.checkbox("Show CoT vs CoD Comparison", value=True)

# Helper function to simulate Chain of Draft reasoning
def chain_of_draft(num_steps, token_limit):
    steps = []
    for i in range(num_steps):
        step = f"Step {i+1}: {' '.join(['word'] * token_limit)}"
        steps.append(step)
    return steps

# Helper function to simulate Chain of Thought reasoning
def chain_of_thought(num_steps):
    steps = []
    for i in range(num_steps):
        step = f"Step {i+1}: Detailed explanation of step {i+1}."
        steps.append(step)
    return steps

# Main panel with outputs
st.header("Chain of Draft Reasoning")

# Show the reasoning steps for Chain of Draft
st.subheader("Chain of Draft Steps")
cod_steps = chain_of_draft(num_steps, token_limit)
for step in cod_steps:
    st.text(step)

# Show the comparison if selected
if show_comparison:
    st.header("Comparison with Chain of Thought")

    # Show the reasoning steps for Chain of Thought
    st.subheader("Chain of Thought Steps")
    cot_steps = chain_of_thought(num_steps)
    for step in cot_steps:
        st.text(step)

# Simulate and display latency and token usage
def simulate_latency_and_tokens():
    cod_latency = np.random.uniform(0.5, 1.5) * num_steps / token_limit
    cot_latency = np.random.uniform(1.5, 3.0) * num_steps
    cod_tokens = np.random.randint(5, 15) * num_steps / token_limit
    cot_tokens = np.random.randint(20, 30) * num_steps
    return cod_latency, cot_latency, cod_tokens, cot_tokens

cod_latency, cot_latency, cod_tokens, cot_tokens = simulate_latency_and_tokens()

# Display latency and token usage
st.header("Performance Metrics")

col1, col2 = st.columns(2)
col1.metric("CoD Latency (s)", f"{cod_latency:.2f}")
col1.metric("CoT Latency (s)", f"{cot_latency:.2f}")

col2.metric("CoD Tokens", f"{int(cod_tokens)}")
col2.metric("CoT Tokens", f"{int(cot_tokens)}")

# Visualization of performance metrics
st.subheader("Performance Visualization")
fig, ax = plt.subplots()
methods = ['Chain of Draft', 'Chain of Thought']
latencies = [cod_latency, cot_latency]
tokens = [cod_tokens, cot_tokens]

ax.barh(methods, latencies, color=['blue', 'red'])
ax.set_xlabel('Latency (s)')
ax.set_title('Latency Comparison')
st.pyplot(fig)

fig, ax = plt.subplots()
ax.barh(methods, tokens, color=['blue', 'red'])
ax.set_xlabel('Token Usage')
ax.set_title('Token Usage Comparison')
st.pyplot(fig)

# Add a download button for results
st.sidebar.header("Download Results")
if st.sidebar.button("Download"):
    result_df = pd.DataFrame({
        "Method": methods,
        "Latency": latencies,
        "Tokens": tokens
    })
    st.sidebar.download_button(
        label="Download metrics as CSV",
        data=result_df.to_csv(index=False),
        file_name='performance_metrics.csv',
        mime='text/csv'
    )

st.sidebar.header("Instructions")
st.sidebar.info("""
- Adjust the number of reasoning steps and token limit using the sliders.
- Toggle the comparison view to see detailed steps for Chain of Thought.
- Observe the latency and token usage changes based on parameters.
- Download the performance metrics for further analysis.
""")