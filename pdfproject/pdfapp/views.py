from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
import os

def PayslipPDFView(request):
    # ✅ Path to logo image
    logo_path = os.path.abspath('pdfapp/static/logo.jpg')
    logo_url = 'file:///' + logo_path.replace('\\', '/')

    # ✅ Render HTML with logo path
    html = render_to_string('payslip.html', {
        'logo_path': logo_url,
    })

    # ✅ Path to wkhtmltopdf
    config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Users\suhan\Downloads\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe'
    )

    # ✅ Add this option to allow local file access
    options = {
        'enable-local-file-access': ''
    }

    # ✅ Generate PDF
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)

    # ✅ Return PDF in browser
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="payslip_october_2023.pdf"'
    return response
