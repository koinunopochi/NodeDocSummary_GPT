from langchain.document_loaders import UnstructuredURLLoader
import list
import uuid
def content_loader():
  urls = list.urls
  loader = UnstructuredURLLoader(urls=urls)

  data = loader.load()
  print(data)

  for x in data:
      file_name = str(uuid.uuid3(uuid.NAMESPACE_URL, x.metadata["source"]))
      with open("./node.js/"+file_name+".txt", 'w', encoding='utf-8') as f:
          f.write(x.metadata["source"]+"\n")
          f.write(x.page_content)


import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import StorageContext, load_index_from_storage, GPTVectorStoreIndex,LLMPredictor, ServiceContext,SimpleDirectoryReader
from langchain.chat_models import ChatOpenAI

import uuid

from dotenv import load_dotenv
load_dotenv()
import os
#　設定
api_key=os.getenv('openai_api_key')
model = os.getenv('model_name')

def setup_data(path,data_path):
  # 設定
  #data_path = "data_use"
  #path = "./storage"
  # LLM Predictor (gpt-3.5-turbo) + service context
  llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key=api_key, temperature=0, model=model))
  service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
  # データの読み込み
  documents = SimpleDirectoryReader(data_path).load_data()
  # データから、ベクトルなどを作成
  index = GPTVectorStoreIndex.from_documents(
      documents, service_context=service_context
  )
  index.storage_context.persist(persist_dir= path)
  print("done")

def question_gpt(path,query):
  # 設定
  #path = "./storage"
  # LLM Predictor (gpt-3.5-turbo) + service context
  llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key=api_key, temperature=0, model_name=model))
  service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=2000)

  # rebuild storage context
  storage_context = StorageContext.from_defaults(persist_dir=path)
  # load index
  index = load_index_from_storage(storage_context, service_context=service_context)
  query_engine = index.as_query_engine(
      service_context=service_context,
  )
  print(path)
  print(query)
  response = query_engine.query("下記の質問に対して、詳細に日本語で回答してください\n\n###質問\n"+query)
  # print(response)
  return response
