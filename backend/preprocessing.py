import re

# Comprehensive synonym mapping for Data Engineering and Data Analytics
SKILL_SYNONYMS = {
    # Programming & Languages
    "py": "python",
    "python3": "python",
    "sql": "sql",
    
    # Data Engineering Stack
    "spark": "apache spark",
    "pyspark": "apache spark",
    "airflow": "apache airlfow",
    "kafka": "apache kafka",
    "aws": "aws",
    "amazon web services": "aws",
    "etl": "etl/elt",
    "elt": "etl/elt",
    "snowflake": "snowflake",
    "dbt": "dbt",
    "databricks": "databricks",
    "terraform": "terraform",
    
    # Data Analyst Stack
    "pbi": "power bi",
    "powerbi": "power bi",
    "tableau": "tableau",
    "excel": "microsoft excel",
    "pivot tables": "microsoft excel",
    "a/b testing": "a/b testing",
    "ab testing": "a/b testing",
    "pandas": "python",
    "numpy": "python",
    "statistics": "statistical analysis"
}

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[•‣▪◦●·∙]", " ", text)
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9+#./\-,()&@:\n ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills_and_canonicalize(text: str) -> set:
    cleaned = clean_text(text)
    words = set(cleaned.split())
    
    extracted = set()
    for word in words:
        canonical = SKILL_SYNONYMS.get(word, word)
        extracted.add(canonical)
        
    for synonym, canonical in SKILL_SYNONYMS.items():
        if " " in synonym and synonym in cleaned:
            extracted.add(canonical)
            
    return extracted