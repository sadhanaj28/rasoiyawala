# Generated by Django 3.0.3 on 2021-02-07 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_jobdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobLocationMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_id', models.IntegerField()),
                ('location_id', models.IntegerField()),
            ],
            options={
                'db_table': 'job_location_mapping',
            },
        ),
        migrations.AlterField(
            model_name='jobdetails',
            name='contact_number_one',
            field=models.CharField(default=None, max_length=10),
        ),
    ]
