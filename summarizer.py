from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq   # or use ChatGroq / Gemini
from dotenv import load_dotenv

load_dotenv()

# 🔑 Step 1: Initialize LLM
llm =ChatGroq(model="llama-3.3-70b-versatile")

# 🧩 Step 2: Define Prompts

# Chunk-level summary prompt (MAP)
map_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Summarize the following text in 2-3 sentences.
    Keep only the most important information.
    - Ensure factual accuracy and do not overgeneralize roles
- Preserve important events but keep it concise

    Text:
    {text}

    Summary:
    """
)

# Final summary prompt (REDUCE)
reduce_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    Combine the following summaries into one final concise summary.
    Remove repeated points and keep it under 3 sentences.

    Summaries:
    {text}

    Final Summary:
    """
)

# 🧩 Step 3: Create Chains
map_chain = LLMChain(llm=llm, prompt=map_prompt)
reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

# 🧩 Step 4: Function to summarize large text
def summarize_large_text(text):

    if len(text)<1000:
        return map_chain(text)
    
    # 🔹 Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    
    chunks = splitter.split_text(text)

    print(f"Total chunks created: {len(chunks)}")

    # 🔹 Map Step: Summarize each chunk
    summaries = []
    for chunk in chunks:
        summary = map_chain.run(chunk)
        summaries.append(summary)

    # 🔹 Reduce Step: Combine summaries
    combined_text = "\n".join(summaries)
    final_summary = reduce_chain.run(combined_text)

    return final_summary


# 🧪 Step 5: Test
if __name__ == "__main__":
    text=input("Please enter text:")
    result = summarize_large_text(text)
    print("\nFinal Summary:\n", result)