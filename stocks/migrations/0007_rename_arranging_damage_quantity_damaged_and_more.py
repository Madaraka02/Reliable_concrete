# Generated by Django 4.1.1 on 2022-09-21 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0024_remove_curingstock_curing_days_and_more'),
        ('stocks', '0006_releaseqty_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='damage',
            old_name='arranging',
            new_name='quantity_damaged',
        ),
        migrations.RemoveField(
            model_name='damage',
            name='packing',
        ),
        migrations.RemoveField(
            model_name='damage',
            name='production',
        ),
        migrations.AddField(
            model_name='damage',
            name='category',
            field=models.CharField(choices=[('1', '1'), ('PRODUCTION', 'PRODUCTION'), ('PACKING', 'PACKING'), ('CURING', 'CURING'), ('TRANSPORTING', 'TRANSPORTING'), ('OFFLOADING', 'OFFLOADING')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='damage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.moulding'),
        ),
    ]
