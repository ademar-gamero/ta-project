# Generated by Django 5.0.4 on 2024-05-12 21:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.IntegerField(null=True)),
                ('course_name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('semester', models.CharField(choices=[('Fall', 'Fall'), ('Winter', 'Wint'), ('Spring', 'Spri'), ('Summer', 'Summ')], default='Fall', max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Mo', 'Monday'), ('Tu', 'Tuesday'), ('We', 'Wednesday'), ('Th', 'Thursday'), ('Fr', 'Friday')], max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_id', models.IntegerField(null=True)),
                ('meeting_time', models.DateTimeField(null=True)),
                ('type', models.CharField(choices=[('lab', 'Lab'), ('lecture', 'Lec')], default='lecture', max_length=7)),
                ('course_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_app.course')),
                ('meeting_days', models.ManyToManyField(blank=True, to='ta_app.day')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.CharField(choices=[('Admin', 'Ad'), ('Teacher-Assistant', 'Ta'), ('Instructor', 'In')], default='Teacher-Assistant', max_length=17)),
                ('phone_number', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=256)),
                ('assigned', models.BooleanField(null=True)),
                ('assigned_section', models.ManyToManyField(blank=True, to='ta_app.section')),
            ],
        ),
    ]
