# Generated by Django 3.2.7 on 2021-10-21 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0002_alter_couple_bride_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couple',
            name='groom_photo',
            field=models.ImageField(default='static/images/avatar-profil.png', upload_to='couple_images/'),
        ),
    ]
