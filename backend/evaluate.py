import numpy as np
from backend.embedding import chunk_text, embed
from backend.preprocessing import extract_skills_and_canonicalize, clean_text

def compute_skill_overlap_score(jd_text: str, resume_text: str) -> float:
    jd_skills = extract_skills_and_canonicalize(jd_text)
    res_skills = extract_skills_and_canonicalize(resume_text)
    
    if not jd_skills:
        return 0.0
        
    matched_skills = jd_skills.intersection(res_skills)
    # Generous partial weighting for keyword recall
    overlap_ratio = len(matched_skills) / max(len(jd_skills), 1)
    return round(overlap_ratio * 100, 1)

def evaluate_resume(jd_text: str, resume_text: str) -> float:
    jd_clean = clean_text(jd_text)
    res_clean = clean_text(resume_text)

    if not res_clean or not jd_clean:
        return 0.0

    # 1. Skill Overlap Score
    skill_score = compute_skill_overlap_score(jd_text, resume_text)

    # 2. Semantic Embedding Similarity
    jd_chunks = chunk_text(jd_clean, max_words=120)
    res_chunks = chunk_text(res_clean, max_words=100)

    jd_vecs = embed(jd_chunks, is_query=False)
    res_vecs = embed(res_chunks, is_query=False)

    if len(jd_vecs) == 0 or len(res_vecs) == 0:
        semantic_score = 0.0
    else:
        sim_matrix = jd_vecs @ res_vecs.T
        # Scale raw cosine similarity (typically 0.3-0.7) into percentage space (0-100)
        raw_sim = float(sim_matrix.max(axis=1).mean())
        semantic_score = round(min(max((raw_sim + 0.15) * 100, 0.0), 100.0), 1)

    # 3. Balanced Hybrid Blend (40% Hard Skills + 60% Semantic Deep Context)
    combined = (0.40 * skill_score) + (0.60 * semantic_score)
    
    # Calibrate range: Boost good matches into professional recruiter ranges (70% - 95%)
    if combined > 35:
        final_score = 45 + (combined * 0.52)
    else:
        final_score = combined * 1.2

    return round(min(max(final_score, 15.0), 96.5), 1)