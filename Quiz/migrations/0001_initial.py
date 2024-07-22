# Generated by Django 5.0.4 on 2024-07-22 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Question",
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
                ("question_statement", models.CharField(max_length=256)),
                (
                    "question_type",
                    models.CharField(
                        choices=[
                            ("MCQ", "Multiple Choice"),
                            ("TF", "True/False"),
                            ("SA", "Short Answer"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "difficulty_level",
                    models.CharField(
                        choices=[
                            ("Easy", "Easy"),
                            ("Medium", "Medium"),
                            ("Hard", "Hard"),
                        ],
                        max_length=10,
                    ),
                ),
                ("correct_answer", models.CharField(blank=True, max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name="Quiz",
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
                ("title", models.CharField(max_length=100)),
                (
                    "difficulty_level",
                    models.CharField(
                        choices=[
                            ("Easy", "Easy"),
                            ("Medium", "Medium"),
                            ("Hard", "Hard"),
                        ],
                        default="",
                        max_length=10,
                    ),
                ),
                ("Total_score", models.IntegerField(blank=True, default=10)),
                (
                    "Time_allowed",
                    models.IntegerField(help_text="Enter duration in minutes"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentAnswer",
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
                ("answer", models.TextField()),
                ("score", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="StudentQuizAttempt",
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
                ("attempt_date", models.DateTimeField(auto_now_add=True)),
                ("attempt_score", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="AnswerOptions",
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
                ("option_text", models.CharField(max_length=256)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="options",
                        to="Quiz.question",
                    ),
                ),
            ],
        ),
    ]
