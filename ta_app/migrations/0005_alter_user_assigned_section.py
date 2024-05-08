# Generated by Django 5.0.4 on 2024-05-07 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_app', '0004_alter_user_assigned_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='assigned_section',
            field=models.ManyToManyField(related_name='assigned_users', to='ta_app.section'),
        ),
    ]