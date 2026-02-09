"""
ATS Resume Scoring and Optimization Engine

This module simulates modern Applicant Tracking Systems (ATS) used by companies
like Workday, Greenhouse, Lever, iCIMS, and Taleo.

Features:
- Resume parsing from PDF/DOCX/TXT
- Job Description analysis
- ATS compatibility scoring (0-100)
- Gap analysis and improvement suggestions
- Resume optimization
"""

import re
import os
from typing import Dict, List, Tuple, Set
from collections import Counter
import json
from datetime import datetime


class ATSEngine:
    """Main ATS Engine for resume scoring and optimization"""
    
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'have', 'had', 'been', 'this', 'which',
            'who', 'whom', 'whose', 'their', 'they', 'them', 'both', 'each',
            'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'just',
            'should', 'now', 'about', 'across', 'after', 'against', 'along',
            'among', 'around', 'because', 'before', 'behind', 'below', 'beneath',
            'beside', 'between', 'beyond', 'but', 'concerning', 'despite',
            'down', 'during', 'except', 'following', 'for', 'from', 'in',
            'including', 'into', 'like', 'near', 'of', 'off', 'on', 'onto',
            'out', 'over', 'past', 'plus', 'regarding', 'since', 'through',
            'throughout', 'to', 'towards', 'under', 'until', 'up', 'upon',
            'upon', 'with', 'within', 'without'
        }
        
        self.action_verbs = {
            'achieved', 'implemented', 'developed', 'managed', 'led', 'created',
            'designed', 'built', 'improved', 'increased', 'reduced', 'optimized',
            'delivered', 'launched', 'established', 'coordinated', 'executed',
            'analyzed', 'resolved', 'streamlined', 'automated', 'collaborated',
            'spearheaded', 'orchestrated', 'pioneered', 'transformed', 'drove',
            'architected', 'facilitated', 'modernized', 'overhauled', 'consolidated',
            'mentored', 'authored', 'presented', 'negotiated', 'realigned'
        }
        
        self.skill_categories = {
            'frontend': ['react', 'angular', 'vue', 'nextjs', 'typescript', 'javascript', 'html', 'css', 'sass', 'tailwind', 'redux', 'webpack'],
            'backend': ['python', 'java', 'node.js', 'go', 'ruby', 'php', 'rust', 'flask', 'django', 'spring', 'express', 'laravel'],
            'database': ['sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'oracle'],
            'cloud_devops': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'terraform', 'ansible', 'prometheus', 'grafana', 'ci/cd', 'pipelines'],
            'data_science': ['pandas', 'numpy', 'scipy', 'scikit-learn', 'tensorflow', 'pytorch', 'nlp', 'computer vision', 'data mining', 'tableau', 'powerbi', 'regression', 'classification', 'time-series', 'forecasting', 'lstm', 'hyperparameter', 'cross-validation', 'feature engineering', 'eda', 'machine learning', 'deep learning', 'artificial intelligence', 'ai', 'ml'],
            'mobile': ['react native', 'flutter', 'swift', 'kotlin', 'objective-c', 'ios', 'android'],
            'professional': ['agile', 'scrum', 'jira', 'project management', 'leadership', 'communication', 'problem solving', 'teamwork', 'collaboration']
        }

        self.synonym_map = {
            'ml': 'machine learning',
            'ai': 'artificial intelligence',
            'sklearn': 'scikit-learn',
            'js': 'javascript',
            'ts': 'typescript',
            'reactjs': 'react',
            'nodejs': 'node.js',
            'nlp': 'natural language processing',
            'cv': 'computer vision',
            'aws': 'amazon web services',
            'gcp': 'google cloud platform',
            'azure': 'microsoft azure',
            'rest': 'restful',
            'git': 'github',
            'eda': 'exploratory data analysis',
            'api': 'application programming interface',
            'dl': 'deep learning',
            'ci/cd': 'continuous integration',
            'cicd': 'continuous integration',
            'k8s': 'kubernetes',
            'qa': 'quality assurance',
            'seo': 'search engine optimization'
        }

    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill terms to standard canonical forms"""
        skill_lower = skill.lower().strip()
        # Direct lookup
        if skill_lower in self.synonym_map:
            return self.synonym_map[skill_lower]
        return skill_lower
        
    def parse_resume(self, resume_text: str) -> Dict:
        """
        Extract structured data from resume text
        
        Args:
            resume_text: Raw resume text
            
        Returns:
            Dictionary containing parsed resume components
        """
        resume_data = {
            'contact_info': self._extract_contact_info(resume_text),
            'summary': self._extract_summary(resume_text),
            'skills': self._extract_skills(resume_text),
            'experience': self._extract_experience(resume_text),
            'education': self._extract_education(resume_text),
            'certifications': self._extract_certifications(resume_text),
            'projects': self._extract_projects(resume_text),
            'keywords': self._extract_keywords(resume_text),
            'formatting_issues': self._detect_formatting_issues(resume_text)
        }
        
        return resume_data
    
    def analyze_job_description(self, jd_text: str) -> Dict:
        """
        Extract and classify job description requirements
        
        Args:
            jd_text: Job description text
            
        Returns:
            Dictionary containing JD analysis
        """
        jd_data = {
            'mandatory_skills': self._extract_mandatory_skills(jd_text),
            'preferred_skills': self._extract_preferred_skills(jd_text),
            'tools_technologies': self._extract_tools_technologies(jd_text),
            'experience_required': self._extract_experience_requirement(jd_text),
            'responsibilities': self._extract_responsibilities(jd_text),
            'domain_keywords': self._extract_domain_keywords(jd_text),
            'action_verbs': self._extract_action_verbs_from_jd(jd_text),
            'weighted_keywords': self._assign_keyword_weights(jd_text)
        }
        
        return jd_data
    
    def calculate_suitability(self, score_data: Dict, resume_data: Dict, jd_data: Dict) -> Dict:
        """
        Calculate overall suitability for the HR team
        
        Args:
            score_data: ATS score results
            resume_data: Parsed resume data
            jd_data: Analyzed JD data
            
        Returns:
            Dictionary with HR-specific suitability metrics
        """
        score = score_data['total_score']
        
        # Determine verdict based on STRICT visibility rules
        vis = score_data.get('visibility_status', {})
        
        if vis.get('contact_details_unlocked', False):
            # Perfect Match: >= 85 AND All Mandatory Skills AND Exp > 60
            verdict = "Perfect Match ✅"
            color = "var(--accent-teal)"
            recommendation = "Shortlist immediately! Meets all critical criteria. 🚀"
        elif vis.get('is_limited_visibility', False):
            # Potential Match: 70-84 OR High score with missing mandatory
            verdict = "Potential Match ⚠️"
            color = "#f59e0b"
            if score >= 85:
                recommendation = "High score but missing mandatory skills. Check gaps carefully. 🔍"
            else:
                recommendation = "Solid foundation. Needs specific keywords to cross the threshold. 📈"
        else:
            # Hidden: < 70
            verdict = "Needs Improvement ❌"
            color = "#ef4444"
            recommendation = "Significant gaps detected. Focus on mandatory skills and experience context. 💪"
            
        # Recruiter Insights
        insights = []
        
        # 1. Experience Check
        years_req = jd_data.get('experience_required', 'Not specified')
        insights.append(f"Experience Match: {years_req} mentioned in JD.")
            
        # 2. Key Skill Match
        mandatory = set(jd_data['mandatory_skills'])
        resume_skills = set(resume_data['skills'])
        matched = mandatory & resume_skills
        if mandatory:
            match_pct = (len(matched) / len(mandatory)) * 100
            insights.append(f"Technical Core: {len(matched)}/{len(mandatory)} mandatory technologies found.")
            
        # 3. Soft Skill Detection
        soft_skills = ['leadership', 'collaboration', 'communication', 'problem-solving', 'teamwork', 'agile']
        found_soft = [s for s in soft_skills if s in ' '.join(resume_data['skills'] + [resume_data['summary']]).lower()]
        if found_soft:
            insights.append(f"Soft Skills Found: {', '.join(found_soft)}.")
        else:
            insights.append("Soft Skills: Limited explicit soft skill keywords detected.")
            
        return {
            'verdict': verdict,
            'color': color,
            'recommendation': recommendation,
            'recruiter_insights': insights,
            'risk_level': "Low" if score > 75 else ("Medium" if score > 50 else "High"),
            'suitability_score': int(score)
        }

    def calculate_ats_score(self, resume_data: Dict, jd_data: Dict) -> Dict:
        """
        Calculate ATS compatibility score (0-100) with breakdown
        
        Scoring components:
        - Keyword Match: 40%
        - Skills Match: 25%
        - Experience Alignment: 15%
        - Role & Domain Similarity: 10%
        - Resume Formatting: 10%
        
        Args:
            resume_data: Parsed resume data
            jd_data: Analyzed job description data
            
        Returns:
            Dictionary containing score and breakdown
        """
        # Calculate individual scores
        keyword_score = self._calculate_keyword_match(resume_data, jd_data)
        skills_score = self._calculate_skills_match(resume_data, jd_data)
        experience_score = self._calculate_experience_alignment(resume_data, jd_data)
        domain_score = self._calculate_domain_similarity(resume_data, jd_data)
        formatting_score = self._calculate_formatting_score(resume_data)
        
        # Weighted total
        # Scale based on new weights (30% Semantic, 30% Skills, 20% Keywords, 15% Exp, 5% Format)
        # Assuming domain_score covers semantic similarity
        
        total_score = (
            domain_score * 0.30 +
            skills_score * 0.30 +
            keyword_score * 0.20 +
            experience_score * 0.15 +
            formatting_score * 0.05
        )
        
        # --- Multi-Gate Visibility Logic ---
        # 1. Mandatory Skills Check
        resume_skills_norm = set(self._normalize_skill(s) for s in resume_data['skills'])
        mandatory_skills_norm = set(self._normalize_skill(s) for s in jd_data['mandatory_skills'])
        missing_mandatory = mandatory_skills_norm - resume_skills_norm
        has_all_mandatory = len(missing_mandatory) == 0

        # 2. Gate Conditions
        # Perfect Match Requirements: >= 85 Score AND All Mandatory Skills AND Decent Experience
        is_perfect_match = (total_score >= 85) and has_all_mandatory and (experience_score >= 60)
        
        # Potential Match: 70-84 OR High Score but missing mandatory skills
        is_potential_match = (70 <= total_score < 85) or (total_score >= 85 and not is_perfect_match)

        visibility_status = {
            'is_recruiter_visible': is_perfect_match or is_potential_match, # Visible but maybe limited
            'is_limited_visibility': is_potential_match,
            'is_hidden': total_score < 70,
            'contact_details_unlocked': is_perfect_match, # STRICT UNLOCK
            'missing_mandatory': list(missing_mandatory)
        }

        return {
            'total_score': round(total_score, 2),
            'visibility_status': visibility_status,
            'breakdown': {
                'domain_similarity': {'score': round(domain_score, 2), 'weight': '30%'},
                'skills_match': {
                    'score': round(skills_score, 2), 
                    'weight': '30%',
                    'matched': list(resume_skills_norm & mandatory_skills_norm),
                    'missing': list(missing_mandatory)
                },
                'keyword_match': {'score': round(keyword_score, 2), 'weight': '20%'},
                'experience_alignment': {'score': round(experience_score, 2), 'weight': '15%'},
                'formatting': {'score': round(formatting_score, 2), 'weight': '5%'}
            }
        }
    
    def perform_gap_analysis(self, resume_data: Dict, jd_data: Dict) -> Dict:
        """
        Identify gaps between resume and job requirements
        
        Args:
            resume_data: Parsed resume data
            jd_data: Analyzed job description data
            
        Returns:
            Dictionary containing gap analysis
        """
        resume_keywords = set(resume_data['keywords'])
        resume_skills = set(self._normalize_skill(s) for s in resume_data['skills'])
        
        # Find missing elements with normalization support
        mandatory_jd = set(self._normalize_skill(s) for s in jd_data['mandatory_skills'])
        preferred_jd = set(self._normalize_skill(s) for s in jd_data['preferred_skills'])
        tools_jd = set(self._normalize_skill(s) for s in jd_data['tools_technologies'])

        missing_mandatory = mandatory_jd - resume_skills
        missing_preferred = preferred_jd - resume_skills
        missing_tools = tools_jd - resume_skills
        missing_keywords = set(jd_data['domain_keywords']) - resume_keywords
        
        # Classify gaps
        gaps = {
            'critical': {
                'missing_mandatory_skills': list(missing_mandatory),
                'missing_key_tools': list(missing_tools & set(jd_data['mandatory_skills']))
            },
            'important': {
                'missing_preferred_skills': list(missing_preferred),
                'missing_domain_keywords': list(missing_keywords)[:10],  # Top 10
                'weak_action_verbs': self._find_weak_action_verbs(resume_data, jd_data)
            },
            'optional': {
                'missing_nice_to_have': list(set(jd_data['tools_technologies']) - missing_tools - resume_skills)
            },
            'formatting_issues': resume_data['formatting_issues']
        }
        
        return gaps
    
    def generate_improvements(self, resume_data: Dict, jd_data: Dict, gaps: Dict) -> Dict:
        """
        Generate actionable improvement suggestions
        
        Args:
            resume_data: Parsed resume data
            jd_data: Analyzed job description data
            gaps: Gap analysis results
            
        Returns:
            Dictionary containing improvement suggestions
        """
        improvements = {
            'keyword_insertions': self._suggest_keyword_insertions(resume_data, gaps),
            'bullet_point_rewrites': self._suggest_bullet_rewrites(resume_data, jd_data),
            'skills_section': self._suggest_skills_restructure(resume_data, jd_data),
            'summary_optimization': self._suggest_summary_optimization(resume_data, jd_data),
            'title_alignment': self._suggest_title_alignment(resume_data, jd_data),
            'formatting_fixes': self._suggest_formatting_fixes(resume_data)
        }
        
        return improvements
    
    def optimize_resume(self, resume_data: Dict, jd_data: Dict, improvements: Dict) -> str:
        """
        Generate ATS-optimized resume
        
        Args:
            resume_data: Parsed resume data
            jd_data: Analyzed job description data
            improvements: Improvement suggestions
            
        Returns:
            Optimized resume text
        """
        optimized_sections = []
        
        # Header
        contact = resume_data['contact_info']
        optimized_sections.append(self._format_header(contact))
        
        # Professional Summary
        optimized_sections.append(self._format_summary(
            resume_data['summary'], 
            improvements['summary_optimization']
        ))
        
        # Skills
        optimized_sections.append(self._format_skills(
            resume_data['skills'],
            improvements['skills_section']
        ))
        
        # Experience
        optimized_sections.append(self._format_experience(
            resume_data['experience'],
            improvements['bullet_point_rewrites']
        ))
        
        # Education
        optimized_sections.append(self._format_education(resume_data['education']))
        
        # Certifications
        if resume_data['certifications']:
            optimized_sections.append(self._format_certifications(resume_data['certifications']))
        
        # Projects
        if resume_data['projects']:
            optimized_sections.append(self._format_projects(resume_data['projects']))
        
        return '\n\n'.join(optimized_sections)
    
    # ==================== HELPER METHODS ====================
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        
        email = re.search(email_pattern, text)
        phone = re.search(phone_pattern, text)
        
        # Extract name (usually first line)
        lines = text.strip().split('\n')
        name = lines[0].strip() if lines else "Name Not Found"
        
        return {
            'name': name,
            'email': email.group() if email else '',
            'phone': phone.group() if phone else '',
            'location': self._extract_location(text)
        }
    
    def _extract_location(self, text: str) -> str:
        """Extract location from text"""
        # Common location patterns
        location_keywords = ['india', 'bangalore', 'mumbai', 'delhi', 'hyderabad', 
                           'pune', 'chennai', 'kolkata', 'usa', 'uk', 'canada']
        
        text_lower = text.lower()
        for keyword in location_keywords:
            if keyword in text_lower:
                # Extract surrounding context
                idx = text_lower.index(keyword)
                return text[max(0, idx-20):min(len(text), idx+30)].strip()
        
        return ''
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary"""
        summary_keywords = ['summary', 'profile', 'objective', 'about']
        
        lines = text.split('\n')
        summary_lines = []
        in_summary = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in summary_keywords):
                in_summary = True
                continue
            
            if in_summary:
                if line.strip() and not self._is_section_header(line):
                    summary_lines.append(line.strip())
                elif len(summary_lines) > 0:
                    break
        
        return ' '.join(summary_lines)
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text by category matching and section analysis"""
        text_lower = text.lower()
        skills = set()
        
        # 1. Direct Category Matching (High Precision)
        for cat, list_of_skills in self.skill_categories.items():
            for skill in list_of_skills:
                # Use word boundaries to avoid partial matches (e.g., 'java' in 'javascript')
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    skills.add(skill)
        
        # 2. Section Based Extraction (High Recall)
        skills_section = self._extract_section(text, ['skills', 'technical skills', 'core competencies', 'technologies'])
        if skills_section:
            # Clean and split by common delimiters
            # Handles bullets, commas, vertical bars, and newlines
            raw_items = re.split(r'[,;|\n•·\t\*]| {2,}', skills_section)
            for item in raw_items:
                cleaned = item.strip().lower()
                # Basic cleaning: remove trailing periods, brackets
                cleaned = re.sub(r'[\.\:\(\)]', '', cleaned).strip()
                if cleaned and 2 < len(cleaned) < 30:
                    # Avoid adding junk (like long sentences)
                    if len(cleaned.split()) <= 4:
                        skills.add(cleaned)
        
        return sorted(list(skills))
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience"""
        experience_section = self._extract_section(text, ['experience', 'work experience', 'employment'])
        
        if not experience_section:
            return []
        
        # Split into individual jobs (usually separated by company/role headers)
        experiences = []
        current_exp = {}
        
        lines = experience_section.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if it's a role/company line (usually has dates)
            if re.search(r'\d{4}', line):
                if current_exp:
                    experiences.append(current_exp)
                current_exp = {
                    'header': line,
                    'bullets': []
                }
            elif line.startswith(('•', '-', '*', '·')) or current_exp:
                if current_exp:
                    current_exp['bullets'].append(line.lstrip('•-*· '))
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_section = self._extract_section(text, ['education', 'academic', 'qualification'])
        
        if not education_section:
            return []
        
        return [line.strip() for line in education_section.split('\n') if line.strip()]
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_section = self._extract_section(text, ['certification', 'certificates', 'licenses'])
        
        if not cert_section:
            return []
        
        return [line.strip() for line in cert_section.split('\n') if line.strip()]
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract projects"""
        project_section = self._extract_section(text, ['projects', 'personal projects', 'key projects'])
        
        if not project_section:
            return []
        
        projects = []
        current_project = {}
        
        lines = project_section.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if not line.startswith(('•', '-', '*', '·')):
                if current_project:
                    projects.append(current_project)
                current_project = {
                    'title': line,
                    'description': []
                }
            elif current_project:
                current_project['description'].append(line.lstrip('•-*· '))
        
        if current_project:
            projects.append(current_project)
        
        return projects
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract all keywords from resume"""
        # Remove common words
        # Remove common words, handling compound terms like scikit-learn or ci/cd
        words = re.findall(r'\b[a-z]{2,}(?:[-/][a-z]{2,})*\b', text.lower())
        keywords = [w for w in words if w not in self.stop_words]
        
        # Count frequency
        keyword_freq = Counter(keywords)
        
        # Return all unique keywords found
        return list(keyword_freq.keys())
    
    def _detect_formatting_issues(self, text: str) -> List[str]:
        """Detect ATS-unfriendly formatting"""
        issues = []
        
        # Check for tables (common issue)
        if '|' in text or '\t' in text:
            issues.append("Contains tables or tabs - may not parse correctly in ATS")
        
        # Check for special characters
        special_chars = set(text) - set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n.,;:()[]{}@#$%&*+-=/<>?!"\'\t')
        if special_chars:
            issues.append(f"Contains special characters that may not parse: {', '.join(list(special_chars)[:5])}")
        
        # Check for graphics indicators
        if any(indicator in text.lower() for indicator in ['[image]', '[graphic]', '[icon]']):
            issues.append("Contains graphics/icons - remove for ATS compatibility")
        
        return issues
    
    def _extract_section(self, text: str, keywords: List[str]) -> str:
        """Extract a specific section from resume"""
        lines = text.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in keywords):
                in_section = True
                continue
            
            if in_section:
                if self._is_section_header(line) and not any(k in line_lower for k in keywords):
                    break
                section_lines.append(line)
        
        return '\n'.join(section_lines)
    
    def _is_section_header(self, line: str) -> bool:
        """Check if line is a section header"""
        common_headers = [
            'summary', 'profile', 'experience', 'education', 'skills',
            'certifications', 'projects', 'achievements', 'awards'
        ]
        line_lower = line.lower().strip()
        return any(header in line_lower for header in common_headers) and len(line.strip()) < 50
    
    def _extract_mandatory_skills(self, jd_text: str) -> List[str]:
        """Extract mandatory skills from JD with bullet point awareness"""
        mandatory_keywords = ['required', 'must have', 'essential', 'mandatory', 'requirements']
        skills = set()
        
        lines = jd_text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in mandatory_keywords):
                # We found a requirements header. Look at subsequent lines.
                for offset in range(1, 15): # Look further ahead
                    if i + offset >= len(lines): break
                    next_line = lines[i + offset].strip()
                    if not next_line: continue
                    
                    # If we hit another major header, stop
                    if self._is_section_header(next_line) and not any(k in next_line.lower() for k in mandatory_keywords):
                        break
                        
                    # Extract skills from this specific line
                    skills.update(self._extract_skills_from_text(next_line))
        
        return list(skills)

    def _extract_preferred_skills(self, jd_text: str) -> List[str]:
        """Extract preferred skills from JD with bullet point awareness"""
        preferred_keywords = ['preferred', 'nice to have', 'bonus', 'plus', 'desired']
        skills = set()
        
        lines = jd_text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in preferred_keywords):
                for offset in range(1, 10):
                    if i + offset >= len(lines): break
                    next_line = lines[i + offset].strip()
                    if not next_line: continue
                    if self._is_section_header(next_line): break
                    skills.update(self._extract_skills_from_text(next_line))
        
        return list(skills)

    def _extract_tools_technologies(self, jd_text: str) -> List[str]:
        """Extract tools and technologies from JD"""
        return self._extract_skills(jd_text)

    def _extract_experience_requirement(self, jd_text: str) -> str:
        """Extract years of experience required"""
        exp_pattern = r'(\d+(?:\s?(?:-|to)\s?\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)?'
        match = re.search(exp_pattern, jd_text.lower())
        
        return match.group() if match else 'Not specified'
    
    def _extract_responsibilities(self, jd_text: str) -> List[str]:
        """Extract job responsibilities"""
        resp_section = self._extract_section(jd_text, ['responsibilities', 'duties', 'you will'])
        
        if not resp_section:
            return []
        
        responsibilities = []
        for line in resp_section.split('\n'):
            line = line.strip()
            if line and (line.startswith(('•', '-', '*', '·')) or len(responsibilities) < 10):
                responsibilities.append(line.lstrip('•-*· '))
        
        return responsibilities
    
    def _extract_domain_keywords(self, jd_text: str) -> List[str]:
        """Extract domain-specific keywords"""
        return self._extract_keywords(jd_text)
    
    def _extract_action_verbs_from_jd(self, jd_text: str) -> List[str]:
        """Extract action verbs from JD"""
        text_lower = jd_text.lower()
        found_verbs = []
        
        for verb in self.action_verbs:
            if verb in text_lower:
                found_verbs.append(verb)
        
        return found_verbs
    
    def _assign_keyword_weights(self, jd_text: str) -> Dict[str, float]:
        """Assign weights to keywords based on importance"""
        keywords = self._extract_keywords(jd_text)
        weights = {}
        
        # Higher weight for keywords in title or early in JD
        lines = jd_text.split('\n')
        early_text = ' '.join(lines[:10]).lower()
        
        for keyword in keywords:
            if keyword in early_text:
                weights[keyword] = 1.5
            else:
                weights[keyword] = 1.0
        
        return weights
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from a text snippet"""
        # Reuse the skills extraction logic
        return self._extract_skills(text)
    
    def _calculate_keyword_match(self, resume_data: Dict, jd_data: Dict) -> float:
        """Calculate weighted keyword match score with normalization"""
        # Normalize resume keywords
        resume_keywords = set(self._normalize_skill(k) for k in resume_data.get('keywords', []))
        
        jd_weighted = jd_data.get('weighted_keywords', {})
        if not jd_weighted:
            return 100.0
        
        # Normalize JD weighted keywords key-by-key
        normalized_weights = {}
        for kw, weight in jd_weighted.items():
            norm_kw = self._normalize_skill(kw)
            normalized_weights[norm_kw] = max(normalized_weights.get(norm_kw, 0), weight)
            
        max_score = sum(normalized_weights.values())
        if max_score == 0: return 100.0

        current_score = sum(weight for kw, weight in normalized_weights.items() if kw in resume_keywords)
        
        score = (current_score / max_score) * 100
        return min(score, 100.0)

    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill names using synonym map"""
        s = skill.lower().strip()
        return self.synonym_map.get(s, s)

    def _calculate_skills_match(self, resume_data: Dict, jd_data: Dict) -> float:
        """Calculate skills match score with higher precision and synonym support"""
        resume_skills = set(self._normalize_skill(s) for s in resume_data['skills'])
        
        mandatory_skills = set(self._normalize_skill(s) for s in jd_data['mandatory_skills'])
        preferred_skills = set(self._normalize_skill(s) for s in jd_data['preferred_skills'])
        
        # Mandatory skills (Critical)
        if mandatory_skills:
            mandatory_matched = resume_skills & mandatory_skills
            # Non-linear scoring: matching most is very good
            ratio = len(mandatory_matched) / len(mandatory_skills)
            if ratio >= 0.8: mandatory_score = 100
            elif ratio >= 0.5: mandatory_score = 85
            else: mandatory_score = ratio * 100
        else:
            mandatory_score = 100.0
            
        # Preferred skills (Bonus)
        if preferred_skills:
            preferred_matched = resume_skills & preferred_skills
            preferred_score = (len(preferred_matched) / len(preferred_skills)) * 100
        else:
            preferred_score = 100.0
            
        # Weighted average: 80% mandatory, 20% preferred
        return min((mandatory_score * 0.8) + (preferred_score * 0.2), 100.0)

    def _calculate_experience_alignment(self, resume_data: Dict, jd_data: Dict) -> float:
        """Calculate experience alignment based on duration and context"""
        if not resume_data['experience']:
            return 20.0 # Partial credit for implicit experience in other sections

        # Context match
        exp_text = ' '.join([str(exp.get('header', '')) + ' ' + ' '.join(exp.get('bullets', [])) 
                            for exp in resume_data['experience']]).lower()
        
        # Use normalized skill matching in experience text too
        jd_keywords = set(self._normalize_skill(jw) for jw in jd_data['domain_keywords'][:25])
        
        matched_count = 0
        for kw in jd_keywords:
            if kw in exp_text:
                matched_count += 1
        
        # Base score is higher to avoid "0" experience shock
        if not jd_keywords:
            context_score = 100.0
        else:
            # Non-linear scoring for experience context
            ratio = matched_count / len(jd_keywords)
            if ratio > 0.6: context_score = 100
            elif ratio > 0.3: context_score = 85
            else: context_score = 50 + (ratio * 100)

        # Action verb density
        resume_verbs = [v for v in self.action_verbs if v in exp_text]
        # Cap at 15 verbs for max score
        verb_score = min((len(resume_verbs) / 10) * 100, 100.0)
        
        return min((context_score * 0.7) + (verb_score * 0.3), 100.0)

    def _calculate_domain_similarity(self, resume_data: Dict, jd_data: Dict) -> float:
        """Calculate semantic domain similarity"""
        resume_text = (resume_data.get('summary', '') + ' ' + 
                      ' '.join([exp.get('header', '') for exp in resume_data['experience']])).lower()
        
        jd_keywords = set(jd_data['domain_keywords'])
        if not jd_keywords:
            return 100.0
            
        # Check for presence of key domain concepts (with semantic normalization)
        found = 0
        for kw in jd_keywords:
            norm_kw = self._normalize_skill(kw)
            # Check raw keyword OR normalized keyword
            if kw in resume_text or norm_kw in resume_text:
                found += 1
                
        score = (found / len(jd_keywords)) * 100
        
        return min(score, 100.0)
    
    def _calculate_formatting_score(self, resume_data: Dict) -> float:
        """Calculate formatting score"""
        issues = resume_data['formatting_issues']
        
        # Deduct points for each issue
        score = 100.0 - (len(issues) * 15)
        
        return max(score, 0.0)
    
    def _find_weak_action_verbs(self, resume_data: Dict, jd_data: Dict) -> List[str]:
        """Find weak action verbs in resume"""
        weak_verbs = ['responsible for', 'worked on', 'helped with', 'assisted in']
        
        found_weak = []
        for exp in resume_data['experience']:
            for bullet in exp.get('bullets', []):
                for weak in weak_verbs:
                    if weak in bullet.lower():
                        found_weak.append(f"'{weak}' in: {bullet[:50]}...")
        
        return found_weak[:5]  # Top 5
    
    def _suggest_keyword_insertions(self, resume_data: Dict, gaps: Dict) -> List[Dict]:
        """Suggest where to insert missing keywords"""
        suggestions = []
        
        # Critical missing skills
        for skill in gaps['critical']['missing_mandatory_skills'][:5]:
            suggestions.append({
                'keyword': skill,
                'location': 'Skills section',
                'priority': 'CRITICAL',
                'suggestion': f"Add '{skill}' to your skills section if you have experience with it"
            })
        
        # Important keywords
        for keyword in gaps['important']['missing_domain_keywords'][:5]:
            suggestions.append({
                'keyword': keyword,
                'location': 'Experience bullets or Summary',
                'priority': 'IMPORTANT',
                'suggestion': f"Incorporate '{keyword}' in relevant experience descriptions"
            })
        
        return suggestions
    
    def _suggest_bullet_rewrites(self, resume_data: Dict, jd_data: Dict) -> List[Dict]:
        """Suggest bullet point improvements using STAR method"""
        suggestions = []
        
        for exp in resume_data['experience'][:2]:  # Top 2 experiences
            for bullet in exp.get('bullets', [])[:3]:  # Top 3 bullets each
                # Check if bullet uses action verbs
                starts_with_action = any(bullet.lower().startswith(verb) for verb in self.action_verbs)
                
                if not starts_with_action:
                    suggestions.append({
                        'original': bullet,
                        'improved': self._rewrite_bullet_star(bullet, jd_data),
                        'reason': 'Start with strong action verb and quantify impact'
                    })
        
        return suggestions[:5]  # Top 5
    
    def _rewrite_bullet_star(self, bullet: str, jd_data: Dict) -> str:
        """Rewrite bullet using STAR method"""
        # Simple template-based rewrite
        action_verb = list(self.action_verbs & set(jd_data['action_verbs']))[0] if (self.action_verbs & set(jd_data['action_verbs'])) else 'Developed'
        
        # Try to preserve the core content
        core_content = bullet.lstrip('•-*· ').strip()
        
        return f"{action_verb.capitalize()} {core_content}, resulting in [quantifiable impact]"
    
    def _suggest_skills_restructure(self, resume_data: Dict, jd_data: Dict) -> Dict:
        """Suggest skills section restructuring"""
        resume_skills = set(s.lower() for s in resume_data['skills'])
        jd_mandatory = set(s.lower() for s in jd_data['mandatory_skills'])
        jd_preferred = set(s.lower() for s in jd_data['preferred_skills'])
        
        matched_mandatory = list(resume_skills & jd_mandatory)
        matched_preferred = list(resume_skills & jd_preferred)
        other_skills = list(resume_skills - jd_mandatory - jd_preferred)
        
        return {
            'structure': 'Categorize skills by relevance',
            'categories': {
                'Core Technical Skills': matched_mandatory[:10],
                'Additional Skills': matched_preferred[:8],
                'Other Competencies': other_skills[:5]
            },
            'note': 'Place most relevant skills first for ATS optimization'
        }
    
    def _suggest_summary_optimization(self, resume_data: Dict, jd_data: Dict) -> str:
        """Suggest optimized professional summary"""
        # Extract key elements
        top_skills = jd_data['mandatory_skills'][:3]
        experience_req = jd_data['experience_required']
        
        template = f"""Results-driven professional with expertise in {', '.join(top_skills[:2])} and {top_skills[2] if len(top_skills) > 2 else 'related technologies'}. Proven track record of delivering high-impact solutions and driving business outcomes. Seeking to leverage technical skills and experience to contribute to [Company Name]'s success."""
        
        return template
    
    def _suggest_title_alignment(self, resume_data: Dict, jd_data: Dict) -> List[str]:
        """Suggest job title alignment"""
        suggestions = []
        
        # Extract common role keywords from JD
        jd_text = ' '.join(jd_data['responsibilities']).lower()
        
        role_keywords = ['engineer', 'developer', 'analyst', 'manager', 'architect', 'lead', 'senior']
        found_roles = [role for role in role_keywords if role in jd_text]
        
        if found_roles:
            suggestions.append(f"Consider aligning your title to include: {', '.join(found_roles)}")
        
        return suggestions
    
    def _suggest_formatting_fixes(self, resume_data: Dict) -> List[str]:
        """Suggest formatting improvements"""
        fixes = []
        
        for issue in resume_data['formatting_issues']:
            if 'table' in issue.lower():
                fixes.append("Remove tables - use simple bullet points instead")
            elif 'special character' in issue.lower():
                fixes.append("Remove special characters and icons")
            elif 'graphic' in issue.lower():
                fixes.append("Remove all graphics and images")
        
        # General ATS best practices
        fixes.extend([
            "Use standard section headings (Summary, Experience, Education, Skills)",
            "Use simple bullet points (• or -)",
            "Avoid headers/footers",
            "Use standard fonts (Arial, Calibri, Times New Roman)",
            "Save as .docx or PDF (text-based, not image)"
        ])
        
        return fixes
    
    def _format_header(self, contact: Dict) -> str:
        """Format resume header"""
        return f"""{contact['name'].upper()}
{contact['email']} | {contact['phone']} | {contact['location']}"""
    
    def _format_summary(self, original_summary: str, optimization: str) -> str:
        """Format professional summary"""
        summary = optimization if optimization else original_summary
        return f"""PROFESSIONAL SUMMARY
{summary}"""
    
    def _format_skills(self, skills: List[str], restructure: Dict) -> str:
        """Format skills section"""
        formatted = "TECHNICAL SKILLS\n"
        
        if 'categories' in restructure:
            for category, skill_list in restructure['categories'].items():
                if skill_list:
                    formatted += f"\n{category}:\n"
                    formatted += ', '.join(skill_list) + "\n"
        else:
            formatted += ', '.join(skills)
        
        return formatted
    
    def _format_experience(self, experiences: List[Dict], bullet_rewrites: List[Dict]) -> str:
        """Format experience section"""
        formatted = "PROFESSIONAL EXPERIENCE\n"
        
        for exp in experiences:
            formatted += f"\n{exp.get('header', '')}\n"
            
            for bullet in exp.get('bullets', []):
                # Check if we have a rewrite for this bullet
                rewritten = next((r['improved'] for r in bullet_rewrites if r['original'] == bullet), bullet)
                formatted += f"• {rewritten}\n"
        
        return formatted
    
    def _format_education(self, education: List[str]) -> str:
        """Format education section"""
        formatted = "EDUCATION\n"
        for edu in education:
            formatted += f"{edu}\n"
        return formatted
    
    def _format_certifications(self, certifications: List[str]) -> str:
        """Format certifications section"""
        formatted = "CERTIFICATIONS\n"
        for cert in certifications:
            formatted += f"• {cert}\n"
        return formatted
    
    def _format_projects(self, projects: List[Dict]) -> str:
        """Format projects section"""
        formatted = "KEY PROJECTS\n"
        for project in projects:
            formatted += f"\n{project.get('title', '')}\n"
            for desc in project.get('description', []):
                formatted += f"• {desc}\n"
        return formatted
    
    def generate_report(self, resume_data: Dict, jd_data: Dict, score_data: Dict, 
                       gaps: Dict, improvements: Dict, optimized_resume: str,
                       suitability_data: Dict = None) -> str:
        """
        Generate comprehensive ATS report
        
        Args:
            resume_data: Parsed resume
            jd_data: Analyzed JD
            score_data: Scoring results
            gaps: Gap analysis
            improvements: Improvement suggestions
            optimized_resume: Optimized resume text
            
        Returns:
            Formatted report string
        """
        report = []
        
        # Header
        report.append("=" * 80)
        report.append("ATS RESUME SCORING & OPTIMIZATION REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Score
        total_score = score_data.get('total_score', 0)
        report.append(f"ATS COMPATIBILITY SCORE: {total_score}/100")
        report.append("-" * 80)
        
        # Score breakdown
        report.append("\nSCORE BREAKDOWN:")
        for component, data in score_data.get('breakdown', {}).items():
            report.append(f"  {component.replace('_', ' ').title()}: {data.get('score', 0)}/100 (Weight: {data.get('weight', 0)})")
        
        # Gap analysis
        report.append("\n" + "=" * 80)
        report.append("GAP ANALYSIS")
        report.append("=" * 80)
        
        report.append("\nCRITICAL GAPS:")
        for gap_type, items in gaps['critical'].items():
            if items:
                report.append(f"  {gap_type.replace('_', ' ').title()}:")
                for item in items[:5]:
                    report.append(f"    - {item}")
        
        report.append("\nIMPORTANT GAPS:")
        for gap_type, items in gaps['important'].items():
            if items:
                report.append(f"  {gap_type.replace('_', ' ').title()}:")
                for item in items[:5]:
                    report.append(f"    - {item}")
        
        # Suitability
        if suitability_data:
            report.append("\n" + "=" * 80)
            report.append("HR SUITABILITY ASSESSMENT")
            report.append("=" * 80)
            report.append(f"VERDICT: {suitability_data.get('verdict', 'N/A')}")
            report.append(f"RISK LEVEL: {suitability_data.get('risk_level', 'N/A')}")
            report.append(f"RECOMMENDATION: {suitability_data.get('recommendation', 'N/A')}")
            
            report.append("\nRECRUITER INSIGHTS:")
            for insight in suitability_data.get('recruiter_insights', []):
                report.append(f"  • {insight}")
        
        # Improvements
        report.append("\n" + "=" * 80)
        report.append("IMPROVEMENT RECOMMENDATIONS")
        report.append("=" * 80)
        
        report.append("\nKEYWORD INSERTIONS:")
        for suggestion in improvements['keyword_insertions'][:5]:
            report.append(f"  [{suggestion['priority']}] {suggestion['keyword']}")
            report.append(f"    Location: {suggestion['location']}")
            report.append(f"    Suggestion: {suggestion['suggestion']}\n")
        
        report.append("\nBULLET POINT REWRITES:")
        for rewrite in improvements['bullet_point_rewrites'][:3]:
            report.append(f"  Original: {rewrite['original']}")
            report.append(f"  Improved: {rewrite['improved']}")
            report.append(f"  Reason: {rewrite['reason']}\n")
        
        report.append("\nFORMATTING FIXES:")
        for fix in improvements['formatting_fixes'][:5]:
            report.append(f"  • {fix}")
        
        # Optimized resume
        report.append("\n" + "=" * 80)
        report.append("OPTIMIZED RESUME")
        report.append("=" * 80)
        report.append(optimized_resume)
        
        # Keyword comparison
        report.append("\n" + "=" * 80)
        report.append("BEFORE vs AFTER KEYWORD COMPARISON")
        report.append("=" * 80)
        
        resume_keywords = set(resume_data.get('keywords', [])[:20])
        jd_keywords = set(jd_data.get('domain_keywords', [])[:20])
        matched_before = resume_keywords & jd_keywords
        
        report.append(f"\nMatched Keywords Before: {len(matched_before)}/20")
        report.append(f"Matched Keywords After: [Run optimization to see improvement]")
        
        # Recruiter readability
        report.append("\n" + "=" * 80)
        report.append("RECRUITER READABILITY RATING")
        report.append("=" * 80)
        
        readability_score = self._calculate_readability(optimized_resume)
        report.append(f"\nReadability Score: {readability_score}/10")
        report.append("Factors: Clear structure, action verbs, quantified achievements, ATS-friendly format")
        
        return '\n'.join(report)
    
    def _calculate_readability(self, text: str) -> int:
        """Calculate recruiter readability score"""
        score = 7  # Base score
        
        # Check for action verbs
        if any(verb in text.lower() for verb in self.action_verbs):
            score += 1
        
        # Check for quantifiable achievements (numbers)
        if re.search(r'\d+%|\d+\+', text):
            score += 1
        
        # Check for clear structure
        if all(section in text.upper() for section in ['SUMMARY', 'EXPERIENCE', 'SKILLS']):
            score += 1
        
        return min(score, 10)


def main():
    """Main function for testing"""
    print("ATS Resume Scoring and Optimization Engine")
    print("=" * 80)
    print("\nThis engine helps you:")
    print("1. Calculate ATS compatibility score (0-100)")
    print("2. Identify gaps between your resume and job requirements")
    print("3. Get actionable improvement suggestions")
    print("4. Generate an ATS-optimized resume")
    print("\nReady to use!")


if __name__ == "__main__":
    main()
