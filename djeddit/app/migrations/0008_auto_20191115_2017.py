# Generated by Django 2.2.7 on 2019-11-15 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20191115_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_subs', to='app.UserProfile'),
        ),
    ]
