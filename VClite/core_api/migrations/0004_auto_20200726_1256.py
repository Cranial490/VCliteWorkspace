# Generated by Django 3.0.8 on 2020-07-26 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_api', '0003_auto_20200725_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='vc_t_ask',
            name='parent_order',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='core_api.VC_T_Order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vc_t_bid',
            name='parent_order',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='core_api.VC_T_Order'),
            preserve_default=False,
        ),
    ]
