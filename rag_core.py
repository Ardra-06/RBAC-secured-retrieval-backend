from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from data.documents import DOCUMENTS

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
VECTOR_SIZE = model.get_embedding_dimension()

client = QdrantClient(":memory:")
client.create_collection(
    collection_name="docs",
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
    ),
)

points = []
for i, doc in enumerate(DOCUMENTS):
    points.append(
        models.PointStruct(
            id=i,
            vector=model.encode(doc["text"]).tolist(),
            payload=doc,
        )
    )
client.upsert(collection_name="docs", points=points)


def build_filter(user):
    return models.Filter(
        must=[
            models.FieldCondition(
                key="allowed_roles",
                match=models.MatchAny(any=user["roles"]),
            ),
            models.FieldCondition(
                key="clearance",
                range=models.Range(lte=user["clearance"]),
            ),
        ]
    )


def search(question, user, k=3):
    q_vector = model.encode(question).tolist()
    result = client.query_points(
        collection_name="docs",
        query=q_vector,
        query_filter=build_filter(user),
        limit=k,
    )
    return result.points