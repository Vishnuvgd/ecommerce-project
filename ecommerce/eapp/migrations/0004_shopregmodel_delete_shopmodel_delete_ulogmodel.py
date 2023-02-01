# Generated by Django 4.1.5 on 2023-01-25 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0003_rename_em_shopmodel_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='shopregmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=25)),
            ],
        ),
        migrations.DeleteModel(
            name='shopmodel',
        ),
        migrations.DeleteModel(
            name='ulogmodel',
        ),
    ]
