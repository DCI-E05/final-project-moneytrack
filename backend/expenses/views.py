from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ExpenseSerializer
from .models import Expense
from django.conf import settings
from mindee import Client, documents
from .forms import ReceiptUploadForm
import csv

class ExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()

    def get_queryset(self):
        user = self.request.user
        query_set = self.queryset
        return query_set.filter(user=user)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def upload_receipt(self, request):
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            receipt_image = request.FILES['receipt_image']
            if not receipt_image.content_type.startswith('image/'):
                return Response({"error": "Invalid file type. Please upload an image."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                process_mindee_api(receipt_image, request)
            except Exception as e:
                return Response({"error": f"Error with Mindee API: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "Receipt processed successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid form submission."}, status=status.HTTP_400_BAD_REQUEST)

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
    with open(settings.CSV_FILE_EXPENSES, 'a', newline='') as csvfile:
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