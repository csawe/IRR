# Generated by Django 4.1.5 on 2023-01-23 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0002_alter_property_capitalgrowthrates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='bond_value',
            field=models.IntegerField(null=True),
        ),
    ]