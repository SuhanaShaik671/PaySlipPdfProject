from django.urls import path
from .views import PayslipPDFView

urlpatterns = [
    path('generate-payslip/', PayslipPDFView, name='generate_payslip'),
]
