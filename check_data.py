from data.documents import DOCUMENTS

for d in DOCUMENTS:
    print(d["doc_id"], "|", d["dept"], "| roles:", d["allowed_roles"], "| level:", d["clearance"])