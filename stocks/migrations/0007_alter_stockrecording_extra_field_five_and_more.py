# Generated by Django 4.1.1 on 2022-09-28 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_stockrecording'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockrecording',
            name='extra_field_five',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='stockrecording',
            name='extra_field_four',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='stockrecording',
            name='extra_field_one',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='stockrecording',
            name='extra_field_three',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='stockrecording',
            name='extra_field_two',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='stockrecording',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
