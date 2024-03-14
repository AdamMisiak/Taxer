from celery import shared_task
from files.models import ReportFile


@shared_task
def save_data_from_report_file(report_file_id: int):
    print("-------TESTING CELERY TASK-------")
    print(ReportFile.objects.get(id=report_file_id))
    report_file_object = ReportFile.objects.get(id=report_file_id)
    with report_file_object.file.open("r") as file:
        print(file)
        print(report_file_object.broker.name)
        # NOTE handle IB/LYNX here
