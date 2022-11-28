# Generated by Django 4.1.1 on 2022-11-28 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CuringStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_date', models.DateTimeField(auto_now_add=True)),
                ('transfered_to_ready', models.BooleanField(default=False)),
                ('quantity_transfered', models.IntegerField(blank=True, default=0, null=True)),
                ('damaged', models.IntegerField(blank=True, default=0, null=True)),
                ('damages_confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReadyForSaleStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold', models.BooleanField(default=False)),
                ('selling', models.BooleanField(default=False)),
                ('damages_confirmed', models.BooleanField(default=False)),
                ('quantity_sold', models.IntegerField(blank=True, default=0, null=True)),
                ('date_received', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_sold', models.DateField(blank=True, null=True)),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='production.curingstock')),
            ],
        ),
        migrations.CreateModel(
            name='SalesTimestamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_sold', models.IntegerField(blank=True, default=0, null=True)),
                ('amount_sold', models.IntegerField(blank=True, default=0, null=True)),
                ('sale_branch', models.CharField(blank=True, max_length=400, null=True)),
                ('date_sold', models.DateField(blank=True, null=True)),
                ('sale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='production.readyforsalestock')),
            ],
        ),
        migrations.CreateModel(
            name='ReadyStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold', models.BooleanField(default=False)),
                ('selling', models.BooleanField(default=False)),
                ('quantity_sold', models.IntegerField(blank=True, default=0, null=True)),
                ('date_received', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_sold', models.DateField(blank=True, null=True)),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='production.curingstock')),
            ],
        ),
        migrations.CreateModel(
            name='RasiseProductionNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='production.readyforsalestock')),
            ],
        ),
        migrations.CreateModel(
            name='ProductMaterialConsumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oil', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('diesel', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('cement', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('white_cement', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('sand', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('river_sand', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('quarter_ballast', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('half_ballast', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('D8', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('pumice', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('dust', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('curing_days', models.PositiveIntegerField(default=10)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production.product')),
            ],
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_production', models.IntegerField(blank=True, null=True)),
                ('actual_production', models.IntegerField(blank=True, null=True)),
                ('number_of_labourers', models.IntegerField(blank=True, null=True)),
                ('wage_per_labourer', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('oil_used_in_litres', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('D8', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('fuel_used_in_litres', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('cement_bags_used', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('white_cement_bags_used', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('sand_buckets_used', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('river_sand_buckets_used', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('quarter_ballast_buckets_used', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('half_ballast_buckets_used', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('dust_buckets_used', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('damages', models.IntegerField(blank=True, null=True)),
                ('transfered_to_curing', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production.product')),
            ],
        ),
        migrations.CreateModel(
            name='Moulding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty_to_be_produced', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('qty_transfered', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('damgess', models.IntegerField(blank=True, default=0, null=True)),
                ('number_of_labourers', models.IntegerField(blank=True, null=True)),
                ('wage_per_labourer', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('transfered_to_curing', models.BooleanField(default=False)),
                ('production_confirmed', models.BooleanField(default=False)),
                ('damages_confirmed', models.BooleanField(default=False)),
                ('production_ended', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production.productmaterialconsumption')),
            ],
        ),
        migrations.AddField(
            model_name='curingstock',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='production.moulding'),
        ),
    ]
