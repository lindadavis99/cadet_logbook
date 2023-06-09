# Generated by Django 4.2 on 2023-04-17 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cadetlogbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_summary', models.CharField(max_length=4000)),
                ('description_of_work', models.TextField()),
                ('start_and_end_date', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Cadetlogbook',
                'ordering': ('-created',),
            },
        ),
    ]
