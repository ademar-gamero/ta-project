# Generated by Django 5.0.4 on 2024-05-01 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_app', '0005_alter_user_assigned_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]