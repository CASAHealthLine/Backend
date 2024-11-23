# Generated by Django 5.1.3 on 2024-11-23 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casa', '0002_customuser_role_customuser_user_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('user', 'User'), ('doctor', 'Doctor'), ('specialist', 'Specialist'), ('receptionist', 'Receptionist'), ('admin', 'Admin')], default='user', max_length=20),
        ),
    ]
