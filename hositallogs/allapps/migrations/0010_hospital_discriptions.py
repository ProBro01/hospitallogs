# Generated by Django 3.2.8 on 2021-11-12 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allapps', '0009_auto_20211110_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='discriptions',
            field=models.TextField(default=True),
            preserve_default=False,
        ),
    ]
