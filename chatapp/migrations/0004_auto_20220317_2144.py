# Generated by Django 3.2.12 on 2022-03-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_alter_student_academic_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='due',
            field=models.FloatField(default=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='paid',
            field=models.FloatField(default=460),
            preserve_default=False,
        ),
    ]