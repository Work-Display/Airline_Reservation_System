# Generated by Django 4.2.1 on 2023-12-10 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_reservation_system', '0018_alter_users_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='APICounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
