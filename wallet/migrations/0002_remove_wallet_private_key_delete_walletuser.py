# Generated by Django 4.2.4 on 2024-02-07 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='private_key',
        ),
        migrations.DeleteModel(
            name='WalletUser',
        ),
    ]