"""
ATS Resume Scorer - Web Application

A beautiful, modern web interface for the ATS Resume Scoring Engine
Built with Flask for the backend and vanilla HTML/CSS/JS for the frontend
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import json
from datetime import datetime

from ats_engine import ATSEngine
from document_parser import DocumentParser
from pdf_generator import PDFGenerator


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Initialize ATS components
ats_engine = ATSEngine()
doc_parser = DocumentParser()
pdf_generator = PDFGenerator()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


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


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 80)
    print("ATS Resume Scoring & Optimization Engine - Web Interface")
    print("=" * 80)
    print("\nStarting server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
