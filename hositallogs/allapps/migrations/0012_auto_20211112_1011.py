# Generated by Django 3.2.8 on 2021-11-12 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allapps', '0011_alter_hospital_discriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='password',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='doctorImages'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='ratings',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='discriptions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
