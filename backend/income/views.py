from .models import Income
from .serializers import IncomeSerializer
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import render, redirect
from django.conf import settings
from mindee import Client, documents
from django.contrib.auth.decorators import login_required
from .forms import DocUploadForm
import csv
from django.contrib import messages

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        query_set = self.queryset
        return query_set.filter(user=user)


class IncomeReceiptUpload(viewsets.ModelViewSet):

    def success_view(request):
        return render(request, 'success.html') #will configure this after frontend is ready

    @login_required
    def upload_income_receipt(request):
        if request.method == 'POST':
            form = DocUploadForm(request.POST, request.FILES)
            if form.is_valid():
                receipt_image = request.FILES['receipt_image'] #will configure this after frontend is ready
                if not receipt_image.content_type.startswith('image/'):
                    messages.error(request, "Invalid file type. Please upload an image.")
                    return render(request, 'upload_income_receipt.html', {'form': form})

                try:
                    process_mindee_api_for_income(receipt_image, request)
                except Exception as e:
                    messages.error(request, f"Error with Mindee API: {e}")
                    return render(request, 'upload_income_receipt.html', {'form': form})

                return redirect('success_view')

        else:
            form = DocUploadForm()

        return render(request, 'upload_income_receipt.html', {'form': form})


def process_mindee_api_for_income(receipt_image, request):
    mindee_client = Client(api_key=settings.MINDEE_API_KEY)
    input_doc = mindee_client.doc_from_file(receipt_image)
    result = input_doc.parse(documents.TypeInvoiceV4)

    invoice = result.document

    supplier_name = invoice.supplier_name if hasattr(invoice, 'supplier_name') else None
    invoice_date = invoice.invoice_date if hasattr(invoice, 'invoice_date') else None
    total_amount = invoice.total_amount if hasattr(invoice, 'total_amount') else None

    try:
        write_to_income_csv(request.user.username, supplier_name, invoice_date, total_amount)
    except Exception as e:
        raise Exception(f"Error writing to CSV: {e}")


def write_to_income_csv(username, supplier_name, invoice_date, total_amount):
    with open(settings.CSV_FILE_income, 'a', newline='') as csvfile:
        fieldnames = ['user', 'supplier_name', 'invoice_date', 'total_amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'user': username,
            'income_source': supplier_name,
            'date': invoice_date,
            'amount': total_amount
        })

