# Generated by Django 2.2.5 on 2021-09-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservtions', '0002_auto_20210731_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', '보류중'), ('confirmed', '확인됨'), ('canceled', '취소됨')], default='pending', max_length=12),
        ),
    ]