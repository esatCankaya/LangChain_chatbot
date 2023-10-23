########### Import necessary libraries and modules
import os
import pickle

from langchain.chat_models import ChatOpenAI
from langchain.chains import create_qa_with_sources_chain
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.memory import ConversationSummaryMemory
from langchain.chains import LLMChain
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

########### load environmental variables
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

# Access vector store from local files
store_name = 'your_db'
with open(f"{store_name}.pkl", "rb") as f:
    VectorStore = pickle.load(f)

########## Initialize a ChatOpenAI model
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

########### Create a QA chain with sources
qa_chain = create_qa_with_sources_chain(llm)

########### Define a document template for prompts
doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

########### Create a chain to combine documents
final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain,
    document_variable_name="context",
    document_prompt=doc_prompt
)

############ Create a RetrievalQA instance
retrieval_qa = RetrievalQA(
    retriever=VectorStore.as_retriever(), 
    combine_documents_chain=final_qa_chain,
    verbose = True
)

############ Initialize a memory for conversation history
memory = ConversationSummaryMemory(llm=llm,memory_key="chat_history", return_messages=True)

############# Define a template for condensing follow-up questions
REPHRASE_TEMPLATE = """ 
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:
"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(REPHRASE_TEMPLATE)

############ Create a chain for condensing questions
condense_question_chain = LLMChain(
    llm=llm,
    prompt=CONDENSE_QUESTION_PROMPT,
    verbose=True
)

############# Create a ConversationalRetrievalChain
qa = ConversationalRetrievalChain(
    question_generator=condense_question_chain,
    combine_docs_chain=final_qa_chain,
    retriever=VectorStore.as_retriever(),
    memory=memory
)

# ########### Query for information and rephrase a follow-up question
query = "ask a question"
result = qa({"question": query})
print(result["answer"])

############ Another example query
# query = "your questin"
# result = qa({"question": query})
# print(result["answer"])
