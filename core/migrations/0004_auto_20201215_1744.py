# Generated by Django 3.1.4 on 2020-12-15 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201215_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(),
        ),
    ]
