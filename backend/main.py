# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import tempfile
import os
from datetime import datetime
import PyPDF2
import re

# Import the ML pipeline
from ml_pipeline import CareerClusterEngine

# ============================================
# INITIALIZE APP
# ============================================

app = FastAPI(
    title="Career Intelligence Platform",
    description="AI-powered career recommendations using clustering",
    version="2.0.0"
)

# ============================================
# CORS CONFIGURATION
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://career-intelligence-platform-1-xuy1.onrender.com",  # YOUR FRONTEND URL
        "https://career-intelligence-api-v2.onrender.com",
        "https://*.onrender.com"  # Allows all Render apps
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# INITIALIZE ML ENGINE
# ============================================

engine = CareerClusterEngine()

# ============================================
# PYDANTIC MODELS
# ============================================

class SkillAnalysisRequest(BaseModel):
    skills: List[str]
    experience_years: Optional[int] = 0

# ============================================
# PDF PARSING FUNCTIONS
# ============================================

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF content"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        text = ''
        with open(tmp_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
        
        os.unlink(tmp_path)
        return text
    except Exception as e:
        print(f"PDF parsing error: {e}")
        return ""

def extract_skills_from_text(text: str) -> List[str]:
    """Extract skills from text"""
    skill_keywords = {
        'python': ['python', 'pandas', 'numpy', 'django', 'flask', 'pytorch', 'tensorflow'],
        'sql': ['sql', 'postgresql', 'mysql', 'database', 'sqlite'],
        'java': ['java', 'spring', 'hibernate', 'maven', 'gradle'],
        'javascript': ['javascript', 'react', 'angular', 'vue', 'node', 'typescript'],
        'c++': ['c++', 'cpp', 'c plus plus'],
        'ml': ['machine learning', 'ml', 'ai', 'artificial intelligence'],
        'cloud': ['aws', 'azure', 'gcp', 'cloud'],
        'docker': ['docker', 'container', 'kubernetes'],
        'git': ['git', 'github', 'gitlab', 'version control'],
        'react': ['react', 'redux', 'react.js'],
        'nodejs': ['node.js', 'nodejs', 'express'],
        'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda'],
        'spark': ['spark', 'apache spark', 'pyspark'],
        'kafka': ['kafka', 'apache kafka'],
        'airflow': ['airflow', 'apache airflow'],
        'hadoop': ['hadoop', 'apache hadoop', 'hdfs'],
        'scala': ['scala', 'scala programming'],
        'postgres': ['postgresql', 'postgres'],
        'mongodb': ['mongodb', 'mongo', 'nosql'],
        'redis': ['redis', 'redis cache'],
        'elasticsearch': ['elasticsearch', 'elastic'],
        'kubernetes': ['kubernetes', 'k8s'],
        'terraform': ['terraform'],
        'jenkins': ['jenkins', 'ci/cd'],
        'ansible': ['ansible'],
        'linux': ['linux', 'unix'],
        'security': ['security', 'cybersecurity', 'encryption', 'audit'],
        'networking': ['network', 'networking', 'tcp/ip'],
        'agile': ['agile', 'scrum', 'kanban'],
        'leadership': ['leadership', 'team lead', 'management'],
        'communication': ['communication', 'presentation', 'public speaking'],
        'problem_solving': ['problem solving', 'analytical', 'critical thinking'],
        'c#': ['c#', 'csharp', '.net'],
        'ruby': ['ruby', 'ruby on rails'],
        'go': ['go', 'golang'],
        'rust': ['rust', 'rustlang'],
        'r': ['r programming', 'r language'],
        'angular': ['angular', 'angular.js'],
        'vue': ['vue', 'vue.js'],
        'django': ['django'],
        'flask': ['flask'],
        'spring': ['spring', 'spring boot'],
        'scikit-learn': ['scikit-learn', 'sklearn'],
        'tensorflow': ['tensorflow', 'tf'],
        'pytorch': ['pytorch'],
        'pandas': ['pandas'],
        'numpy': ['numpy']
    }
    
    text_lower = text.lower()
    found_skills = set()
    
    for skill, keywords in skill_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_skills.add(skill)
                break
    
    return list(found_skills)

def extract_skills_from_filename(filename: str) -> List[str]:
    """Extract skills from filename as fallback"""
    filename_lower = filename.lower()
    skill_keywords = {
        'python': ['python', 'data', 'analytics', 'ml'],
        'sql': ['sql', 'database'],
        'java': ['java', 'spring'],
        'javascript': ['javascript', 'react', 'frontend'],
        'aws': ['aws', 'cloud'],
        'docker': ['docker'],
        'ml': ['ml', 'machine', 'ai'],
        'spark': ['spark'],
        'kafka': ['kafka']
    }
    
    found_skills = []
    for skill, keywords in skill_keywords.items():
        for keyword in keywords:
            if keyword in filename_lower:
                found_skills.append(skill)
                break
    
    return found_skills

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {
        "message": "Career Intelligence Platform API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "/": "This help",
            "/api/health": "Health check",
            "/api/upload-cv": "Upload CV (POST)",
            "/api/analyze-skills": "Analyze skills (POST)",
            "/api/skills": "Get available skills (GET)",
            "/api/cluster-info/{cluster_id}": "Get cluster info (GET)",
            "/docs": "Swagger documentation"
        }
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_loaded": engine is not None,
        "trained": engine.trained if engine else False
    }

@app.post("/api/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """Upload and parse a CV"""
    try:
        print(f"📄 Received file: {file.filename}")
        print(f"📊 Content type: {file.content_type}")
        
        # Check file type
        allowed_types = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        if file.content_type not in allowed_types:
            raise HTTPException(400, f"Only PDF and DOCX files are allowed. Got: {file.content_type}")
        
        # Read file content
        content = await file.read()
        print(f"📊 File size: {len(content)} bytes")
        
        # Extract skills
        skills = []
        education = []
        experience = 0
        
        # Try to extract text from PDF
        if file.content_type == 'application/pdf':
            text = extract_text_from_pdf(content)
            if text:
                skills = extract_skills_from_text(text)
                print(f"📝 Extracted {len(skills)} skills from PDF content")
        
        # If no skills found, try filename
        if not skills:
            skills = extract_skills_from_filename(file.filename)
            print(f"📝 Extracted {len(skills)} skills from filename")
        
        # If still no skills, use default
        if not skills:
            skills = ['python', 'sql', 'docker']
            print(f"📝 Using default skills: {skills}")
        
        return {
            "status": "success",
            "data": {
                "skills": skills,
                "education": education or ["Not specified"],
                "experience": experience or 3,
                "skill_count": len(skills),
                "filename": file.filename
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"❌ Error in upload_cv: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/analyze-skills")
async def analyze_skills(request: SkillAnalysisRequest):
    """Analyze skills and provide comprehensive career recommendations"""
    try:
        print(f"🧠 Analyzing skills: {request.skills}")
        print(f"📊 Experience: {request.experience_years} years")
        
        # Get FULL recommendations with all rich data
        recommendations = engine.analyze_candidate(request.skills)
        
        print(f"✅ Analysis complete: {recommendations['cluster_name']}")
        print(f"📊 Match: {recommendations['match_percentage']}%")
        print(f"📊 Keys in recommendations: {list(recommendations.keys())}")
        print(f"📊 Has skill_resources? {'skill_resources' in recommendations}")
        
        if 'skill_resources' in recommendations:
            missing = recommendations['skill_resources'].get('missing_skills', {})
            print(f"📊 Missing skills with resources: {list(missing.keys())}")
        
        # Return EVERYTHING - don't filter anything!
        return {
            "status": "success",
            "recommendations": recommendations
        }
        
    except Exception as e:
        print(f"❌ Error in analyze_skills: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/batch-analysis")
async def batch_analysis(profiles: List[SkillAnalysisRequest]):
    """Analyze multiple candidates for clustering"""
    try:
        print(f"📊 Batch analysis: {len(profiles)} candidates")
        
        results = []
        for profile in profiles:
            recommendations = engine.analyze_candidate(profile.skills)
            results.append({
                "skills": profile.skills,
                "recommendations": recommendations
            })
        
        return {
            "status": "success",
            "total_candidates": len(profiles),
            "results": results
        }
        
    except Exception as e:
        print(f"❌ Error in batch_analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/skills")
async def get_available_skills():
    """Get all available skill categories"""
    return {
        "status": "success",
        "total_skills": len(engine.skill_categories),
        "skills": engine.skill_categories
    }

@app.get("/api/clusters")
async def get_all_clusters():
    """Get information about all career clusters"""
    try:
        clusters = []
        for cluster_id, cluster_info in engine.career_clusters.items():
            clusters.append({
                "id": cluster_id,
                "name": cluster_info['name'],
                "roles": cluster_info['roles'],
                "keywords": cluster_info['keywords'],
                "salary_range": cluster_info.get('salary_range', 'Varies'),
                "growth_potential": cluster_info.get('growth_potential', 'High'),
                "description": cluster_info.get('description', ''),
                "industry": cluster_info.get('industry', ['Tech']),
                "remote_opportunities": cluster_info.get('remote_opportunities', 'High')
            })
        
        return {
            "status": "success",
            "total_clusters": len(clusters),
            "clusters": clusters
        }
        
    except Exception as e:
        print(f"❌ Error in get_all_clusters: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cluster-info/{cluster_id}")
async def get_cluster_info(cluster_id: int):
    """Get detailed information about a specific cluster"""
    try:
        if cluster_id not in engine.career_clusters:
            raise HTTPException(404, f"Cluster {cluster_id} not found")
        
        cluster_info = engine.career_clusters[cluster_id]
        
        return {
            "status": "success",
            "cluster": {
                "id": cluster_id,
                "name": cluster_info['name'],
                "roles": cluster_info['roles'],
                "keywords": cluster_info['keywords'],
                "learning_path": cluster_info['learning_path'],
                "salary_range": cluster_info.get('salary_range', 'Varies'),
                "growth_potential": cluster_info.get('growth_potential', 'High'),
                "entry_level_skills": cluster_info.get('entry_level_skills', []),
                "description": cluster_info.get('description', ''),
                "industry": cluster_info.get('industry', ['Tech']),
                "remote_opportunities": cluster_info.get('remote_opportunities', 'High'),
                "project_idea": cluster_info.get('project_idea', ''),
                "why_choose": cluster_info.get('why_choose', '')
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"❌ Error in get_cluster_info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/train")
async def train_model():
    """Train the clustering model (for development/testing)"""
    try:
        print("🧠 Training model with sample data...")
        
        from ml_pipeline import generate_sample_data
        sample_data = generate_sample_data(200)
        
        labels = engine.train_clusters(sample_data, method='kmeans', n_clusters=10)
        engine.save_model()
        
        metrics = engine.get_cluster_quality_metrics() if hasattr(engine, 'get_cluster_quality_metrics') else {}
        
        return {
            "status": "success",
            "message": "Model trained successfully",
            "clusters": len(set(labels)),
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error in train_model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    print("="*60)
    print("🚀 Career Intelligence Platform API")
    print("="*60)
    print(f"📊 Skills loaded: {len(engine.skill_categories)}")
    print(f"📊 Career clusters: {len(engine.career_clusters)}")
    print(f"📊 Engine trained: {engine.trained}")
    print("="*60)
    print("🌐 Starting server at http://localhost:8000")
    print("📚 API Docs at http://localhost:8000/docs")
    print("="*60)
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Important: Turn off reload in production
    )
    
