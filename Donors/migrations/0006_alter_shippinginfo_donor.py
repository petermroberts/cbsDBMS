# Generated by Django 4.1.7 on 2023-03-26 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Donors', '0005_remove_shippinginfo_id_alter_shippinginfo_donor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippinginfo',
            name='donor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Donors.donor'),
        ),
    ]
