from celery import shared_task
from files.models import ReportFile, CurrencyRateFile
from django.conf import settings
from files.logic import save_data_ib_lynx_report_file
from utils.exceptions import ImportException

broker_name_mapping = {
    settings.INTERACTIVE_BROKERS: save_data_ib_lynx_report_file,
    settings.LYNX: save_data_ib_lynx_report_file,
}

@shared_task
def save_data_from_report_file(report_file_id: int):
    print("⚡️ Celery task: save_data_from_report_file function started.")
    # NOTE add some standar logging at the beginning of the task

    report_file_object = ReportFile.objects.get(id=report_file_id)
    broker_name = report_file_object.broker.name

    with report_file_object.file.open("r") as file:
        try:
            broker_name_mapping[broker_name](file, report_file_object)
        except KeyError:
            raise ImportException("❌ Report file broker is not available!")



@shared_task
def save_data_from_currency_rate_file(currency_rate_file_id: int):
    from files.logic import save_data_currency_rate_file

    print("⚡️ Celery task: save_data_from_curenncy_rate_file function started.")
    curenncy_rate_file_object = CurrencyRateFile.objects.get(id=currency_rate_file_id)

    with curenncy_rate_file_object.file.open("r") as file:
        if curenncy_rate_file_object.file.name.startswith("Rates"):
            save_data_currency_rate_file(file)
        else:
            raise ImportException("❌ Currency Rate file name has to begin with `Rates`!")
