# Generated by Django 2.2.7 on 2019-11-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20191114_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(default='Mitigating schema mistake'),
        ),
    ]