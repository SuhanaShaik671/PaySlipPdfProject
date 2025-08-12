from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
import os

def PayslipPDFView(request):
    # Logo absolute path
    logo_path = os.path.abspath('pdfapp/static/logo.jpg')
    logo_url = 'file:///' + logo_path.replace('\\', '/')

    # Earnings & Deductions data
    earnings = [
        ("Basic", 100869.00),
        ("House Rent Allowance", 40348.00),
        ("Flexible Benefit Plan", 60520.00),
    ]
    deductions = [
        ("EPF Contribution", 1800.00),
        ("Income Tax", 36120.00),
        ("Professional Tax", 200.00),
    ]

    # Calculations
    gross_earnings_val = sum(e[1] for e in earnings)
    total_deductions_val = sum(d[1] for d in deductions)
    net_pay_val = gross_earnings_val - total_deductions_val

    # Format as Rs.
    def rs(amount):
        return f"Rs.{amount:,.2f}"

    # Dynamic context
    context = {
        'logo_path': logo_url,
        'company_name': "FYERS Securities Private Limited",
        'company_address': "A-901 & A-902, 9th Floor A wing, Brigade Magnum, Kodige Halli Cross, Amrutha Halli, International Airport Road, Bangalore Karnataka 560032 India",
        'payslip_month': "October 2023",
        'employee_name': "Rajasekhar Varikuti",
        'employee_code': "EM353",
        'designation': "Technical Lead Engineer",
        'doj': "21/12/2020",
        'pay_period': "October 2023",
        'pay_date': "01/11/2023",
        'pf_number': "BG/BNG/1960351/000/0010188",
        'uan': "101526255716",
        'pan': "AXKPV5382P",
        'bank_account': "45711749753",
        'paid_days': "31",
        'lop_days': "0",

        # Earnings & Deductions (formatted for display)
        'earnings': [(name, rs(amount)) for name, amount in earnings],
        'deductions': [(name, rs(amount)) for name, amount in deductions],

        # Totals (formatted for display)
        'gross_earnings': rs(gross_earnings_val),
        'total_deductions': rs(total_deductions_val),
        'net_pay': rs(net_pay_val),

        # Words
        'net_pay_words': "Indian Rupee One Lakh Sixty-Three Thousand Six Hundred Seventeen Only",
        'net_pay_formula': "Total Net Pay = Gross Earnings - Total Deductions",
    }

    # Align earnings & deductions for table rows
    max_rows = max(len(context['earnings']), len(context['deductions']))
    earnings_padded = context['earnings'] + [("", "")] * (max_rows - len(context['earnings']))
    deductions_padded = context['deductions'] + [("", "")] * (max_rows - len(context['deductions']))
    context['rows'] = list(zip(earnings_padded, deductions_padded))

    # Render HTML
    html = render_to_string('payslip.html', context)

    # PDF config
    config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Users\suhan\Downloads\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe'
    )
    options = {'enable-local-file-access': ''}

    pdf = pdfkit.from_string(html, False, configuration=config, options=options)

    # Response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="payslip_october_2023.pdf"'
    return response
