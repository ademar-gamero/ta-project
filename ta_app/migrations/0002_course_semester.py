# Generated by Django 5.0.4 on 2024-04-27 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('Fall', 'Fall'), ('Winter', 'Wint'), ('Spring', 'Spri'), ('Summer', 'Summ')], default=None, max_length=7),
        ),
    ]