# Generated by Django 5.0.4 on 2024-04-30 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.CharField(choices=[('Fall', 'Fall'), ('Winter', 'Wint'), ('Spring', 'Spri'), ('Summer', 'Summ')], default='Fall', max_length=6),
        ),
    ]