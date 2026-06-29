# cv_parser.py
import re
import PyPDF2
import docx
import spacy
from typing import List, Dict

class CVParser:
    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except:
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
            self.nlp = spacy.load('en_core_web_sm')
        
        self.skill_keywords = {
            'python': ['python', 'pandas', 'numpy', 'scikit-learn'],
            'sql': ['sql', 'postgresql', 'mysql'],
            'java': ['java', 'spring', 'hibernate'],
            'javascript': ['javascript', 'react', 'angular', 'vue'],
            'ml': ['machine learning', 'ml', 'artificial intelligence'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud'],
            'docker': ['docker', 'container', 'kubernetes'],
            'git': ['git', 'github', 'version control']
        }
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
            return text
    
    def extract_text_from_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text
    
    def extract_skills(self, text: str) -> List[str]:
        text_lower = text.lower()
        found_skills = set()
        
        for skill, keywords in self.skill_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_skills.add(skill)
                    break
        
        return list(found_skills)
    
    def parse_cv(self, file_path: str) -> Dict:
        ext = file_path.split('.')[-1].lower()
        
        if ext == 'pdf':
            text = self.extract_text_from_pdf(file_path)
        elif ext == 'docx':
            text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported format")
        
        return {
            'skills': self.extract_skills(text),
            'text_length': len(text)
        }