import sys

try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
except ImportError:
    print("Error: Missing required libraries.")
    print("Please install them using: pip install python-docx reportlab")
    sys.exit(1)

# Resume Content
resume_data = {
    "header": {
        "name": "SANJEEV RAMASAMY SEENIVASAGAMANI",
        "contact": "315-278-0599 | sanjeevsramasamy@gmail.com | linkedin.com/in/sanjeev-rs | rssanjeev.github.io"
    },
    "skills": [
        ("Languages & Scripting", "SQL, Python, PySpark, R, Bash"),
        ("Data Engineering", "Snowflake, AWS (S3, EC2, EMR, RDS, Redshift), Hive, Hadoop (HDFS)"),
        ("Transformation & Orchestration", "dbt (Data Build Tool), Prefect, Airflow"),
        ("Data Modeling", "Dimensional Modeling (Kimball), Star Schema, OLTP/OLAP, One-Big-Table (OBT)"),
        ("Visualization & Tools", "PowerBI, Tableau, Git, CI/CD (CircleCI), JIRA, Agile/Scrum")
    ],
    "experience": [
        {
            "company": "KAGR", "location": "Foxborough, MA (Remote)",
            "title": "Data Engineer III", "date": "Jul 2023 – Present",
            "bullets": [
                "Architected a high-scale ticketing data model unifying records for 1,100 schools and 500,000 college athletes, acting as the single source of truth for cross-client analytics.",
                "Optimized historical seat-level transaction pipelines by refactoring FACT table logic, reducing processing runtime by 75% and significantly lowering compute costs.",
                "Developed a cross-client internal Python package utilizing Prefect for event-based orchestration, reducing manual intervention and cutting average pipeline runtime by 30%.",
                "Led the migration of legacy SQL procedures to modular dbt models, improving code reusability and reducing deployment failures."
            ]
        },
        {
            "company": "Klearnow.AI", "location": "Santa Clara, CA",
            "title": "Senior Data Engineer", "date": "Nov 2022 – May 2023",
            "bullets": [
                "Led the re-design of a PySpark ingestion pipeline processing high-volume shipment data into a Redshift One-Big-Table (OBT) architecture via multi-node AWS EMR clusters.",
                "Slashed shipment tracking dashboard latency from 48 minutes to 17 minutes by optimizing Spark transformations and resolving bottlenecks in the critical path.",
                "Reduced Data Warehouse CPU utilization by 22% through the implementation of materialized views and upstream data validation frameworks (Great Expectations), eliminating data redundancy.",
                "Built a Python-based extraction pipeline for the HubSpot API to aggregate customer interactions (contacts, emails, calls), contributing to an 18% increase in customer retention through improved analytics."
            ]
        },
        {
            "company": "AstraZeneca", "location": "Gaithersburg, MD",
            "title": "Data Engineer", "date": "Nov 2020 – Nov 2022",
            "bullets": [
                "Engineered an end-to-end ETL pipeline on AWS (EC2, S3) to ingest global rare disease clinical trial data, enabling R&D teams to accelerate drug development lifecycles.",
                "Migrated petabyte-scale patient data from legacy on-prem systems to Snowflake, feeding Qlik dashboards that expanded patient recruitment capabilities by 40%.",
                "Spearheaded data integrity initiatives by implementing automated anomaly detection scripts, ensuring 99.9% accuracy for FDA-compliant reporting.",
                "Designed dimensional data models to predict clinical trial deviations, integrating disparate data sources to support advanced predictive analytics."
            ]
        },
        {
            "company": "Marathon Energy", "location": "Syracuse, NY",
            "title": "Data Analytics Intern", "date": "May 2019 – Dec 2019",
            "bullets": [
                "Developed Python-Selenium web scrapers to automate data extraction from utility portals (National Grid), fueling PowerBI dashboards for the revenue team.",
                "Improved data refresh rates by 94% (from weekly to near real-time), enabling the sales team to react instantly to market rate changes."
            ]
        },
        {
            "company": "Latentview Analytics", "location": "Chennai, India",
            "title": "Data Analyst", "date": "Jan 2018 – July 2018",
            "bullets": [
                "Partnered with the Data Science team to analyze quarterly customer conversion rates, proposing strategy adjustments that increased sales and retention by 12%.",
                "Executed end-to-end descriptive analysis on website traffic data to optimize ad placement strategies for high-value e-commerce clients."
            ]
        },
        {
            "company": "Cognizant Technology Solutions", "location": "Chennai, India",
            "title": "Data Engineer", "date": "Aug 2014 – Jan 2018",
            "bullets": [
                "Led a cross-functional team in optimizing international transaction data processing using Hadoop ecosystem tools to enhance regulatory compliance.",
                "Reduced service downtime by 85 minutes per day by implementing a distributed caching system for HDFS, accelerating daily foreign exchange data availability."
            ]
        }
    ],
    "education": [
        ("Master of Science, Applied Data Science", "Syracuse University", "2020"),
        ("Bachelor of Engineering, Electrical & Electronics Engineering", "Anna University", "2014")
    ]
}

def create_docx(data):
    doc = Document()
    
    # Normal Style
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    # --- Header ---
    h1 = doc.add_heading(data['header']['name'], 0)
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    contact_p = doc.add_paragraph(data['header']['contact'])
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # --- Skills ---
    doc.add_heading('TECHNICAL SKILLS', level=1)
    for cat, skills in data['skills']:
        p = doc.add_paragraph()
        p.style = 'Normal'
        runner = p.add_run(f"{cat}: ")
        runner.bold = True
        p.add_run(skills)
        
    # --- Experience ---
    doc.add_heading('PROFESSIONAL EXPERIENCE', level=1)
    for job in data['experience']:
        # Company Line
        p1 = doc.add_paragraph()
        r1 = p1.add_run(job['company'])
        r1.bold = True
        r1.font.size = Pt(12)
        p1.add_run(f" | {job['location']}")
        
        # Title Line
        p2 = doc.add_paragraph()
        r2 = p2.add_run(job['title'])
        r2.bold = True
        r2.italic = True
        p2.add_run(f" | {job['date']}")
        
        # Bullets
        for bullet in job['bullets']:
            p_bullet = doc.add_paragraph(bullet, style='List Bullet')

    # --- Education ---
    doc.add_heading('EDUCATION', level=1)
    for deg, school, year in data['education']:
        p = doc.add_paragraph()
        r = p.add_run(deg)
        r.bold = True
        p.add_run(f" | {school} ({year})")
        
    doc.save('Sanjeev_Ramasamy_Resume.docx')
    print("DOCX generated.")

def create_pdf(data):
    doc = SimpleDocTemplate("Sanjeev_Ramasamy_Resume.pdf", pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    # Custom Styles
    title_style = ParagraphStyle('Title', parent=styles['Normal'], alignment=TA_CENTER, fontSize=16, spaceAfter=6, fontName='Helvetica-Bold')
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, spaceAfter=12)
    
    # Section Header Style
    h1_style = ParagraphStyle('Heading1Custom', parent=styles['Heading1'], fontSize=12, spaceBefore=12, spaceAfter=6, 
                              textTransform='uppercase', borderPadding=0, textColor=colors.black)

    # Content Styles
    skill_style = ParagraphStyle('Skill', parent=styles['Normal'], fontSize=10, spaceAfter=3, leading=12)
    job_header_style = ParagraphStyle('JobHeader', parent=styles['Normal'], fontSize=11, spaceAfter=1, leading=13)
    job_subheader_style = ParagraphStyle('JobSubHeader', parent=styles['Normal'], fontSize=11, spaceAfter=2, fontName='Helvetica-Oblique', leading=13)
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=10, leading=12)

    # --- Content Construction ---
    
    # Header
    story.append(Paragraph(data['header']['name'], title_style))
    story.append(Paragraph(data['header']['contact'], contact_style))
    
    # Skills
    story.append(Paragraph("<b>TECHNICAL SKILLS</b>", h1_style))
    story.append(Spacer(1, 2))
    for cat, skills in data['skills']:
        text = f"<b>{cat}:</b> {skills}"
        story.append(Paragraph(text, skill_style))
    
    story.append(Spacer(1, 8))

    # Experience
    story.append(Paragraph("<b>PROFESSIONAL EXPERIENCE</b>", h1_style))
    story.append(Spacer(1, 2))
    
    for job in data['experience']:
        # Company
        story.append(Paragraph(f"<b>{job['company']}</b> | {job['location']}", job_header_style))
        # Title
        story.append(Paragraph(f"<b>{job['title']}</b> | {job['date']}", job_subheader_style))
        
        # Bullets
        bullets = []
        for b in job['bullets']:
            bullets.append(ListItem(Paragraph(b, bullet_style), bulletColor=colors.black, value='circle'))
        
        story.append(ListFlowable(bullets, bulletType='bullet', start='circle', leftIndent=12, bulletOffsetY=-1))
        story.append(Spacer(1, 8))

    # Education
    story.append(Paragraph("<b>EDUCATION</b>", h1_style))
    story.append(Spacer(1, 2))
    for deg, school, year in data['education']:
        story.append(Paragraph(f"<b>{deg}</b> | {school} ({year})", skill_style))

    doc.build(story)
    print("PDF generated.")

if __name__ == "__main__":
    create_docx(resume_data)
    create_pdf(resume_data)
    print("\nSuccess! Files 'Sanjeev_Ramasamy_Resume.docx' and 'Sanjeev_Ramasamy_Resume.pdf' created.")