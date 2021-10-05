# Generated by Django 2.2.5 on 2021-07-29 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0002_auto_20210729_0101"),
    ]

    operations = [
        migrations.CreateModel(
            name="Amenity",
            fields=[
                (
                    "abstractitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="rooms.AbstractItem",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("rooms.abstractitem",),
        ),
        migrations.CreateModel(
            name="Facility",
            fields=[
                (
                    "abstractitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="rooms.AbstractItem",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("rooms.abstractitem",),
        ),
        migrations.CreateModel(
            name="Rule",
            fields=[
                (
                    "abstractitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="rooms.AbstractItem",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("rooms.abstractitem",),
        ),
        migrations.RemoveField(
            model_name="room",
            name="room_type",
        ),
        migrations.AddField(
            model_name="room",
            name="room_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="rooms.RoomType",
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="amenities",
            field=models.ManyToManyField(to="rooms.Amenity"),
        ),
        migrations.AddField(
            model_name="room",
            name="facilities",
            field=models.ManyToManyField(to="rooms.Facility"),
        ),
        migrations.AddField(
            model_name="room",
            name="house_rules",
            field=models.ManyToManyField(to="rooms.Rule"),
        ),
    ]
