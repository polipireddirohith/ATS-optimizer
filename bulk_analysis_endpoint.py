"""
Bulk Resume Analysis API Endpoint

Analyzes multiple resumes against a single job description
and returns ranked comparison results
"""

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
