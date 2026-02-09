"""
Test script to verify PDF generation functionality
"""

from pdf_generator import PDFGenerator
import json

# Initialize PDF generator
pdf_gen = PDFGenerator()

# Test data for report generation
test_data = {
    'score': {
        'total_score': 78,
        'breakdown': {
            'skills_match': {
                'score': 85,
                'weight': 0.4,
                'matched': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL'],
                'missing': ['AWS', 'Docker', 'Kubernetes']
            },
            'experience_match': {
                'score': 75,
                'weight': 0.3
            },
            'education_match': {
                'score': 70,
                'weight': 0.2
            },
            'formatting': {
                'score': 80,
                'weight': 0.1
            }
        }
    },
    'suitability': {
        'verdict': 'Strong Candidate',
        'recommendation': 'Highly recommended for interview',
        'recruiter_insights': [
            'Strong technical skills match',
            'Relevant industry experience',
            'Good educational background'
        ],
        'matched_skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL'],
        'missing_skills': ['AWS', 'Docker', 'Kubernetes'],
        'experience_summary': [
            'Led development of web applications using React and Node.js',
            'Implemented RESTful APIs and database optimization',
            'Collaborated with cross-functional teams'
        ]
    },
    'improvements': {
        'keyword_insertions': [
            {
                'keyword': 'AWS',
                'suggestion': 'Add AWS experience in cloud projects section'
            },
            {
                'keyword': 'Docker',
                'suggestion': 'Mention containerization experience with Docker'
            }
        ],
        'bullet_point_rewrites': [
            {
                'suggestion': 'Developed scalable web applications serving 100K+ users using React and Node.js'
            },
            {
                'suggestion': 'Optimized database queries resulting in 40% performance improvement'
            }
        ]
    }
}

# Test resume text
test_resume = """JOHN DOE
Software Engineer

CONTACT INFORMATION
Email: john.doe@email.com
Phone: (555) 123-4567
Location: San Francisco, CA

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years of expertise in full-stack development.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, TypeScript
• Frameworks: React, Node.js, Express
• Databases: PostgreSQL, MongoDB, Redis
• Tools: Git, VS Code, Postman

WORK EXPERIENCE

Senior Software Engineer | Tech Company Inc.
January 2020 - Present
• Led development of customer-facing web applications
• Implemented RESTful APIs serving 100K+ daily users
• Optimized database performance by 40%
• Mentored junior developers

Software Engineer | Startup Co.
June 2018 - December 2019
• Developed features for SaaS platform
• Collaborated with product team on requirements
• Wrote comprehensive unit and integration tests

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley
Graduated: 2018
"""

print("=" * 80)
print("Testing PDF Generation")
print("=" * 80)

# Test 1: Generate Report PDF
print("\n1. Generating ATS Report PDF...")
try:
    report_pdf_path = pdf_gen.generate_report_pdf(test_data)
    print(f"[SUCCESS] Report PDF generated successfully: {report_pdf_path}")
except Exception as e:
    print(f"[ERROR] Error generating report PDF: {e}")

# Test 2: Generate Resume PDF
print("\n2. Generating Optimized Resume PDF...")
try:
    resume_pdf_path = pdf_gen.generate_resume_pdf(test_resume)
    print(f"[SUCCESS] Resume PDF generated successfully: {resume_pdf_path}")
except Exception as e:
    print(f"[ERROR] Error generating resume PDF: {e}")

print("\n" + "=" * 80)
print("PDF Generation Test Complete!")
print("=" * 80)
print("\nYou can now test the download functionality in the web application.")
print("The PDFs will be automatically generated when you click the download buttons.")
