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
    """Turn a user into a rule the database understands."""
    return models.Filter(
        must=[
            # Rule 1: the user must have one of the allowed roles
            models.FieldCondition(
                key="allowed_roles",
                match=models.MatchAny(any=user["roles"]),
            ),
            # Rule 2: the user's clearance must be high enough
            # (document clearance <= user clearance)
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
        query_filter=build_filter(user),  # the filter runs INSIDE the search
        limit=k,
    )
    return result.points


# Three sample users
USERS = {
    "employee": {"roles": ["employee"], "clearance": 1},
    "hr_person": {"roles": ["hr"], "clearance": 3},
    "engineer": {"roles": ["engineer", "employee"], "clearance": 2},
}

question = "What is the CEO salary?"
print("Question:", question)

for name, user in USERS.items():
    print(f"\n--- Asked by: {name} ---")
    hits = search(question, user)
    if not hits:
        print("(no results)")
    for hit in hits:
        print(f"score={hit.score:.2f} | {hit.payload['doc_id']} | {hit.payload['text'][:50]}...")