# Generated by Django 4.1.1 on 2022-09-27 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeStampedMaterialUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.rawmaterial')),
            ],
        ),
    ]
