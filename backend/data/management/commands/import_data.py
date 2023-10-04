from django.core.management.base import BaseCommand
from data.models import FinanceData
import pandas as pd

class Command(BaseCommand):
    help = 'Import data from Excel file to FinanceData model'

    def handle(self, *args, **options):
        # Read the Excel file into a DataFrame
        df = pd.read_excel("data/management/commands/bank.xlsx")
        df.columns = df.columns.str.replace(' ', '_')
        df.fillna(0, inplace=True)
        print(df.columns[4])
        #Your data processing and saving logic here
        for row in df.itertuples():
            account_number = row[1]
            date = row[2]
            details = row[3]
            withdraw = row[4]
            deposit = row[5]
            balance = row[6]

            


            # Create and save FinanceData instance
            finance_data = FinanceData(
                account_number=account_number,
                date=date,
                details=details,
                withdraw=withdraw,
                deposit=deposit,
                balance=balance
            )
            finance_data.save()