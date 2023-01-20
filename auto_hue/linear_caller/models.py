from django.db import models

# TODO test agains whether or not the key values ascending in order
# TODO make it so that a job can start on the previous day
class CircadianTime(models.Model):
    start_time = models.IntegerField('start cron time')
    mid_time = models.IntegerField('mid cron time')
    end_time = models.IntegerField('end cron time')

    def __str__(self):
        return (
            self.start_time,
            self.mid_time,
            self.end_time
        )

class CircadianTime_Named(models.Model):
    # this model is for named jobs that can be saved in a list
    # relate all 3 times of jobs
    start_time = models.ForeignKey(CircadianTime, related_name='start_time')
    mid_time = models.ForeignKey(CircadianTime, related_name='mid_time')
    end_time = models.ForeignKey(CircadianTime, related_name='end_time')
    job_creation_date = models.DateTimeField('Date this job was created.')
    # and the name for the jobs
    circadian_job_name = models.CharField(max_length=20)
    circadian_job_description = models.CharField(max_length=100)

    def __str__(self):
        return self.circadian_job_name