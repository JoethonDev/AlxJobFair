# Generated by Django 5.1.3 on 2024-11-27 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobscanner', '0002_scanlog_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='visits',
            field=models.IntegerField(default=0),
        ),
    ]
