import os

########### load environmental variables
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

########### loading a knowladge base


from langchain.document_loaders import Docx2txtLoader
loader = Docx2txtLoader("/your/file/path.docx")
word_documents = loader.load()


# from langchain.document_loaders import GoogleDriveLoader
# loader = GoogleDriveLoader(
#     folder_id="1ySbAQND8cIvtlyUr-LJyrmKitru9xURJ",
#     credentials_path = '/Users/esatcankaya/Downloads/webapp.json'
# )

# docs = loader.load()
# texts = ''
# for i in docs:
#     texts += i.page_content

# Create a SitemapLoader object, providing the URL of the sitemap.xml file and any filtering options
# from langchain.document_loaders import SitemapLoader
# loader = SitemapLoader(
#     "https://otomentor.com/sitemap.xml"
# )
# site_documents = loader.load()



from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(word_documents)

for i, text in enumerate(docs):
    text.metadata["source"] = f"{i}-pl"


########### Initialize OpenAI embeddings
from langchain.embeddings.openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
# Create a vector store (FAISS) index from the loaded documents
from langchain.vectorstores import FAISS
import pickle

store_name = 'otomentor.net_doc'
if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
else:
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_documents(docs, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
