from companies.models import Job, JobApplication


class CompanyService:

    def get_jobs_count(self, company_id,active=True):
        return Job.objects.filter(company_id=company_id, is_active=active).count()
    def get_active_jobs_count(self, company_id):
        return self.get_jobs_count(company_id,True)
    def get_inactive_jobs_count(self, company_id):
        return self.get_jobs_count(company_id,False)

    def get_pending_applications_count(self, company_id):
        return JobApplication.objects.filter(job__company_id=company_id,
                                             status=JobApplication.Status.PENDING).count()

    def get_applications_count(self,company_id):
        apps_count = JobApplication.objects.filter(job__company_id=company_id).select_related('job', 'user').count()
        return apps_count or 0


    @classmethod
    def get_global_stats(cls,company_id):
        service=cls()

        return {
            "active_jobs_count": service.get_active_jobs_count(company_id),
            "inactive_jobs_count": service.get_inactive_jobs_count(company_id),
            "apps_count": service.get_applications_count(company_id),
            # "last_update": timezone.now()
        }