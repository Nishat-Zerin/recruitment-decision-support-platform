"""
Mock candidate data for the demo.
In a production version, this would be populated by an actual CV-extraction
pipeline. For this portfolio prototype, extraction is simulated with
pre-structured data so the demo can focus on ranking, fairness safeguards,
and the agentic explanation feature.
"""

CANDIDATES = [
    {
        "id": "C12",
        "name": "Candidate 12",
        "title": "Data Analyst",
        "match_score": 92,
        "matched_skills": ["Python", "SQL", "Machine Learning", "Embeddings", "AWS", "Docker"],
        "missing_skills": [],
        "required_skills": ["Python", "SQL", "Machine Learning", "Embeddings", "AWS", "Docker"],
        "relevant_project": "Built a recommendation engine using Python and sentence embeddings, deployed on AWS.",
        "extraction_confidence": "high",
        "segment": "main",
        "phone": "+880 1XX-XXX-101",
        "email": "candidate12@email.com",
        "address": "Dhaka, Bangladesh",
        "applied_days_ago": 2,
        "tracker_stage": "hired",
    },
    {
        "id": "C07",
        "name": "Candidate 7",
        "title": "Senior Cloud Solutions Architect",
        "match_score": 77,
        "matched_skills": ["SQL", "Excel", "Communication", "Problem Solving", "Python"],
        "missing_skills": ["Cloud Deployment (AWS)"],
        "required_skills": ["SQL", "Excel", "Communication", "Problem Solving", "Python", "Cloud Deployment (AWS)"],
        "relevant_project": "Led a business analytics dashboard project; no direct cloud deployment experience listed.",
        "extraction_confidence": "high",
        "segment": "main",
        "phone": "+880 1XX-XXX-107",
        "email": "candidate7@email.com",
        "address": "Dhaka, Bangladesh",
        "applied_days_ago": 4,
        "tracker_stage": "shortlisted",
    },
    {
        "id": "C03",
        "name": "Candidate 3",
        "title": "Software Engineer",
        "match_score": 61,
        "matched_skills": ["Python", "R", "Data Analysis", "ML Basics"],
        "missing_skills": ["SQL", "Cloud Deployment (AWS)"],
        "required_skills": ["Python", "R", "Data Analysis", "ML Basics", "SQL", "Cloud Deployment (AWS)"],
        "relevant_project": "No directly relevant project found in extracted CV content.",
        "extraction_confidence": "high",
        "segment": "main",
        "phone": "+880 1XX-XXX-103",
        "email": "candidate3@email.com",
        "address": "Rajshahi, Bangladesh",
        "applied_days_ago": 7,
        "tracker_stage": None,
    },
    {
        "id": "C04",
        "name": "Candidate 4",
        "title": "Business Analyst",
        "match_score": 81,
        "matched_skills": ["Python", "SQL", "Excel", "Data Visualization"],
        "missing_skills": ["AWS"],
        "required_skills": ["Python", "SQL", "Excel", "Data Visualization", "AWS"],
        "relevant_project": "Built sales dashboards in Power BI and automated reporting in Python.",
        "extraction_confidence": "high",
        "segment": "main",
        "phone": "+880 1XX-XXX-104",
        "email": "candidate4@email.com",
        "address": "Chittagong, Bangladesh",
        "applied_days_ago": 3,
        "tracker_stage": "interview",
    },
    {
        "id": "C09",
        "name": "Candidate 9",
        "title": "Business Analyst",
        "match_score": 74,
        "matched_skills": ["Excel", "SQL", "Communication"],
        "missing_skills": ["Python", "Data Visualization"],
        "required_skills": ["Excel", "SQL", "Communication", "Python", "Data Visualization"],
        "relevant_project": "Requirements gathering and stakeholder workshops for an ERP rollout.",
        "extraction_confidence": "high",
        "segment": "main",
        "phone": "+880 1XX-XXX-109",
        "email": "candidate9@email.com",
        "address": "Dhaka, Bangladesh",
        "applied_days_ago": 5,
        "tracker_stage": "shortlisted",
    },
    # --- Needs Manual Review: low extraction confidence (non-standard CV formatting) ---
    {
        "id": "C15",
        "name": "Candidate 15",
        "title": "ML Engineer (CV had a multi-column layout)",
        "match_score": None,  # Not scored with full confidence - routed for manual review
        "matched_skills": ["Python", "Machine Learning"],
        "missing_skills": ["Unable to reliably extract remaining fields"],
        "required_skills": ["Python", "SQL", "Machine Learning", "Embeddings", "AWS", "Docker"],
        "relevant_project": "Extraction incomplete due to non-standard formatting - manual review recommended.",
        "extraction_confidence": "low",
        "segment": "review",
        "phone": "+880 1XX-XXX-115",
        "email": "candidate15@email.com",
        "address": "Dhaka, Bangladesh",
        "applied_days_ago": 1,
        "tracker_stage": None,
    },
    {
        "id": "C18",
        "name": "Candidate 18",
        "title": "Data Scientist (CV was a scanned image)",
        "match_score": None,
        "matched_skills": [],
        "missing_skills": ["Unable to reliably extract fields"],
        "required_skills": ["Python", "SQL", "Machine Learning", "Embeddings", "AWS", "Docker"],
        "relevant_project": "Extraction incomplete - scanned/image-based CV, low text confidence.",
        "extraction_confidence": "low",
        "segment": "review",
        "phone": "+880 1XX-XXX-118",
        "email": "candidate18@email.com",
        "address": "Khulna, Bangladesh",
        "applied_days_ago": 6,
        "tracker_stage": None,
    },
    {
        "id": "C21",
        "name": "Candidate 21",
        "title": "Software Engineer (tables/graphics-heavy CV)",
        "match_score": None,
        "matched_skills": ["SQL"],
        "missing_skills": ["Unable to reliably extract remaining fields"],
        "required_skills": ["Python", "SQL", "Machine Learning", "Embeddings", "AWS", "Docker"],
        "relevant_project": "Partial extraction only - infographic-style CV layout.",
        "extraction_confidence": "low",
        "segment": "review",
        "phone": "+880 1XX-XXX-121",
        "email": "candidate21@email.com",
        "address": "Sylhet, Bangladesh",
        "applied_days_ago": 8,
        "tracker_stage": None,
    },
    {
        "id": "C24",
        "name": "Candidate 24",
        "title": "AI Engineer (CV in unusual template)",
        "match_score": None,
        "matched_skills": ["Python", "AWS"],
        "missing_skills": ["Unable to reliably extract remaining fields"],
        "required_skills": ["Python", "SQL", "Machine Learning", "Embeddings", "AWS", "Docker"],
        "relevant_project": "Partial extraction - creative-template CV, medium-low text confidence.",
        "extraction_confidence": "low",
        "segment": "review",
        "phone": "+880 1XX-XXX-124",
        "email": "candidate24@email.com",
        "address": "Dhaka, Bangladesh",
        "applied_days_ago": 2,
        "tracker_stage": None,
    },
]

# The policy the agentic workflow retrieves and reasons against.
REVIEW_POLICY = (
    "Routing policy: A candidate is routed to 'Needs Manual Review' if extraction "
    "confidence is low (CV formatting prevented reliable field extraction), "
    "regardless of any partial score. This ensures no candidate is silently "
    "penalized for CV formatting rather than qualifications. For candidates with "
    "high extraction confidence, one or more missing required skills lowers the "
    "match score but does not by itself require manual review - it is surfaced "
    "to the recruiter as a gap to weigh."
)


def get_main_list():
    main = [c for c in CANDIDATES if c["segment"] == "main"]
    return sorted(main, key=lambda c: c["match_score"], reverse=True)


def get_review_list():
    return [c for c in CANDIDATES if c["segment"] == "review"]


def get_candidate_by_id(candidate_id):
    for c in CANDIDATES:
        if c["id"] == candidate_id:
            return c
    return None


def get_tracker_candidates():
    stages = {"shortlisted": [], "interview": [], "hired": []}
    for c in CANDIDATES:
        if c.get("tracker_stage") in stages:
            stages[c["tracker_stage"]].append(c)
    return stages
