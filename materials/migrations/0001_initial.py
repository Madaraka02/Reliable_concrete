# Generated by Django 4.1.1 on 2022-11-28 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, null=True)),
                ('manager', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BranchMaterialCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, default=0, max_digits=200, null=True)),
                ('date', models.DateField(null=True)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.branch')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, null=True)),
                ('confirm_received', models.BooleanField(default=False)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('date', models.DateField(null=True)),
                ('available_qty', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, null=True)),
                ('manager', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TotalMaterialCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, default=0, max_digits=200, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='TimeStampedMaterialUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='SiteMaterialUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.site')),
            ],
        ),
        migrations.CreateModel(
            name='SiteMaterialCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, default=0, max_digits=200, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.site')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterialUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.rawmaterial')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='production.productmaterialconsumption')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('sale_by', models.CharField(max_length=400, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, default=0, max_digits=200, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='DispatchMaterialToSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.site')),
            ],
        ),
        migrations.CreateModel(
            name='DispatchMaterialExternal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.branch')),
            ],
        ),
        migrations.CreateModel(
            name='BranchMaterialSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('date', models.DateField(null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.branchmaterialcounts')),
            ],
        ),
        migrations.AddField(
            model_name='branchmaterialcounts',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial'),
        ),
    ]
