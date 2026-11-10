# Each document has text plus access rules.
# allowed_roles = who can read it
# clearance     = minimum level needed (1 = low, 3 = high)

DOCUMENTS = [
    {
        "doc_id": "pol-001",
        "dept": "general",
        "text": "Office hours are 9 AM to 6 PM, Monday to Friday. "
                "Employees get 24 days of paid leave every year.",
        "allowed_roles": ["employee", "hr", "finance", "engineer", "admin"],
        "clearance": 1,
    },
    {
        "doc_id": "hr-001",
        "dept": "hr",
        "text": "The CEO salary is 5 crore rupees per year. "
                "The average engineer salary is 18 lakh rupees per year.",
        "allowed_roles": ["hr", "admin"],
        "clearance": 3,
    },
    {
        "doc_id": "hr-002",
        "dept": "hr",
        "text": "Performance reviews happen every March and September. "
                "Managers must submit ratings within 10 days.",
        "allowed_roles": ["hr", "admin"],
        "clearance": 2,
    },
    {
        "doc_id": "fin-001",
        "dept": "finance",
        "text": "Q3 revenue was 42 crore rupees. "
                "The company plans to cut marketing budget by 15 percent.",
        "allowed_roles": ["finance", "admin"],
        "clearance": 3,
    },
    {
        "doc_id": "eng-001",
        "dept": "engineering",
        "text": "Production servers are hosted on AWS in the Mumbai region. "
                "Deployments happen every Thursday at 4 PM.",
        "allowed_roles": ["engineer", "admin"],
        "clearance": 2,
    },
    {
        "doc_id": "eng-002",
        "dept": "engineering",
        "text": "Our code review rule: every pull request needs two approvals "
                "before it can be merged into the main branch.",
        "allowed_roles": ["engineer", "employee", "admin"],
        "clearance": 1,
    },
]