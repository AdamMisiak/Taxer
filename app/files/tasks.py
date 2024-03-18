from celery import shared_task
from files.models import ReportFile
from django.conf import settings
from files.logic import save_data_ib_lynx_report_file

broker_name_mapping = {
    settings.INTERACTIVE_BROKERS: save_data_ib_lynx_report_file,
    settings.LYNX: save_data_ib_lynx_report_file,
}

@shared_task
def save_data_from_report_file(report_file_id: int):
    print("-------TESTING CELERY TASK-------")
    # NOTE add some standar logging at the beginning of the task
    print(ReportFile.objects.get(id=report_file_id))
    report_file_object = ReportFile.objects.get(id=report_file_id)
    broker_name = report_file_object.broker.name

    with report_file_object.file.open("r") as file:
        broker_name_mapping[broker_name](file)
