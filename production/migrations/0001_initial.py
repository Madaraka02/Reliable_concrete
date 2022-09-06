# Generated by Django 4.1.1 on 2022-09-06 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=400, null=True)),
                ('target_production', models.IntegerField(null=True)),
                ('actual_production', models.IntegerField(null=True)),
                ('number_of_labourers', models.IntegerField(null=True)),
                ('wage_per_labourer', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('oil_used_in_litres', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('fuel_used_in_litres', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('cement_bags_used', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('white_cement_bags_used', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('sand_buckets_used', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('river_sand_buckets_used', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('quarter_ballast_buckets_used', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('half_ballast_buckets_used', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('dust_buckets_used', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('damages', models.IntegerField(null=True)),
                ('date', models.DateField()),
            ],
        ),
    ]
