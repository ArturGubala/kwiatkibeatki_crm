from flask import render_template
from weasyprint import HTML


from html_to_pdf_converter import HTMLToPDFConverter
from file_saver import FileSaver


class PDFGenerator:
    def __init__(self):
        self.html_to_pdf_converter = HTMLToPDFConverter()
        self.file_saver = FileSaver()
        self.template_name = "invoice.html"

    def execute(self, data: dict) -> None:
        rendered_template = render_template(self.template_name, data=data)

        html = HTML(string=rendered_template)
        generated_pdf = html.write_pdf()

        pdf_name = f"{data['document']['number']}.pdf"
        with open(f'/queue/pdfs/{data["document"]["number"]}.pdf', 'wb') as f:
            f.write(generated_pdf)
            return f"http://127.0.0.1:5004/pdfs/{pdf_name}"
