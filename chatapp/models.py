from functools import total_ordering
from pyexpat import model
from django.db import models

# Create your models here.
GENDER_CHOICES =(
    ("male", "male"),
    ("female", "female"),
)
class Student(models.Model):
    school_id = models.IntegerField()
    branch_vls_id = models.IntegerField()
    exam_id = models.IntegerField()
    class_id = models.IntegerField()
    section_id = models.IntegerField()
    academic_year = models.IntegerField()
    student_id = models.IntegerField(unique=True)
    student_name = models.CharField(max_length=50)
    student_gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    total_subject = models.IntegerField()
    total_mark = models.IntegerField()
    total_obtain_mark = models.IntegerField()
    total_grade_point = models.FloatField()
    grade_id = models.IntegerField()
    result_status = models.CharField(max_length=50)
    merit_rank_in_class = models.CharField(max_length=50)
    merit_rank_in_section = models.CharField(max_length=50)
    remark = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    paid = models.FloatField()
    due = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True)
    create_by = models.CharField(max_length=50)
    modified_by = models.CharField(max_length=50)

    def __str__(self):
        return str(self.student_id)
