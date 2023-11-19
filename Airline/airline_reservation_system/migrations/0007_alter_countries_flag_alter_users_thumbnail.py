# Generated by Django 4.2.1 on 2023-06-26 12:20

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('airline_reservation_system', '0006_alter_countries_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countries',
            name='flag',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=False, null=True, quality=75, scale=0.5, size=[240, 180], upload_to='./web-design/upload_img/user_flags/'),
        ),
        migrations.AlterField(
            model_name='users',
            name='thumbnail',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=False, null=True, quality=75, scale=0.5, size=[500, None], upload_to='./web-design/upload_img/user_thumbnails/'),
        ),
    ]
