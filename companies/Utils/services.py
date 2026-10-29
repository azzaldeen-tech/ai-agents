from companies.models import JobApplication, SimpleApplication
from django.shortcuts import get_object_or_404


def change_job_application_status(pk,status):
    if status and pk :
        job_app=get_object_or_404(JobApplication, pk=pk)
        if job_app:
            job_app.status=status
            job_app.save(update_fields=['status'])


def get_filtered_applications(**filters):
    return JobApplication.objects.filter(**filters) \
        .select_related('job', 'member__user') \
        .order_by('-match_score') \
        .distinct()


def get_job_simple_applications(job_applications):
    return  [SimpleApplication(app) for app in job_applications]
def get_job_applications(company, status=None):
    # Initialize filters with the required company field
    filters = {'job__company': company}

    # Only add status to the filter if it was actually provided
    if status is not None:
        filters['status'] = status

    return JobApplication.objects.filter(**filters)\
        .select_related('job', 'member__user')\
        .order_by('-match_score')