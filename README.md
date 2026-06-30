# 🎯 AI Career Intelligence Platform

An AI-powered full-stack web application that analyzes CVs, extracts skills, and provides personalized career recommendations using machine learning.

## 🚀 Features

- 📄 **CV Parsing** - Extract skills from PDF documents
- 🧠 **ML Clustering** - K-Means, Hierarchical, and DBSCAN clustering
- 🎯 **Career Clusters** - 10 career categories with detailed insights
- 📚 **Learning Resources** - Curated courses, certifications, and project ideas
- 🔗 **Clickable Links** - Direct access to learning materials
- 💡 **Project Ideas** - Portfolio project suggestions
- 📊 **Alternative Paths** - Other career options based on your skills

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **ML**: scikit-learn, K-Means clustering
- **Deployment**: Render

## 📊 Career Clusters

1. Data Engineering
2. Machine Learning Engineering
3. Full Stack Development
4. Cloud Architecture & DevOps
5. Backend Engineering
6. Mobile Development
7. Data Science & Analytics
8. Security Engineering
9. Product Management
10. Game Development

## 🚀 Deployment

### Backend (Render)

1. Push your code to GitHub
2. On Render, click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Render)

1. On Render, click "New +" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
4. Add environment variable:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://your-backend-url.onrender.com`

## 🔧 Environment Variables

### Backend (.env in backend folder)

```env
ENVIRONMENT=production
