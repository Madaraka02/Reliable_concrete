# Generated by Django 4.1.1 on 2022-09-27 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_alter_damage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damage',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='damages'),
        ),
    ]
