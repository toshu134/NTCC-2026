from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

llm = ChatGroq(
    groq_api_key="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",
    model_name="llama3-70b-8192",
    temperature=0.2
)

prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer the following question:\n\n{question}"
)

chain = prompt | llm

response = chain.invoke({"question": "What is Groq and how is it different from OpenAI?"})
print(response.content.strip())
