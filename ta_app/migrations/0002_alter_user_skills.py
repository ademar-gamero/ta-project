# Generated by Django 5.0.4 on 2024-05-15 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='skills',
            field=models.CharField(default='None', max_length=500, null=True),
        ),
    ]