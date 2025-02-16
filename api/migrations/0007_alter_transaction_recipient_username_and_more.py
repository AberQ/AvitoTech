# Generated by Django 5.1.6 on 2025-02-15 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_rename_recipient_email_transaction_recipient_username_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="recipient_username",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="sender_username",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
