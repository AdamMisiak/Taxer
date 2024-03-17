from celery import shared_task
from files.models import ReportFile
from django.conf import settings
from files.logic import save_data_ib_lynx_report_file

@shared_task
def save_data_from_report_file(report_file_id: int):
    print("-------TESTING CELERY TASK-------")
    print(ReportFile.objects.get(id=report_file_id))
    report_file_object = ReportFile.objects.get(id=report_file_id)
    broker_name = report_file_object.broker.name

    with report_file_object.file.open("r") as file:
        # NOTE make migrations/or something else with ib and lynx brokers by default 
        # NOTE instead of ifs, use dict with mapping
        if broker_name in [settings.INTERACTIVE_BROKERS, settings.LYNX]:
            print("IB/LYNX BROKER")
            save_data_ib_lynx_report_file(file)
        # NOTE handle IB/LYNX here
