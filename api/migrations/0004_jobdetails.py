# Generated by Django 3.0.3 on 2021-02-07 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200118_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('contact_number_one', models.CharField(max_length=10)),
                ('descriptions', models.TextField(default=None)),
            ],
            options={
                'db_table': 'job_details',
            },
        ),
    ]
