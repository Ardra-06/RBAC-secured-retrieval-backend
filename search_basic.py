from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from data.documents import DOCUMENTS

# 1. Load the embedding model (downloads once, about 130 MB)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")
VECTOR_SIZE = model.get_sentence_embedding_dimension()

# 2. Create a database that lives in memory (no install needed)
client = QdrantClient(":memory:")

client.create_collection(
    collection_name="docs",
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)

# 3. Turn every document into a vector and store it
points = []
for i, doc in enumerate(DOCUMENTS):
    vector = model.encode(doc["text"]).tolist()
    points.append(
        models.PointStruct(
            id=i,
            vector=vector,
            payload=doc,  # keep text and access rules with the vector
        )
    )

client.upsert(collection_name="docs", points=points)
print(f"Stored {len(points)} documents.\n")

# 4. Search function (no security yet)
def search(question, k=3):
    q_vector = model.encode(question).tolist()
    result = client.query_points(
        collection_name="docs",
        query=q_vector,
        limit=k,
    )
    return result.points

# 5. Try it
question = "What is the CEO salary?"
print("Question:", question, "\n")

for hit in search(question):
    print(f"score={hit.score:.2f} | {hit.payload['doc_id']} | {hit.payload['text'][:60]}...")