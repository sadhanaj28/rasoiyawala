# Generated by Django 3.0.3 on 2021-02-07 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210207_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdetails',
            name='contact_number_one',
            field=models.CharField(default='0000000000', max_length=10),
        ),
    ]
