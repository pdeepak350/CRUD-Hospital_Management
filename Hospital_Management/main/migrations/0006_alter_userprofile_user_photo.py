# Generated by Django 3.2 on 2021-05-02 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_userprofile_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_photo',
            field=models.ImageField(default='admin.png', upload_to='profile/'),
        ),
    ]