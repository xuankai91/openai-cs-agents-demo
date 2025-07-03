from openai import OpenAI
import os
import json

from dotenv import load_dotenv
load_dotenv()
assert 'OPENAI_API_KEY' in os.environ, "ERROR: set up your OPENAI_API_KEY"

## settings
EMBED = "text-embedding-3-small"
EMBEDDIM = 1536 # based on the embedding model. see https://milvus.io/docs/openai.md

# create embedding function
openai_client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
def encode_doc(doc: str) -> list:
    return openai_client.embeddings.create(model=EMBED,input=doc,encoding_format="float").data[0].embedding

# create vectorDB (use in-memory vdb for now)
from pymilvus import MilvusClient
milvus_client = MilvusClient("../milvus.db")

collection_name = "faq"
# if milvus_client.has_collection(collection_name=collection_name):
#     milvus_client.drop_collection(collection_name=collection_name)

if not milvus_client.has_collection(collection_name=collection_name)
    # create collection 
    milvus_client.create_collection(
        collection_name=collection_name,
        dimension=EMBEDDIM,
        metric_type="COSINE",  # cosine distance
        consistency_level="Strong",  # See https://milvus.io/docs/consistency.md#Consistency-Level for supported values.
    )
    
    # load faq data
    with open('./faqs.json','r') as f:
        faqs = json.load(f)
    
    # embed data (note that this will consume another round of your openAI credits)
    data = []
    for k,v in faqs.items():
        data.append({'id':int(k),
                 'vector':encode_doc(v['q']),
                 'question':v['q'],
                 'answer':v['a']})
    
    # insert into database
    milvus_client.insert(collection_name=collection_name, data=data)
    print(collection_name, 'collection created')
else:
    print(collection_name, 'collection already exists')
