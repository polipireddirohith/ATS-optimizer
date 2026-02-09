"""
ATS Resume Scorer - Command Line Interface

Usage:
    python ats_cli.py --resume <resume_file> --jd <jd_file_or_text>
    python ats_cli.py --resume resume.pdf --jd job_description.txt
    python ats_cli.py --resume resume.docx --jd "Job description text here"
"""

import argparse
import os
import sys
from ats_engine import ATSEngine
from document_parser import DocumentParser


def main():
    parser = argparse.ArgumentParser(
        description='ATS Resume Scoring and Optimization Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ats_cli.py --resume resume.pdf --jd job_description.txt
  python ats_cli.py --resume resume.docx --jd "Full job description text"
  python ats_cli.py --resume resume.txt --jd jd.txt --output report.txt
        """
    )
    
    parser.add_argument(
        '--resume',
        required=True,
        help='Path to resume file (PDF, DOCX, or TXT)'
    )
    
    parser.add_argument(
        '--jd',
        required=True,
        help='Path to job description file OR job description text'
    )
    
    parser.add_argument(
        '--output',
        default='ats_report.txt',
        help='Output file for the ATS report (default: ats_report.txt)'
    )
    
    parser.add_argument(
        '--optimized-resume',
        default='optimized_resume.txt',
        help='Output file for optimized resume (default: optimized_resume.txt)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed progress information'
    )
    
    args = parser.parse_args()
    
    # Initialize components
    if args.verbose:
        print("Initializing ATS Engine...")
    
    ats_engine = ATSEngine()
    doc_parser = DocumentParser()
    
    # Parse resume
    if args.verbose:
        print(f"\nParsing resume: {args.resume}")
    
    try:
        resume_text = doc_parser.parse_file(args.resume)
        if args.verbose:
            print(f"  ✓ Resume parsed successfully ({len(resume_text)} characters)")
    except Exception as e:
        print(f"ERROR: Failed to parse resume: {e}", file=sys.stderr)
        return 1
    
    # Parse job description
    if args.verbose:
        print(f"\nParsing job description...")
    
    if os.path.isfile(args.jd):
        try:
            jd_text = doc_parser.parse_file(args.jd)
            if args.verbose:
                print(f"  ✓ Job description parsed from file ({len(jd_text)} characters)")
        except Exception as e:
            print(f"ERROR: Failed to parse job description file: {e}", file=sys.stderr)
            return 1
    else:
        jd_text = args.jd
        if args.verbose:
            print(f"  ✓ Using provided job description text ({len(jd_text)} characters)")
    
    # Process resume
    if args.verbose:
        print("\n" + "=" * 80)
        print("STEP 1: PARSING RESUME")
        print("=" * 80)
    
    resume_data = ats_engine.parse_resume(resume_text)
    
    if args.verbose:
        print(f"  ✓ Contact Info: {resume_data['contact_info']['name']}")
        print(f"  ✓ Skills found: {len(resume_data['skills'])}")
        print(f"  ✓ Experience entries: {len(resume_data['experience'])}")
        print(f"  ✓ Keywords extracted: {len(resume_data['keywords'])}")
        if resume_data['formatting_issues']:
            print(f"  ⚠ Formatting issues detected: {len(resume_data['formatting_issues'])}")
    
    # Analyze job description
    if args.verbose:
        print("\n" + "=" * 80)
        print("STEP 2: ANALYZING JOB DESCRIPTION")
        print("=" * 80)
    
    jd_data = ats_engine.analyze_job_description(jd_text)
    
    if args.verbose:
        print(f"  ✓ Mandatory skills: {len(jd_data['mandatory_skills'])}")
        print(f"  ✓ Preferred skills: {len(jd_data['preferred_skills'])}")
        print(f"  ✓ Tools/Technologies: {len(jd_data['tools_technologies'])}")
        print(f"  ✓ Experience required: {jd_data['experience_required']}")
        print(f"  ✓ Domain keywords: {len(jd_data['domain_keywords'])}")
    
    # Calculate ATS score
    if args.verbose:
        print("\n" + "=" * 80)
        print("STEP 3: CALCULATING ATS SCORE")
        print("=" * 80)
    
    score_data = ats_engine.calculate_ats_score(resume_data, jd_data)
    
    print(f"\n{'=' * 80}")
    print(f"ATS COMPATIBILITY SCORE: {score_data['total_score']}/100")
    print(f"{'=' * 80}")
    
    if args.verbose:
        for component, data in score_data['breakdown'].items():
            print(f"  {component.replace('_', ' ').title()}: {data['score']}/100 (Weight: {data['weight']})")
    
    # Perform gap analysis
    if args.verbose:
        print("\n" + "=" * 80)
        print("STEP 4: GAP ANALYSIS")
        print("=" * 80)
    
    gaps = ats_engine.perform_gap_analysis(resume_data, jd_data)
    
    if args.verbose:
        critical_count = sum(len(items) for items in gaps['critical'].values())
        important_count = sum(len(items) for items in gaps['important'].values())
        print(f"  ✓ Critical gaps: {critical_count}")
        print(f"  ✓ Important gaps: {important_count}")
    
    # Generate improvements
    if args.verbose:
        print("\n" + "=" * 80)
        print("STEP 5: GENERATING IMPROVEMENTS")
        print("=" * 80)
    
    improvements = ats_engine.generate_improvements(resume_data, jd_data, gaps)
    
    if args.verbose:
        print(f"  ✓ Keyword insertion suggestions: {len(improvements['keyword_insertions'])}")
        print(f"  ✓ Bullet point rewrites: {len(improvements['bullet_point_rewrites'])}")
        print(f"  ✓ Formatting fixes: {len(improvements['formatting_fixes'])}")
    
    # Generate optimized resume
    if args.verbose:
        print("\n" + "=" * 80)
        print("STEP 6: GENERATING OPTIMIZED RESUME")
        print("=" * 80)
    
    optimized_resume = ats_engine.optimize_resume(resume_data, jd_data, improvements)
    
    if args.verbose:
        print(f"  ✓ Optimized resume generated ({len(optimized_resume)} characters)")
    
    # Generate report
    if args.verbose:
        print("\n" + "=" * 80)
        print("STEP 7: GENERATING REPORT")
        print("=" * 80)
    
    report = ats_engine.generate_report(
        resume_data, jd_data, score_data, gaps, improvements, optimized_resume
    )
    
    # Save outputs
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✓ Report saved to: {args.output}")
    except Exception as e:
        print(f"ERROR: Failed to save report: {e}", file=sys.stderr)
        return 1
    
    try:
        with open(args.optimized_resume, 'w', encoding='utf-8') as f:
            f.write(optimized_resume)
        print(f"✓ Optimized resume saved to: {args.optimized_resume}")
    except Exception as e:
        print(f"ERROR: Failed to save optimized resume: {e}", file=sys.stderr)
        return 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"ATS Score: {score_data['total_score']}/100")
    
    if score_data['total_score'] >= 80:
        print("Status: ✓ EXCELLENT - High chance of passing ATS")
    elif score_data['total_score'] >= 60:
        print("Status: ⚠ GOOD - Moderate chance, improvements recommended")
    else:
        print("Status: ✗ NEEDS IMPROVEMENT - Low chance, optimization required")
    
    print(f"\nFull report: {args.output}")
    print(f"Optimized resume: {args.optimized_resume}")
    print("\n" + "=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
