from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ExpenseSerializer
from .models import Expense
from django.shortcuts import render, redirect
from django.conf import settings
from mindee import Client, documents
from django.contrib.auth.decorators import login_required
from .forms import ReceiptUploadForm
import csv
from django.contrib import messages


class ExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()

    def get_queryset(self):
        user = self.request.user
        query_set = self.queryset
        return query_set.filter(user=user)

class ReceiptUpload(viewsets.ModelViewSet):

    def success_view(request):
        return render(request, 'success.html') #will configure this after frontend is ready

    @login_required
    def upload_receipt(request):
        if request.method == 'POST':
            form = ReceiptUploadForm(request.POST, request.FILES)
            if form.is_valid():
                receipt_image = request.FILES['receipt_image'] #will configure this after frontend is ready
                if not receipt_image.content_type.startswith('image/'):
                    messages.error(request, "Invalid file type. Please upload an image.")
                    return render(request, 'upload_receipt.html', {'form': form})

                try:
                    process_mindee_api(receipt_image, request)
                except Exception as e:
                    messages.error(request, f"Error with Mindee API: {e}")
                    return render(request, 'upload_receipt.html', {'form': form})

                return redirect('success_view')

        else:
            form = ReceiptUploadForm()

        return render(request, 'upload_expenses_receipt.html', {'form': form})


def process_mindee_api(receipt_image, request):
    mindee_client = Client(api_key=settings.MINDEE_API_KEY)
    input_doc = mindee_client.doc_from_file(receipt_image)
    result = input_doc.parse(documents.TypeInvoiceV4)

    invoice = result.document

    supplier_name = invoice.supplier_name if hasattr(invoice, 'supplier_name') else None
    invoice_date = invoice.invoice_date if hasattr(invoice, 'invoice_date') else None

    try:
        write_to_csv(invoice, request.user.username, supplier_name, invoice_date)
    except Exception as e:
        raise Exception(f"Error writing to CSV: {e}")


def write_to_csv(invoice, username, supplier_name, invoice_date):
    with open(settings.CSV_FILE_expenses, 'a', newline='') as csvfile:
        fieldnames = ['user', 'supplier_name', 'invoice_date', 'description', 'quantity', 'unit_price', 'total_amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        for item in invoice.line_items:
            description = item.description if hasattr(item, 'description') else ''
            quantity = item.quantity if hasattr(item, 'quantity') else ''
            unit_price = item.unit_price if hasattr(item, 'unit_price') else ''
            total_amount = item.total_amount if hasattr(item, 'total_amount') else ''

            writer.writerow({
                'user': username,
                'supplier_name': supplier_name,
                'invoice_date': invoice_date,
                'description': description,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_amount': total_amount
            })