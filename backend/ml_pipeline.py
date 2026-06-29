# backend/ml_pipeline.py
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from typing import List, Dict, Tuple, Optional
import json
from datetime import datetime

# ============================================
# SKILL RESOURCE DATABASE - COMPLETE WITH ALL DATA
# ============================================

SKILL_RESOURCES = {
    # Programming Languages
    'python': {
        'description': 'High-level programming language for data science, ML, and web development. Most versatile language in tech.',
        'difficulty': 'Beginner',
        'learning_time': '2-3 months',
        'why_learn': 'Python is the #1 language for AI, data science, and automation. Used by 80% of tech companies.',
        'resources': [
            {'name': 'Python.org Official Tutorial', 'url': 'https://docs.python.org/3/tutorial/'},
            {'name': 'Codecademy Python Course', 'url': 'https://www.codecademy.com/learn/learn-python-3'},
            {'name': 'Real Python Tutorials', 'url': 'https://realpython.com/'},
            {'name': 'Python for Data Science (Coursera)', 'url': 'https://www.coursera.org/learn/python-for-applied-data-science-ai'}
        ],
        'certification': 'PCAP - Certified Associate in Python Programming',
        'projects': ['Build a data analysis pipeline', 'Create a web scraper', 'Develop a REST API'],
        'job_demand': 'Very High - 500K+ job postings'
    },
    'sql': {
        'description': 'Structured Query Language for managing and analyzing relational databases. Essential for any data role.',
        'difficulty': 'Beginner',
        'learning_time': '1-2 months',
        'why_learn': 'SQL is the language of data. Every company uses databases, making SQL skills universally valuable.',
        'resources': [
            {'name': 'SQL Tutorial (W3Schools)', 'url': 'https://www.w3schools.com/sql/'},
            {'name': 'SQL for Data Analysis (Mode)', 'url': 'https://mode.com/sql-tutorial/'},
            {'name': 'Coursera SQL Course', 'url': 'https://www.coursera.org/learn/sql-for-data-science'},
            {'name': 'LeetCode SQL Problems', 'url': 'https://leetcode.com/problemset/database/'}
        ],
        'certification': 'Microsoft SQL Certification',
        'projects': ['Design a database schema', 'Write complex analytics queries', 'Build a data warehouse'],
        'job_demand': 'Very High - 600K+ job postings'
    },
    'spark': {
        'description': 'Apache Spark is a unified analytics engine for large-scale data processing. Handles billions of records.',
        'difficulty': 'Advanced',
        'learning_time': '3-5 months',
        'why_learn': 'Spark is the industry standard for big data. Companies processing terabytes of data need Spark experts.',
        'resources': [
            {'name': 'Apache Spark Official Docs', 'url': 'https://spark.apache.org/docs/latest/'},
            {'name': 'Spark Programming (Databricks)', 'url': 'https://www.databricks.com/learn/training'},
            {'name': 'Spark Course (Coursera)', 'url': 'https://www.coursera.org/learn/spark-scala'},
            {'name': 'Spark: The Definitive Guide (Book)', 'url': 'https://www.oreilly.com/library/view/spark-the-definitive/9781491912201/'}
        ],
        'certification': 'Apache Spark Developer',
        'projects': ['Build a real-time data pipeline', 'Process streaming data', 'Create a data lake solution'],
        'job_demand': 'High - 100K+ job postings'
    },
    'kafka': {
        'description': 'Apache Kafka is a distributed event streaming platform for real-time data pipelines and streaming applications.',
        'difficulty': 'Advanced',
        'learning_time': '3-5 months',
        'why_learn': 'Kafka powers real-time data at companies like Netflix, Uber, and LinkedIn. Critical for modern data architecture.',
        'resources': [
            {'name': 'Apache Kafka Official Docs', 'url': 'https://kafka.apache.org/documentation/'},
            {'name': 'Kafka Course (Udemy)', 'url': 'https://www.udemy.com/course/apache-kafka/'},
            {'name': 'Confluent Kafka Tutorials', 'url': 'https://developer.confluent.io/learn-kafka/'},
            {'name': 'Kafka: The Definitive Guide (Book)', 'url': 'https://www.confluent.io/resources/kafka-the-definitive-guide/'}
        ],
        'certification': 'Confluent Certified Developer',
        'projects': ['Build a real-time streaming pipeline', 'Create an event-driven microservice', 'Implement CDC with Kafka'],
        'job_demand': 'High - 80K+ job postings'
    },
    'airflow': {
        'description': 'Apache Airflow is a platform for programmatically authoring, scheduling, and monitoring workflows.',
        'difficulty': 'Intermediate',
        'learning_time': '2-3 months',
        'why_learn': 'Airflow is the standard for data orchestration. Companies use it to automate complex data pipelines.',
        'resources': [
            {'name': 'Apache Airflow Official Docs', 'url': 'https://airflow.apache.org/docs/'},
            {'name': 'Astronomer Airflow Tutorials', 'url': 'https://www.astronomer.io/docs/learn/'},
            {'name': 'Airflow Course (Udemy)', 'url': 'https://www.udemy.com/course/the-complete-hands-on-introduction-to-apache-airflow/'},
            {'name': 'Data Pipelines with Airflow (Book)', 'url': 'https://www.manning.com/books/data-pipelines-with-apache-airflow'}
        ],
        'certification': 'Apache Airflow Developer',
        'projects': ['Build a DAG for ETL pipeline', 'Schedule data processing workflows', 'Create monitoring alerts'],
        'job_demand': 'High - 60K+ job postings'
    },
    'java': {
        'description': 'Object-oriented programming language for enterprise applications and Android development.',
        'difficulty': 'Intermediate',
        'learning_time': '3-4 months',
        'why_learn': 'Java powers 3 billion devices. Enterprise companies heavily rely on Java for backend systems.',
        'resources': [
            {'name': 'Oracle Java Tutorials', 'url': 'https://docs.oracle.com/javase/tutorial/'},
            {'name': 'Java Programming Masterclass (Udemy)', 'url': 'https://www.udemy.com/course/java-the-complete-java-developer-course/'},
            {'name': 'Codecademy Java', 'url': 'https://www.codecademy.com/learn/learn-java'},
            {'name': 'Hyperskill (JetBrains)', 'url': 'https://hyperskill.org/learn-java'}
        ],
        'certification': 'Oracle Certified Professional Java Programmer',
        'projects': ['Build a REST API', 'Create a microservice', 'Develop an Android app'],
        'job_demand': 'Very High - 400K+ job postings'
    },
    'javascript': {
        'description': 'Versatile language for web development, both frontend and backend. The language of the web.',
        'difficulty': 'Beginner',
        'learning_time': '2-3 months',
        'why_learn': 'JavaScript is everywhere - 98% of websites use it. Essential for any web development career.',
        'resources': [
            {'name': 'MDN JavaScript Guide', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide'},
            {'name': 'JavaScript.info', 'url': 'https://javascript.info/'},
            {'name': 'FreeCodeCamp JavaScript', 'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/'},
            {'name': 'The Odin Project', 'url': 'https://www.theodinproject.com/'}
        ],
        'certification': 'OpenJS Foundation JavaScript Developer',
        'projects': ['Build a web app', 'Create an interactive dashboard', 'Develop a browser extension'],
        'job_demand': 'Very High - 600K+ job postings'
    },
    'react': {
        'description': 'Popular frontend library for building interactive user interfaces. The most used web framework.',
        'difficulty': 'Intermediate',
        'learning_time': '2-3 months',
        'why_learn': 'React is the most in-demand frontend framework. Used by Facebook, Netflix, and countless others.',
        'resources': [
            {'name': 'React Official Docs', 'url': 'https://react.dev/learn'},
            {'name': 'FreeCodeCamp React', 'url': 'https://www.freecodecamp.org/learn/front-end-development-libraries/react'},
            {'name': 'React Redux Course (Udemy)', 'url': 'https://www.udemy.com/course/react-redux/'},
            {'name': 'Scrimba React Course', 'url': 'https://scrimba.com/learn/learnreact'}
        ],
        'certification': 'Meta Frontend Developer Certificate',
        'projects': ['Build a SaaS dashboard', 'Create an e-commerce store', 'Develop a social media app'],
        'job_demand': 'Very High - 300K+ job postings'
    },
    'docker': {
        'description': 'Containerization platform for application deployment and isolation. Industry standard for DevOps.',
        'difficulty': 'Intermediate',
        'learning_time': '1-2 months',
        'why_learn': 'Docker is essential for modern development. 80% of companies use containers in production.',
        'resources': [
            {'name': 'Docker Official Docs', 'url': 'https://docs.docker.com/get-started/'},
            {'name': 'Docker Course (Udemy)', 'url': 'https://www.udemy.com/course/docker-compose-in-depth/'},
            {'name': 'Docker Curriculum', 'url': 'https://docker-curriculum.com/'},
            {'name': 'Docker Mastery (Udemy)', 'url': 'https://www.udemy.com/course/docker-mastery/'}
        ],
        'certification': 'Docker Certified Associate',
        'projects': ['Containerize an application', 'Create a multi-container setup', 'Build a CI/CD pipeline with Docker'],
        'job_demand': 'Very High - 200K+ job postings'
    },
    'aws': {
        'description': 'Amazon Web Services - Leading cloud computing platform with 200+ services.',
        'difficulty': 'Intermediate',
        'learning_time': '3-6 months',
        'why_learn': 'AWS is the #1 cloud provider. Cloud skills are essential for modern infrastructure roles.',
        'resources': [
            {'name': 'AWS Documentation', 'url': 'https://docs.aws.amazon.com/'},
            {'name': 'AWS Training & Certification', 'url': 'https://aws.amazon.com/training/'},
            {'name': 'AWS Solutions Architect Course (Udemy)', 'url': 'https://www.udemy.com/course/aws-certified-solutions-architect-associate/'},
            {'name': 'Qwiklabs AWS', 'url': 'https://www.qwiklabs.com/quests/15'}
        ],
        'certification': 'AWS Certified Solutions Architect',
        'projects': ['Deploy a web app on EC2', 'Build a serverless app', 'Create a data pipeline with AWS services'],
        'job_demand': 'Very High - 400K+ job postings'
    }
}

# ============================================
# MAIN CLUSTER ENGINE
# ============================================

class CareerClusterEngine:
    def __init__(self):
        # Expanded skill categories
        self.skill_categories = [
            'python', 'sql', 'spark', 'kafka', 'airflow', 'hadoop', 'scala', 'java',
            'javascript', 'react', 'nodejs', 'mongodb', 'docker', 'typescript',
            'aws', 'kubernetes', 'terraform', 'jenkins', 'gcp', 'azure',
            'ml', 'dl', 'nlp', 'computer_vision', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'postgres', 'mysql', 'redis', 'elasticsearch',
            'c++', 'c#', 'ruby', 'go', 'rust', 'r',
            'angular', 'vue', 'django', 'flask', 'spring',
            'git', 'ci/cd', 'linux',
            'agile', 'scrum', 'leadership', 'communication', 'problem_solving'
        ]
        
        # 10 Career Clusters
        self.career_clusters = {
            0: {
                'name': 'Data Engineering',
                'keywords': ['python', 'sql', 'spark', 'kafka', 'airflow', 'hadoop', 'scala', 'java'],
                'roles': ['Data Engineer', 'ETL Developer', 'Big Data Engineer', 'Data Architect'],
                'learning_path': [
                    'Advanced Python', 
                    'SQL Optimization & Performance Tuning',
                    'Apache Spark (PySpark)',
                    'Kafka Streaming',
                    'Apache Airflow',
                    'Data Warehouse Design',
                    'Cloud Data Platforms (AWS/Azure)'
                ],
                'salary_range': '$90K - $160K',
                'growth_potential': 'High (30% growth over 5 years)',
                'entry_level_skills': ['python', 'sql', 'git'],
                'description': 'Build and maintain data pipelines and infrastructure that process billions of records daily.',
                'industry': ['Tech', 'Finance', 'Healthcare', 'E-commerce'],
                'remote_opportunities': 'Very High - 80% remote roles available',
                'project_idea': 'Build a real-time data pipeline that processes streaming data from multiple sources into a data warehouse',
                'why_choose': 'Data Engineering is the backbone of modern data infrastructure. Every company needs data engineers.'
            },
            1: {
                'name': 'Machine Learning Engineering',
                'keywords': ['python', 'ml', 'dl', 'nlp', 'computer_vision', 'tensorflow', 'pytorch', 'scikit-learn'],
                'roles': ['ML Engineer', 'Data Scientist', 'AI Researcher', 'Computer Vision Engineer'],
                'learning_path': [
                    'ML Fundamentals',
                    'Deep Learning (PyTorch/TensorFlow)',
                    'NLP with Transformers',
                    'MLOps & Model Deployment',
                    'Computer Vision',
                    'Reinforcement Learning',
                    'ML System Design'
                ],
                'salary_range': '$100K - $180K',
                'growth_potential': 'Very High (40% growth over 5 years)',
                'entry_level_skills': ['python', 'ml', 'statistics', 'git'],
                'description': 'Design and deploy machine learning models at scale to solve complex business problems.',
                'industry': ['Tech', 'Finance', 'Healthcare', 'Autonomous Vehicles'],
                'remote_opportunities': 'High - 70% remote roles available',
                'project_idea': 'Build a production-ready ML model with API deployment, monitoring, and retraining pipelines',
                'why_choose': 'ML Engineering is the fastest growing tech career. AI is transforming every industry.'
            },
            2: {
                'name': 'Full Stack Development',
                'keywords': ['javascript', 'react', 'nodejs', 'mongodb', 'docker', 'typescript', 'vue', 'angular'],
                'roles': ['Full Stack Developer', 'Frontend Lead', 'Tech Lead', 'Software Architect'],
                'learning_path': [
                    'Advanced React & Next.js',
                    'Node.js Microservices',
                    'System Design',
                    'DevOps & Docker',
                    'GraphQL',
                    'Cloud Deployment',
                    'Testing & CI/CD'
                ],
                'salary_range': '$85K - $150K',
                'growth_potential': 'High (25% growth over 5 years)',
                'entry_level_skills': ['javascript', 'html', 'css', 'git'],
                'description': 'Build end-to-end web applications and services that power modern businesses.',
                'industry': ['Tech', 'E-commerce', 'Startups', 'Fintech'],
                'remote_opportunities': 'Very High - 85% remote roles available',
                'project_idea': 'Build a full-stack SaaS product with authentication, payments, and real-time features',
                'why_choose': 'Full Stack developers are the most versatile and in-demand software engineers.'
            },
            3: {
                'name': 'Cloud Architecture & DevOps',
                'keywords': ['aws', 'docker', 'kubernetes', 'terraform', 'jenkins', 'gcp', 'azure', 'ansible'],
                'roles': ['Cloud Architect', 'DevOps Engineer', 'Site Reliability Engineer', 'Platform Engineer'],
                'learning_path': [
                    'AWS/Azure/GCP Certification',
                    'Kubernetes Mastery',
                    'CI/CD Pipelines (Jenkins/GitHub Actions)',
                    'Infrastructure as Code (Terraform)',
                    'Monitoring (Prometheus/Grafana)',
                    'Security Best Practices',
                    'Cloud Cost Optimization'
                ],
                'salary_range': '$95K - $170K',
                'growth_potential': 'Very High (35% growth over 5 years)',
                'entry_level_skills': ['aws', 'docker', 'git', 'linux'],
                'description': 'Design and manage cloud infrastructure and deployment pipelines for modern applications.',
                'industry': ['Tech', 'Finance', 'Healthcare', 'Government'],
                'remote_opportunities': 'High - 75% remote roles available',
                'project_idea': 'Design a multi-cloud infrastructure with Kubernetes, CI/CD, monitoring, and auto-scaling',
                'why_choose': 'Cloud skills are the most sought-after in tech. Every company is moving to the cloud.'
            },
            4: {
                'name': 'Backend Engineering',
                'keywords': ['java', 'spring', 'postgres', 'redis', 'microservices', 'go', 'c#', 'sql'],
                'roles': ['Backend Developer', 'API Engineer', 'Systems Architect', 'Microservices Developer'],
                'learning_path': [
                    'Spring Boot / .NET Core',
                    'Microservices Architecture',
                    'Database Design & Optimization',
                    'API Security (OAuth/JWT)',
                    'Performance Optimization',
                    'Event-Driven Architecture',
                    'System Integration'
                ],
                'salary_range': '$88K - $155K',
                'growth_potential': 'High (28% growth over 5 years)',
                'entry_level_skills': ['java', 'sql', 'git', 'spring'],
                'description': 'Build robust backend systems and APIs that scale to millions of users.',
                'industry': ['Tech', 'Finance', 'Healthcare', 'E-commerce'],
                'remote_opportunities': 'High - 70% remote roles available',
                'project_idea': 'Build a scalable microservices architecture with API gateway, service discovery, and distributed logging',
                'why_choose': 'Backend engineers are the foundation of all web applications. High demand, high pay.'
            },
            5: {
                'name': 'Mobile Development',
                'keywords': ['javascript', 'react', 'android', 'ios', 'swift', 'kotlin', 'react-native', 'flutter'],
                'roles': ['Mobile Developer', 'React Native Developer', 'iOS/Android Engineer', 'Mobile Architect'],
                'learning_path': [
                    'React Native / Flutter',
                    'Native iOS (Swift)',
                    'Native Android (Kotlin)',
                    'Mobile App Architecture',
                    'App Store Deployment',
                    'Mobile Testing',
                    'Performance Optimization'
                ],
                'salary_range': '$82K - $145K',
                'growth_potential': 'High (22% growth over 5 years)',
                'entry_level_skills': ['javascript', 'git', 'react'],
                'description': 'Build cross-platform and native mobile applications that millions of people use.',
                'industry': ['Tech', 'Startups', 'Fintech', 'Healthcare'],
                'remote_opportunities': 'High - 65% remote roles available',
                'project_idea': 'Build a cross-platform mobile app with offline support, push notifications, and cloud sync',
                'why_choose': 'Mobile is the future. 6 billion smartphone users worldwide need apps.'
            },
            6: {
                'name': 'Data Science & Analytics',
                'keywords': ['python', 'sql', 'r', 'pandas', 'numpy', 'ml', 'statistics', 'visualization'],
                'roles': ['Data Scientist', 'Data Analyst', 'Business Intelligence Analyst', 'Analytics Engineer'],
                'learning_path': [
                    'Advanced Statistics',
                    'Data Visualization (Tableau/PowerBI)',
                    'SQL for Analytics',
                    'Python for Data Science',
                    'Business Intelligence',
                    'A/B Testing',
                    'Data Storytelling'
                ],
                'salary_range': '$80K - $140K',
                'growth_potential': 'High (28% growth over 5 years)',
                'entry_level_skills': ['python', 'sql', 'statistics', 'excel'],
                'description': 'Extract insights and drive decisions from data. Turn raw data into business value.',
                'industry': ['Tech', 'Finance', 'Healthcare', 'Marketing'],
                'remote_opportunities': 'High - 70% remote roles available',
                'project_idea': 'Build a complete BI dashboard with predictive analytics and automated reporting',
                'why_choose': 'Data is the new oil. Companies desperately need people who can make sense of data.'
            },
            7: {
                'name': 'Security Engineering',
                'keywords': ['aws', 'python', 'linux', 'network', 'security', 'encryption', 'audit', 'compliance'],
                'roles': ['Security Engineer', 'Penetration Tester', 'Security Analyst', 'Cloud Security Engineer'],
                'learning_path': [
                    'Security Fundamentals',
                    'Cloud Security (AWS/Azure)',
                    'Penetration Testing',
                    'Security Compliance (SOC2, HIPAA)',
                    'Network Security',
                    'DevSecOps',
                    'Incident Response'
                ],
                'salary_range': '$95K - $165K',
                'growth_potential': 'Very High (35% growth over 5 years)',
                'entry_level_skills': ['python', 'linux', 'networking', 'git'],
                'description': 'Protect systems and data from security threats. The most critical role in tech.',
                'industry': ['Tech', 'Finance', 'Healthcare', 'Government'],
                'remote_opportunities': 'High - 70% remote roles available',
                'project_idea': 'Build a security monitoring dashboard with threat detection, vulnerability scanning, and compliance reporting',
                'why_choose': 'Security is the #1 concern for businesses. Secure engineers are always in demand.'
            },
            8: {
                'name': 'Product Management',
                'keywords': ['agile', 'scrum', 'leadership', 'communication', 'problem_solving', 'ui/ux', 'analytics'],
                'roles': ['Product Manager', 'Technical Product Manager', 'Product Owner', 'Project Manager'],
                'learning_path': [
                    'Product Strategy',
                    'Agile & Scrum Mastery',
                    'UX/UI Principles',
                    'Data-Driven Decision Making',
                    'Stakeholder Management',
                    'Roadmap Planning',
                    'Go-to-Market Strategy'
                ],
                'salary_range': '$85K - $160K',
                'growth_potential': 'High (20% growth over 5 years)',
                'entry_level_skills': ['communication', 'leadership', 'problem_solving', 'agile'],
                'description': 'Lead product development from vision to launch. Bridge the gap between business and tech.',
                'industry': ['Tech', 'Healthcare', 'Finance', 'Startups'],
                'remote_opportunities': 'High - 75% remote roles available',
                'project_idea': 'Lead a product from concept to launch, including market research, feature prioritization, and go-to-market strategy',
                'why_choose': 'Product Management is the perfect blend of business, design, and technology.'
            },
            9: {
                'name': 'Game Development',
                'keywords': ['c++', 'c#', 'python', 'unity', 'unreal', 'opengl', 'directx', '3d'],
                'roles': ['Game Developer', 'Gameplay Engineer', 'Graphics Engineer', 'Unity/Unreal Developer'],
                'learning_path': [
                    'C++ / C# Mastery',
                    'Unity / Unreal Engine',
                    'Game Physics',
                    'Computer Graphics',
                    'Multiplayer Networking',
                    'Game Design',
                    'Optimization'
                ],
                'salary_range': '$75K - $130K',
                'growth_potential': 'Medium (15% growth over 5 years)',
                'entry_level_skills': ['c++', 'c#', 'git', 'problem_solving'],
                'description': 'Create engaging interactive games and experiences for millions of players worldwide.',
                'industry': ['Gaming', 'Entertainment', 'Education', 'Simulation'],
                'remote_opportunities': 'Medium - 50% remote roles available',
                'project_idea': 'Build a complete 3D game with Unity/Unreal, including physics, AI, and multiplayer features',
                'why_choose': 'Game development combines creativity with engineering. Build the next hit game!'
            }
        }
        
        # Initialize models
        self.scaler = None
        self.kmeans_model = None
        self.pca_model = None
        self.feature_vectors = None
        self.cluster_labels = None
        self.trained = False
    
    def get_skill_resources(self, skill_name: str) -> Dict:
        """Get learning resources for a specific skill with complete details"""
        if skill_name in SKILL_RESOURCES:
            return SKILL_RESOURCES[skill_name]
        return {
            'description': f'{skill_name} is a valuable skill for your career path in tech.',
            'difficulty': 'Intermediate',
            'learning_time': '2-4 months',
            'why_learn': f'Learning {skill_name} will open up new career opportunities and help you grow as a professional.',
            'resources': [
                {'name': 'Google Search', 'url': f'https://www.google.com/search?q=learn+{skill_name}'},
                {'name': 'YouTube Tutorials', 'url': f'https://www.youtube.com/results?search_query={skill_name}+tutorial'},
                {'name': 'Coursera Courses', 'url': f'https://www.coursera.org/courses?query={skill_name}'},
                {'name': 'Udemy Courses', 'url': f'https://www.udemy.com/courses/search/?q={skill_name}'}
            ],
            'certification': f'{skill_name.title()} Certification',
            'projects': [f'Build a project using {skill_name}', f'Create a portfolio with {skill_name}'],
            'job_demand': 'High demand in the job market'
        }
    
    def get_detailed_skill_info(self, skills: List[str]) -> Dict:
        """Get detailed information about all skills in a list"""
        skill_info = {}
        for skill in skills:
            skill_info[skill] = self.get_skill_resources(skill)
        return skill_info
    
    def create_feature_vector(self, skills: List[str]) -> np.ndarray:
        """Convert skills list to binary feature vector"""
        vector = [1 if skill in skills else 0 for skill in self.skill_categories]
        return np.array(vector)
    
    def create_feature_matrix(self, all_skills: List[List[str]]) -> np.ndarray:
        """Create feature matrix from list of skill lists"""
        vectors = [self.create_feature_vector(skills) for skills in all_skills]
        return np.array(vectors)
    
    def preprocess_features(self, features: np.ndarray) -> np.ndarray:
        """Scale features for clustering"""
        self.scaler = StandardScaler()
        return self.scaler.fit_transform(features)
    
    def train_clusters(self, all_skills: List[List[str]], method: str = 'kmeans', n_clusters: int = 10):
        """Train clustering model on candidate data"""
        self.feature_vectors = self.create_feature_matrix(all_skills)
        scaled_features = self.preprocess_features(self.feature_vectors)
        
        if method == 'kmeans':
            self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            self.cluster_labels = self.kmeans_model.fit_predict(scaled_features)
        elif method == 'hierarchical':
            model = AgglomerativeClustering(n_clusters=n_clusters)
            self.cluster_labels = model.fit_predict(scaled_features)
        elif method == 'dbscan':
            model = DBSCAN(eps=0.5, min_samples=2)
            self.cluster_labels = model.fit_predict(scaled_features)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        self.pca_model = PCA(n_components=2)
        self.pca_result = self.pca_model.fit_transform(scaled_features)
        self.trained = True
        return self.cluster_labels
    
    def analyze_candidate(self, skills: List[str]) -> Dict:
        """Analyze a single candidate and return comprehensive recommendations"""
        feature_vector = self.create_feature_vector(skills)
        
        if self.trained and self.kmeans_model:
            scaled_feature = self.scaler.transform([feature_vector])
            cluster_label = self.kmeans_model.predict(scaled_feature)[0]
        else:
            # Fallback to simple matching
            best_match = 0
            cluster_label = 0
            
            for cluster_id, cluster_info in self.career_clusters.items():
                cluster_skills = cluster_info['keywords']
                matches = len([s for s in cluster_skills if s in skills])
                if matches > best_match:
                    best_match = matches
                    cluster_label = cluster_id
        
        return self.get_cluster_recommendations(cluster_label, skills)
    
    def get_cluster_recommendations(self, cluster_label: int, candidate_skills: List[str]) -> Dict:
        """Get comprehensive recommendations with ALL rich data"""
        if cluster_label not in self.career_clusters:
            cluster_label = 2
        
        cluster_info = self.career_clusters[cluster_label]
        cluster_skills = cluster_info['keywords']
        
        # Calculate match details
        matched_skills = [s for s in cluster_skills if s in candidate_skills]
        missing_skills = [s for s in cluster_skills if s not in candidate_skills]
        total = len(cluster_skills)
        matched = len(matched_skills)
        match_percentage = (matched / total * 100) if total > 0 else 0
        
        # Get detailed skill resources for ALL skills (both your skills and missing)
        all_skills_info = self.get_detailed_skill_info(candidate_skills + cluster_skills)
        
        # Get resources for missing skills with full details
        missing_skills_resources = {}
        for skill in missing_skills:
            missing_skills_resources[skill] = self.get_skill_resources(skill)
        
        # Calculate potential
        if match_percentage < 30:
            potential = "Entry Level - Focus on fundamentals first"
            time_estimate = "3-6 months of dedicated learning"
        elif match_percentage < 60:
            potential = "Mid Level - Build advanced skills"
            time_estimate = "6-12 months of focused development"
        else:
            potential = "Senior Level - Refine expertise"
            time_estimate = "3-6 months of specialization"
        
        # Find alternative paths
        alternatives = self._find_alternative_paths(candidate_skills)
        
        # Build learning path with resources
        learning_path = self._generate_personalized_path(cluster_info['learning_path'], missing_skills)
        
        return {
            'cluster_name': cluster_info['name'],
            'cluster_id': cluster_label,
            'recommended_roles': cluster_info['roles'],
            'learning_path': learning_path,
            'suggested_skills': cluster_skills,
            'missing_skills': missing_skills,
            'match_percentage': round(match_percentage, 2),
            'skill_coverage': {
                'has': matched_skills,
                'missing': missing_skills,
                'total_needed': total,
                'percentage': round(match_percentage, 2)
            },
            # THIS IS THE RICH DATA SECTION - FULLY POPULATED
            'skill_resources': {
                'your_skills': {s: all_skills_info.get(s, {}) for s in candidate_skills},
                'missing_skills': missing_skills_resources
            },
            'career_info': {
                'description': cluster_info['description'],
                'salary_range': cluster_info.get('salary_range', 'Varies'),
                'growth_potential': cluster_info.get('growth_potential', 'High'),
                'entry_level_skills': cluster_info.get('entry_level_skills', []),
                'industry': cluster_info.get('industry', ['Tech']),
                'remote_opportunities': cluster_info.get('remote_opportunities', 'High'),
                'project_idea': cluster_info.get('project_idea', 'Build a project in this domain to showcase your skills'),
                'why_choose': cluster_info.get('why_choose', 'This career path offers great growth and opportunities.')
            },
            'career_potential': potential,
            'time_estimate': time_estimate,
            'alternative_paths': alternatives,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_personalized_path(self, base_path: List[str], missing_skills: List[str]) -> List[Dict]:
        """Generate personalized learning path with resources"""
        personalized = []
        
        for step in base_path:
            related_skills = []
            for skill in missing_skills:
                if skill.lower() in step.lower():
                    related_skills.append(skill)
            
            # Get resources for related skills
            resources = []
            for skill in related_skills[:2]:
                skill_data = self.get_skill_resources(skill)
                if skill_data.get('resources'):
                    resources.append({
                        'skill': skill,
                        'resources': skill_data['resources'][:2]
                    })
            
            personalized.append({
                'step': step,
                'priority': 'High' if related_skills else 'Medium',
                'related_skills': related_skills,
                'resources': resources
            })
        
        return personalized
    
    def _find_alternative_paths(self, skills: List[str]) -> List[Dict]:
        """Find alternative career paths with full details"""
        alternatives = []
        
        for cluster_id, cluster_info in self.career_clusters.items():
            cluster_skills = set(cluster_info['keywords'])
            candidate_skills = set(skills)
            
            overlap = len(cluster_skills & candidate_skills)
            total_needed = len(cluster_skills)
            
            if overlap > 0 and overlap < total_needed:
                alternatives.append({
                    'cluster_name': cluster_info['name'],
                    'cluster_id': cluster_id,
                    'match_percentage': round(overlap / total_needed * 100, 2),
                    'overlap_skills': list(cluster_skills & candidate_skills),
                    'missing_for_this': list(cluster_skills - candidate_skills)[:3],
                    'salary_range': cluster_info.get('salary_range', 'Varies'),
                    'description': cluster_info.get('description', ''),
                    'remote_opportunities': cluster_info.get('remote_opportunities', ''),
                    'roles': cluster_info['roles'][:2]
                })
        
        alternatives.sort(key=lambda x: x['match_percentage'], reverse=True)
        return alternatives[:3]

# ============================================
# TESTING
# ============================================

def generate_sample_data(n_candidates: int = 100) -> List[List[str]]:
    """Generate synthetic candidate data for training"""
    np.random.seed(42)
    
    career_skill_sets = [
        ['python', 'sql', 'spark', 'kafka', 'airflow', 'hadoop', 'java'],
        ['python', 'ml', 'dl', 'nlp', 'tensorflow', 'pytorch', 'scikit-learn'],
        ['javascript', 'react', 'nodejs', 'mongodb', 'docker', 'typescript'],
        ['aws', 'docker', 'kubernetes', 'terraform', 'jenkins', 'gcp'],
        ['java', 'spring', 'postgres', 'redis', 'microservices', 'git'],
        ['javascript', 'react', 'swift', 'kotlin', 'react-native'],
        ['python', 'sql', 'pandas', 'numpy', 'ml', 'statistics'],
        ['python', 'aws', 'linux', 'security', 'encryption'],
        ['agile', 'scrum', 'leadership', 'communication', 'analytics'],
        ['c++', 'c#', 'unity', 'unreal', 'python']
    ]
    
    all_candidates = []
    for i in range(n_candidates):
        base_skills = career_skill_sets[i % len(career_skill_sets)]
        random_skills = ['python', 'sql', 'git', 'docker', 'javascript', 'aws']
        additional = [s for s in random_skills if np.random.random() > 0.3]
        candidate_skills = list(set(base_skills + additional))
        all_candidates.append(candidate_skills)
    
    return all_candidates

if __name__ == "__main__":
    print("🚀 Career Cluster Engine Test")
    print("="*50)
    
    engine = CareerClusterEngine()
    
    print("📊 Generating sample candidate data...")
    sample_data = generate_sample_data(200)
    print(f"✅ Generated {len(sample_data)} candidates")
    
    print("🧠 Training clustering model...")
    labels = engine.train_clusters(sample_data, method='kmeans', n_clusters=10)
    print(f"✅ Training complete! Found {len(set(labels))} clusters")
    
    # Test single candidate
    print("\n🧪 Testing single candidate analysis...")
    test_candidate = ['python', 'sql', 'docker', 'aws', 'git']
    print(f"   Candidate Skills: {test_candidate}")
    
    result = engine.analyze_candidate(test_candidate)
    
    print(f"\n📈 Analysis Results:")
    print(f"   Cluster: {result['cluster_name']}")
    print(f"   Match: {result['match_percentage']}%")
    print(f"   Roles: {', '.join(result['recommended_roles'][:3])}")
    print(f"   Missing Skills: {result['missing_skills']}")
    
    # Show skill resources with links
    print(f"\n📚 Learning Resources for Missing Skills:")
    for skill, resources in result['skill_resources']['missing_skills'].items():
        print(f"\n   🔹 {skill.title()}:")
        print(f"      Description: {resources.get('description', 'N/A')}")
        print(f"      Difficulty: {resources.get('difficulty', 'N/A')}")
        print(f"      Time: {resources.get('learning_time', 'N/A')}")
        print(f"      Why Learn: {resources.get('why_learn', 'N/A')}")
        print(f"      Certification: {resources.get('certification', 'N/A')}")
        print(f"      Resources:")
        for res in resources.get('resources', [])[:2]:
            print(f"         - {res['name']}: {res['url']}")
    
    print("\n✅ All tests complete!")
    print("="*50)