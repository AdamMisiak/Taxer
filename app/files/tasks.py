from celery import shared_task
from models import ReportFile


@shared_task
def save_data_from_file(report_file: ReportFile):
    return report_file
