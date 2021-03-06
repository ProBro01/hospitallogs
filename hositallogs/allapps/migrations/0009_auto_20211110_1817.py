# Generated by Django 3.2.8 on 2021-11-10 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('allapps', '0008_hospital_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='picture',
        ),
        migrations.AlterField(
            model_name='hospital',
            name='hospitalimage',
            field=models.ImageField(upload_to='hospitalimage'),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='allapps.hospital'),
        ),
    ]
