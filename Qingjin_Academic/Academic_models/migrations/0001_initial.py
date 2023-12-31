# Generated by Django 4.1 on 2023-12-11 01:00

import Academic_models.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Admin",
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
                ("username", models.CharField(max_length=20, unique=True)),
                ("password", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("comment_time", models.DateTimeField(auto_now=True)),
                ("paper_id", models.CharField(max_length=20)),
                ("content", models.CharField(max_length=20)),
                ("top", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Paper_display",
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
                ("es_id", models.CharField(max_length=20, unique=True)),
                ("display", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Scholar",
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
                ("es_id", models.CharField(max_length=20, unique=True)),
                ("name", models.CharField(max_length=80)),
                ("claim_email", models.TextField(null=True)),
                ("claimed_user_id", models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(max_length=20, unique=True)),
                ("password", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=50, unique=True)),
                (
                    "claimed_scholar",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.scholar",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Star_folder",
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
                ("name", models.CharField(max_length=20)),
                ("num", models.IntegerField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Star",
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
                ("type", models.IntegerField(default=0)),
                ("paper_id", models.CharField(max_length=20)),
                ("time", models.DateTimeField(auto_now=True)),
                (
                    "folder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.star_folder",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Report",
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
                ("paper_id", models.CharField(max_length=20)),
                ("report_text", models.CharField(max_length=100, null=True)),
                (
                    "report_file",
                    models.FileField(
                        null=True,
                        upload_to=Academic_models.models.report_file_upload_to,
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.comment",
                    ),
                ),
                (
                    "reported_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="History",
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
                ("paper_id", models.CharField(max_length=20)),
                ("type", models.IntegerField(default=0)),
                ("time", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.user",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Academic_models.user"
            ),
        ),
        migrations.CreateModel(
            name="Claim",
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
                ("claim_email", models.CharField(max_length=50, null=True)),
                ("claim_text", models.CharField(max_length=100, null=True)),
                (
                    "claim_file",
                    models.FileField(
                        null=True, upload_to=Academic_models.models.claim_file_upload_to
                    ),
                ),
                (
                    "claimed_scholar",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.scholar",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Appeal",
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
                ("appeal_email", models.CharField(max_length=50, null=True)),
                ("appeal_text", models.CharField(max_length=100, null=True)),
                (
                    "appeal_file",
                    models.FileField(
                        null=True,
                        upload_to=Academic_models.models.appeal_file_upload_to,
                    ),
                ),
                (
                    "appealed_scholar",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.scholar",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Affair",
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
                ("type", models.IntegerField(default=0)),
                ("submit_time", models.DateTimeField(auto_now_add=True)),
                ("handle_time", models.DateTimeField(auto_now=True)),
                ("handle_reason", models.CharField(max_length=100, null=True)),
                ("status", models.IntegerField(default=0)),
                (
                    "appeal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.appeal",
                    ),
                ),
                (
                    "claim",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.claim",
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.report",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Academic_models.user",
                    ),
                ),
            ],
        ),
    ]
