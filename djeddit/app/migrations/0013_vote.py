# Generated by Django 2.2.7 on 2019-11-20 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20191120_0457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted', models.BooleanField()),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='app.Comment')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='app.Post')),
                ('user_voted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes_done', to='app.UserProfile')),
            ],
        ),
    ]
