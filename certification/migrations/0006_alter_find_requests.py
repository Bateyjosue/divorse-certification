# Generated by Django 3.2.7 on 2021-11-01 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0005_find'),
    ]

    operations = [
        migrations.AlterField(
            model_name='find',
            name='requests',
            field=models.CharField(choices=[('Marriage', 'Marriage'), ('Divorce', 'Divorce')], max_length=50),
        ),
    ]