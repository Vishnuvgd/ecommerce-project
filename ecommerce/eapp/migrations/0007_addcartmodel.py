# Generated by Django 4.1.5 on 2023-01-28 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0006_uploadmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='addcartmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cartname', models.CharField(max_length=25)),
                ('cartimage', models.ImageField(upload_to='eapp/static')),
                ('cartprice', models.IntegerField()),
                ('cartdescription', models.CharField(max_length=30)),
            ],
        ),
    ]
