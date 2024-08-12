# Generated by Django 5.0.7 on 2024-08-12 10:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('bug_id', models.AutoField(primary_key=True, serialize=False)),
                ('bug_type', models.CharField(choices=[('error', 'Error'), ('mistake', 'Mistake'), ('bug', 'Bug'), ('issue', 'Issue'), ('fault', 'Fault'), ('defect', 'Defect'), ('other', 'Other')], max_length=20)),
                ('report_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('bug_description', models.TextField()),
                ('url_bug', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='bugs/')),
                ('bug_priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10)),
                ('bug_severity', models.CharField(choices=[('critical', 'Critical'), ('major', 'Major'), ('normal', 'Normal'), ('minor', 'Minor'), ('trivial', 'Trivial'), ('enhancements', 'Enhancements/Feature Requests')], max_length=20)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('in_progress', 'In Progress')], max_length=20)),
                ('is_current_project', models.BooleanField(default=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_bugs', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_bugs', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
        ),
    ]
