# Generated by Django 2.1.1 on 2018-10-20 13:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0008_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('code', models.CharField(max_length=6)),
                ('current', models.CharField(max_length=5)),
                ('expected', models.CharField(max_length=5)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]