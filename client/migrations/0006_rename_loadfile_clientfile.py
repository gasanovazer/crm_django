# Generated by Django 4.1.3 on 2024-07-12 13:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0003_team_plan"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("client", "0005_loadfile"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="LoadFile",
            new_name="ClientFile",
        ),
    ]
