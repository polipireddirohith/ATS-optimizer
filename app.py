"""
ATS Resume Scorer - Web Application

A beautiful, modern web interface for the ATS Resume Scoring Engine
Built with Flask for the backend and vanilla HTML/CSS/JS for the frontend
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import re
import urllib.parse
try:
    import requests
except ImportError:
    requests = None
import tempfile
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
# TODO: Replace with actual SMTP credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "your-company-email@gmail.com" 
SMTP_PASSWORD = "your-app-password"

def send_shortlist_notification(candidate_email, candidate_name):
    """Send an email notification to the shortlisted candidate"""
    # Check if credentials are set (simple validation)
    if "your-company-email" in SMTP_EMAIL:
        print(f"[MOCK EMAIL] To: {candidate_email}\nSubject: Shortlisted\nBody: Dear {candidate_name}, You have been shortlisted! (Configure SMTP in app.py to send real emails)")
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = candidate_email
        msg['Subject'] = "Update on your Application: Shortlisted"

        body = f"""
Dear {candidate_name},

We are pleased to inform you that your application has been shortlisted by our recruitment team.
Your skills and experience align well with our requirements.

Our team will contact you shortly regarding the next steps in the hiring process.

Best regards,
Talent Acquisition Team
(Sent via ATS Optimizer)
        """
        msg.attach(MIMEText(body, 'plain'))

        # Connect to server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(SMTP_EMAIL, candidate_email, text)
        server.quit()
        
        print(f"Email sent successfully to {candidate_email}")
        return True
    
    except Exception as e:
        print(f"Failed to send email to {candidate_email}: {str(e)}")
        return False


from ats_engine import ATSEngine
from document_parser import DocumentParser
from pdf_generator import PDFGenerator
from shortlist_manager import ShortlistManager


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Initialize ATS components
ats_engine = ATSEngine()
doc_parser = DocumentParser()
pdf_generator = PDFGenerator()
shortlist_manager = ShortlistManager()


ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.context_processor
def inject_user():
    """Inject user identity from headers or query params for portal integration"""
    # Check headers (typical for enterprise SSO/Gateway)
    user = request.headers.get('X-User-Name') or request.headers.get('X-Remote-User')
    # Fallback to query params for simple embedding (e.g. iframe?user=John)
    if not user:
        user = request.args.get('user')
    
    role = request.headers.get('X-User-Role') or request.args.get('role')
    
    return dict(current_user=user, current_role=role)


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/bulk')
def bulk_analysis():
    """Render bulk analysis page"""
    return render_template('bulk.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze resume against job description
    
    Expected form data:
    - resume_file: Resume file (PDF/DOCX/TXT)
    - jd_text: Job description text
    """
    try:
        # Validate inputs
        if 'resume_file' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        if 'jd_text' not in request.form:
            return jsonify({'error': 'No job description provided'}), 400
        
        resume_file = request.files['resume_file']
        jd_text = request.form['jd_text']
        
        if resume_file.filename == '':
            return jsonify({'error': 'No resume file selected'}), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        if not jd_text.strip():
            return jsonify({'error': 'Job description cannot be empty'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(filepath)
        
        try:
            # Parse resume
            resume_text = doc_parser.parse_file(filepath)
            
            # Parse resume data
            resume_data = ats_engine.parse_resume(resume_text)
            
            # Analyze job description
            jd_data = ats_engine.analyze_job_description(jd_text)
            
            # Calculate score
            score_data = ats_engine.calculate_ats_score(resume_data, jd_data)
            
            # Perform gap analysis
            gaps = ats_engine.perform_gap_analysis(resume_data, jd_data)
            
            # Calculate suitability for HR
            suitability = ats_engine.calculate_suitability(score_data, resume_data, jd_data)
            
            # Generate improvements
            improvements = ats_engine.generate_improvements(resume_data, jd_data, gaps)
            
            # Generate optimized resume
            optimized_resume = ats_engine.optimize_resume(resume_data, jd_data, improvements)
            
            # Prepare response
            response = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'score': score_data,
                'suitability': suitability,
                'resume_data': resume_data,
                'jd_data': jd_data,
                'gaps': gaps,
                'improvements': improvements,
                'optimized_resume': optimized_resume
            }
            
            return jsonify(response)
        
        finally:
            # Clean up temporary file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/api/download-resume', methods=['POST'])
def download_resume():
    """Download optimized resume as PDF"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        
        if not resume_text:
            return jsonify({'error': 'No resume text provided'}), 400
        
        # Generate PDF
        pdf_path = pdf_generator.generate_resume_pdf(resume_text)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f'Optimized_Resume_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


@app.route('/api/download-report', methods=['POST'])
def download_report():
    """Download full ATS report as PDF"""
    try:
        data = request.get_json()
        
        # Generate PDF report
        pdf_path = pdf_generator.generate_report_pdf(data)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f'ATS_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


@app.route('/api/bulk-analyze', methods=['POST'])
def bulk_analyze_resumes():
    """
    Analyze multiple resumes against a single job description
    
    Expected form data:
    - resume_files: Multiple resume files (PDF/DOCX/TXT)
    - jd_text: Job description text
    
    Returns:
    - Ranked list of candidates with scores and comparisons
    """
    try:
        # Validate inputs
        if 'resume_files' not in request.files:
            return jsonify({'error': 'No resume files provided'}), 400
        
        if 'jd_text' not in request.form:
            return jsonify({'error': 'No job description provided'}), 400
        
        resume_files = request.files.getlist('resume_files')
        jd_text = request.form['jd_text']
        
        if not resume_files or len(resume_files) == 0:
            return jsonify({'error': 'No resume files selected'}), 400
        
        if not jd_text.strip():
            return jsonify({'error': 'Job description cannot be empty'}), 400
        
        # Analyze job description once (same for all candidates)
        jd_data = ats_engine.analyze_job_description(jd_text)
        jd_experience = ats_engine.extract_years_of_experience(jd_text)
        
        # Process each resume
        results = []
        for idx, resume_file in enumerate(resume_files):
            if resume_file.filename == '':
                continue
                
            if not allowed_file(resume_file.filename):
                results.append({
                    'filename': resume_file.filename,
                    'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}',
                    'status': 'failed'
                })
                continue
            
            try:
                # Save file temporarily
                filename = secure_filename(resume_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'bulk_{idx}_{filename}')
                resume_file.save(filepath)
                
                # Parse resume
                resume_text = doc_parser.parse_file(filepath)
                resume_experience = ats_engine.extract_years_of_experience(resume_text[:2000]) # Scan first 2000 chars for summary
                resume_data = ats_engine.parse_resume(resume_text)
                
                # Calculate scores
                score_data = ats_engine.calculate_ats_score(resume_data, jd_data)
                suitability = ats_engine.calculate_suitability(score_data, resume_data, jd_data)
                gaps = ats_engine.perform_gap_analysis(resume_data, jd_data)
                
                # Compile result
                results.append({
                    'filename': filename,
                    'candidate_name': resume_data['contact_info']['name'],
                    'email': resume_data['contact_info']['email'],
                    'phone': resume_data['contact_info']['phone'],
                    'total_score': score_data['total_score'],
                    'verdict': suitability['verdict'],
                    'verdict_color': suitability['color'],
                    'recommendation': suitability['recommendation'],
                    'visibility_status': score_data['visibility_status'],
                    'matched_skills': suitability['matched_skills'],
                    'missing_skills': suitability['missing_skills'],
                    'education_match': suitability['education_match'],
                    'education_required': suitability['education_required'],
                    'resume_education': suitability['resume_education'],
                    'matched_certifications': suitability['matched_certifications'],
                    'missing_certifications': suitability['missing_certifications'],
                    'experience_summary': suitability['experience_summary'],
                    'breakdown': score_data['breakdown'],
                    'jd_experience': jd_experience,
                    'resume_experience': resume_experience,
                    'status': 'success'
                })
                
                # Clean up temp file
                try:
                    os.remove(filepath)
                except:
                    pass
                    
            except Exception as e:
                results.append({
                    'filename': resume_file.filename,
                    'error': str(e),
                    'status': 'failed'
                })
        
        # Sort by score (highest first)
        successful_results = [r for r in results if r['status'] == 'success']
        failed_results = [r for r in results if r['status'] == 'failed']
        
        successful_results.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Add rank to successful results
        for idx, result in enumerate(successful_results):
            result['rank'] = idx + 1
        
        return jsonify({
            'success': True,
            'total_processed': len(resume_files),
            'successful': len(successful_results),
            'failed': len(failed_results),
            'jd_data': {
                'mandatory_skills': jd_data['mandatory_skills'],
                'preferred_skills': jd_data['preferred_skills'],
                'experience_required': jd_data['experience_required'],
                'required_certifications': jd_data['required_certifications'],
                'education_required': jd_data['education_required']
            },
            'candidates': successful_results,
            'failed_files': failed_results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Shortlist Management Endpoints
@app.route('/api/shortlist/add', methods=['POST'])
def add_to_shortlist():
    """Add a candidate to the shortlist and send notification email"""
    try:
        data = request.get_json()
        result = shortlist_manager.add_candidate(data)
        
        # Send Email Notification if successfully added
        if result.get('success'):
            candidate_name = data.get('candidate_name', 'Candidate')
            email = data.get('email')
            
            if email:
                email_sent = send_shortlist_notification(email, candidate_name)
                result['email_sent'] = email_sent
                if email_sent:
                    result['message'] += " (Email sent to candidate)"
            else:
                 result['message'] += " (No email found for notification)"
                 
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/shortlist/remove', methods=['POST'])
def remove_from_shortlist():
    """Remove a candidate from the shortlist"""
    try:
        data = request.get_json()
        email = data.get('email')
        result = shortlist_manager.remove_candidate(email)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/shortlist/all', methods=['GET'])
def get_all_shortlisted():
    """Get all shortlisted candidates"""
    try:
        candidates = shortlist_manager.get_all_shortlisted()
        return jsonify({
            'success': True,
            'candidates': candidates,
            'total': len(candidates)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/shortlist/check/<email>', methods=['GET'])
def check_shortlist_status(email):
    """Check if a candidate is shortlisted"""
    try:
        candidate = shortlist_manager.get_by_email(email)
        return jsonify({
            'success': True,
            'is_shortlisted': bool(candidate),
            'candidate': candidate
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/shortlist/update-status', methods=['POST'])
def update_shortlist_status():
    """Update candidate status"""
    try:
        data = request.get_json()
        email = data.get('email')
        status = data.get('status')
        result = shortlist_manager.update_status(email, status)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/shortlist/add-note', methods=['POST'])
def add_shortlist_note():
    """Add a note to a shortlisted candidate"""
    try:
        data = request.get_json()
        email = data.get('email')
        note = data.get('note')
        result = shortlist_manager.add_note(email, note)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/shortlist/statistics', methods=['GET'])
def get_shortlist_statistics():
    """Get shortlist statistics"""
    try:
        stats = shortlist_manager.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/shortlist')
def view_shortlist():
    """Render shortlist page"""
    return render_template('shortlist.html')


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error"""
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/source')
def sourcing_page():
    """Render sourcing page"""
    return render_template('sourcing.html')


@app.route('/api/source/generate', methods=['POST'])
def generate_sourcing():
    """Generate sourcing strategies from JD"""
    try:
        data = request.get_json()
        jd_text = data.get('jd_text', '')
        
        # Keyword extraction using global re
        words = re.findall(r'\b[A-Z][a-zA-Z]+\b', jd_text)
        common = {'The', 'And', 'For', 'With', 'Job', 'Description', 'We', 'Are', 'You', 'Will', 'Work', 'Team', 'Role', 'This', 'Our', 'To', 'In', 'Of', 'Is', 'Be', 'Or', 'As', 'An', 'At', 'By', 'On', 'It', 'If'}
        keywords = [w for w in words if w not in common and len(w) > 3]
        unique_keywords = sorted(list(set(keywords)), key=lambda x: keywords.count(x), reverse=True)[:5]
        
        if not unique_keywords:
            unique_keywords = ['Developer', 'Engineer', 'Software']
            
        keyword_str = " ".join([f'"{k}"' for k in unique_keywords])
        
        links = []
        platforms = [
            ('LinkedIn', f'site:linkedin.com/in/ {keyword_str}'),
            ('GitHub', f'site:github.com {keyword_str}'),
            ('Naukri', f'site:naukri.com {keyword_str}'),
            ('StackOverflow', f'site:stackoverflow.com/users {keyword_str}')
        ]
        
        for p, q in platforms:
            url = f"https://www.google.com/search?q={urllib.parse.quote(q)}"
            links.append({'platform': p, 'query': q, 'url': url})
            
        # Real Search via Google API (if keys provided)
        api_key = data.get('api_key')
        cx_id = data.get('cx_id')
        candidates_list = []
        
        if api_key and cx_id:
            if requests:
                try:
                    # Targeted Query for LinkedIn Profiles
                    search_query = f'site:linkedin.com/in/ {keyword_str}'
                    # Use params for safer encoding
                    params = {
                        'key': api_key,
                        'cx': cx_id,
                        'q': search_query
                    }
                    resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=5)
                    
                    if resp.status_code == 200:
                        results = resp.json().get('items', [])
                        for item in results[:5]:
                            title = item.get('title', 'Unknown Professional')
                            parts = title.split(' - ')
                            name = parts[0].strip()
                            role = parts[1] if len(parts) > 1 else 'Professional'
                            if '|' in role: role = role.split('|')[0].strip()
                            
                            candidates_list.append({
                                'name': name,
                                'title': role,
                                'match_score': 85 + (len(results) - results.index(item)),
                                'skills': unique_keywords[:3],
                                'profile_url': item.get('link')
                            })
                    else:
                        print(f"Google API Error: {resp.status_code} - {resp.text}")
                except Exception as e:
                    print(f"Google API Exception: {str(e)}")
            else:
                print("Warning: 'requests' module not installed. Skipping Google API call.")

        return jsonify({'success': True, 'links': links, 'mock_candidates': candidates_list})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 80)
    print("ATS Resume Scoring & Optimization Engine - Web Interface")
    print("=" * 80)
    print("\nStarting server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
