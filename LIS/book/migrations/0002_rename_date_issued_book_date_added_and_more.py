# Generated by Django 4.0.3 on 2022-03-25 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='date_issued',
            new_name='date_added',
        ),
        migrations.AlterField(
            model_name='book',
            name='issue_status',
            field=models.DateField(null=True),
        ),
    ]