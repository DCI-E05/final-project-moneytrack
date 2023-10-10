from django.core.management.base import BaseCommand, CommandParser, CommandError
from data.models import FinanceData
import pandas as pd
import os
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Import data from Excel or CSV files in a directory to FinanceData model'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("directory", type=str)

    def handle(self, *args, **options):
        directory = options.get("directory", None)
        if not directory:
            raise CommandError("Directory not found!")

        if not os.path.isdir(directory):
            raise CommandError("Invalid directory path!")

        for root, _, files in os.walk(directory):
            for filename in files:
                _, file_extension = os.path.splitext(filename)
                if file_extension.lower() == '.xlsx' or file_extension.lower() == '.csv':
                    file_path = os.path.join(root, filename)

                    # Read the file into a DataFrame
                    if file_extension.lower() == '.xlsx':
                        df = pd.read_excel(file_path)
                    else:
                        df = pd.read_csv(file_path)

                    df.columns = df.columns.str.replace(' ', '_')
                    df.fillna(0, inplace=True)

                    # Your data processing and saving logic here
                    for row in df.itertuples():
                        account_number = row[1]
                        date = row[2]
                        details = row[3]
                        withdraw = row[4]
                        deposit = row[5]
                        balance = row[6]

                        # Create and save FinanceData instance
                        finance_data = FinanceData(
                            user = User.objects.first(),
                            account_number=account_number,
                            date=date,
                            details=details,
                            withdraw=withdraw,
                            deposit=deposit,
                            balance=balance
                        )
                        finance_data.save()
