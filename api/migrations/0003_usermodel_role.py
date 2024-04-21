# Generated by Django 4.2.11 on 2024-04-20 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_usermodel_options_usermodel_company_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='role',
            field=models.IntegerField(blank=True, choices=[(1, 'EMPLOYEE'), (2, 'EMPLOYER')], null=True),
        ),
    ]