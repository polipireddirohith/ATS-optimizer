"""
PDF Generator for ATS Resume Analyzer
Generates professional PDF reports and resumes
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import KeepTogether, ListFlowable, ListItem
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import tempfile


class PDFGenerator:
    """Generate professional PDFs for ATS reports and resumes"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section Header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0891b2'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection Header
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#0d9488'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        ))
        
        # Score text
        self.styles.add(ParagraphStyle(
            name='ScoreText',
            parent=self.styles['Normal'],
            fontSize=48,
            textColor=colors.HexColor('#059669'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
    
    def generate_report_pdf(self, data):
        """
        Generate comprehensive ATS analysis report as PDF
        
        Args:
            data: Dictionary containing analysis results
            
        Returns:
            Path to generated PDF file
        """
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            temp_file.name,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        story = []
        
        # Title
        story.append(Paragraph("ATS Resume Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Timestamp
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<i>Generated on {timestamp}</i>", self.styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Score Section
        score_data = data.get('score', {})
        total_score = score_data.get('total_score', 0)
        
        story.append(Paragraph("Overall ATS Score", self.styles['SectionHeader']))
        story.append(Paragraph(f"{int(total_score)}", self.styles['ScoreText']))
        
        # Score interpretation
        if total_score >= 80:
            interpretation = "Excellent Match - Highly likely to pass ATS screening"
            color = colors.HexColor('#059669')
        elif total_score >= 60:
            interpretation = "Good Match - Likely to pass with minor improvements"
            color = colors.HexColor('#0891b2')
        elif total_score >= 40:
            interpretation = "Fair Match - Needs optimization to improve chances"
            color = colors.HexColor('#d97706')
        else:
            interpretation = "Needs Improvement - Significant optimization required"
            color = colors.HexColor('#dc2626')
        
        story.append(Paragraph(f'<font color="{color.hexval()}">{interpretation}</font>', self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Score Breakdown
        story.append(Paragraph("Score Breakdown", self.styles['SectionHeader']))
        breakdown = score_data.get('breakdown', {})
        
        breakdown_data = [['Category', 'Score', 'Weight']]
        for category, details in breakdown.items():
            category_name = category.replace('_', ' ').title()
            score = details.get('score', 0)
            weight = details.get('weight', 0)
            breakdown_data.append([category_name, f"{int(score)}/100", f"{int(weight * 100)}%"])
        
        breakdown_table = Table(breakdown_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0891b2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')])
        ]))
        story.append(breakdown_table)
        story.append(Spacer(1, 20))
        
        # Skills Analysis
        story.append(Paragraph("Skills Analysis", self.styles['SectionHeader']))
        skills_match = breakdown.get('skills_match', {})
        
        matched_skills = skills_match.get('matched', [])
        missing_skills = skills_match.get('missing', [])
        
        if matched_skills:
            story.append(Paragraph("Matched Skills:", self.styles['SubsectionHeader']))
            for skill in matched_skills[:10]:  # Limit to top 10
                story.append(Paragraph(f"✓ {skill}", self.styles['CustomBody']))
            story.append(Spacer(1, 10))
        
        if missing_skills:
            story.append(Paragraph("Missing Skills:", self.styles['SubsectionHeader']))
            for skill in missing_skills[:10]:  # Limit to top 10
                story.append(Paragraph(f"✗ {skill}", self.styles['CustomBody']))
            story.append(Spacer(1, 20))
        
        # Suitability Assessment
        suitability = data.get('suitability', {})
        if suitability:
            story.append(PageBreak())
            story.append(Paragraph("Suitability Assessment", self.styles['SectionHeader']))
            
            verdict = suitability.get('verdict', '')
            recommendation = suitability.get('recommendation', '')
            
            story.append(Paragraph(f"<b>Verdict:</b> {verdict}", self.styles['CustomBody']))
            story.append(Paragraph(f"<b>Recommendation:</b> {recommendation}", self.styles['CustomBody']))
            story.append(Spacer(1, 15))
            
            # Recruiter Insights
            insights = suitability.get('recruiter_insights', [])
            if insights:
                story.append(Paragraph("Key Insights:", self.styles['SubsectionHeader']))
                for insight in insights:
                    story.append(Paragraph(f"• {insight}", self.styles['CustomBody']))
                story.append(Spacer(1, 15))
        
        # Improvements Section
        improvements = data.get('improvements', {})
        if improvements:
            story.append(Paragraph("Recommended Improvements", self.styles['SectionHeader']))
            
            keyword_insertions = improvements.get('keyword_insertions', [])
            if keyword_insertions:
                story.append(Paragraph("Keyword Suggestions:", self.styles['SubsectionHeader']))
                for item in keyword_insertions[:5]:
                    keyword = item.get('keyword', '')
                    suggestion = item.get('suggestion', '')
                    story.append(Paragraph(f"<b>{keyword}:</b> {suggestion}", self.styles['CustomBody']))
                story.append(Spacer(1, 10))
            
            bullet_rewrites = improvements.get('bullet_point_rewrites', [])
            if bullet_rewrites:
                story.append(Paragraph("Bullet Point Enhancements:", self.styles['SubsectionHeader']))
                for item in bullet_rewrites[:3]:
                    suggestion = item.get('suggestion', '')
                    story.append(Paragraph(f"• {suggestion}", self.styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        
        return temp_file.name
    
    def generate_resume_pdf(self, resume_text):
        """
        Generate optimized resume as PDF
        
        Args:
            resume_text: String containing resume content
            
        Returns:
            Path to generated PDF file
        """
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            temp_file.name,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=50,
            bottomMargin=50
        )
        
        # Container for PDF elements
        story = []
        
        # Process resume text
        lines = resume_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 8))
                continue
            
            # Detect headers (all caps or specific patterns)
            if line.isupper() and len(line) < 50:
                story.append(Paragraph(line, self.styles['SectionHeader']))
            elif line.startswith('•') or line.startswith('-'):
                # Bullet points
                story.append(Paragraph(line, self.styles['CustomBody']))
            else:
                # Regular text
                story.append(Paragraph(line, self.styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        
        return temp_file.name
