# Generated by Django 2.2.5 on 2021-07-29 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20210729_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
