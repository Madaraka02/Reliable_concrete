# Generated by Django 4.1.1 on 2022-09-27 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_remove_timestampedmaterialupdate_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timestampedmaterialupdate',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]
