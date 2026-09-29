"""
Sample queries used to validate the Agentic AI RAG chatbot.

These queries cover:
1. Definition
2. Memory
3. System components
4. Comparison with traditional automation
5. Out-of-context question
6. Planning
"""

SAMPLE_QUERIES = [
    "What is Agentic AI?",
    "What is the role of memory in Agentic AI?",
    "What are the main components of an Agentic AI system?",
    "How is Agentic AI different from traditional automation?",
    "Who won the 2022 FIFA World Cup?",
    "What is the role of planning in Agentic AI?",
]


if __name__ == "__main__":
    for number, query in enumerate(SAMPLE_QUERIES, start=1):
        print(f"{number}. {query}")