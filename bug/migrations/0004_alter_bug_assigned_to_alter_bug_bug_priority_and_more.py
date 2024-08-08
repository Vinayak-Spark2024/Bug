# Generated by Django 5.0.7 on 2024-08-08 10:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0003_alter_bug_assigned_to_alter_bug_bug_priority_and_more'),
        ('department', '0002_alter_department_user'),
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_bugs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bug',
            name='bug_priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10),
        ),
        migrations.AlterField(
            model_name='bug',
            name='bug_severity',
            field=models.CharField(choices=[('critical', 'Critical'), ('major', 'Major'), ('normal', 'Normal'), ('minor', 'Minor'), ('trivial', 'Trivial'), ('enhancements', 'Enhancements/Feature Requests')], max_length=20),
        ),
        migrations.AlterField(
            model_name='bug',
            name='bug_type',
            field=models.CharField(choices=[('error', 'Error'), ('mistake', 'Mistake'), ('bug', 'Bug'), ('issue', 'Issue'), ('fault', 'Fault'), ('defect', 'Defect'), ('other', 'Other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='bug',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='bugs/'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='report_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bug',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('in_progress', 'In Progress')], max_length=20),
        ),
        migrations.AlterField(
            model_name='bug',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
