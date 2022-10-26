# Generated by Django 4.1.1 on 2022-10-26 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_materialsale_sale_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchmaterialcounts',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.branch'),
        ),
        migrations.AlterField(
            model_name='dispatchmaterialexternal',
            name='to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.branch'),
        ),
        migrations.AlterField(
            model_name='dispatchmaterialtosite',
            name='to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.site'),
        ),
        migrations.AlterField(
            model_name='sitematerialcounts',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.site'),
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
    ]
