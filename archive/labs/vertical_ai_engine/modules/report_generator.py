from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import uuid

def generate_pdf_report(data: dict, output_dir='output/reports', template_dir='templates'):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')
    
    html_out = template.render(data)
    filename = f"report_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    HTML(string=html_out).write_pdf(output_path)
    return output_path
