# Generated by Django 4.1.5 on 2023-02-08 23:24

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_delete_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file_name",
                    models.FileField(
                        upload_to="static/files_admin",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["xlsx", "xls"]
                            )
                        ],
                    ),
                ),
                (
                    "upload_date",
                    models.DateField(
                        default=datetime.datetime(2023, 2, 9, 0, 24, 23, 887173)
                    ),
                ),
            ],
        ),
    ]