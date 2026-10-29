from companies.models import Job, JobApplication


class MemberService:



    def get_pending_applications(self, member_id):
        return JobApplication.objects.filter(
            job__member_id=member_id,
            status=JobApplication.Status.PENDING
        ).count()

    @classmethod
    def get_global_stats(self,member_id=0):
        service=self()
        return {
            "jobs_count": Job.objects.filter(is_active=True).count(),
            # "apps_count": service.get_pending_applications(member_id),
            # "last_update": timezone.now()
        }