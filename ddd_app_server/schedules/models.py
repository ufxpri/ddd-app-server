import uuid
from django.db import models
from django.contrib.auth.models import User
from members.models import Member


class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_schedules')

    def __str__(self):
        return self.title


class Attendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
        ('unknown', 'Unknown'),
    ]
    METHOD_CHOICES = [
        ('qr', 'QR'),
        ('manual', 'Manual'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendance_records')  # Many-to-one relation with Member
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendance_records')  # Many-to-one relation with Schedule
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS_CHOICES)
    arrive_time = models.DateTimeField(null=True, blank=True)
    leave_time = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.schedule.title} - {self.member.name}"
