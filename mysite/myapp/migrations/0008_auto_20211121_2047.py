# Generated by Django 3.2.6 on 2021-11-21 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_userprofilemodel_userpic'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_item_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='cart',
            name='cart_item',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_item',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='cart_item_quality',
            field=models.ImageField(default=0, upload_to=''),
        ),
        migrations.RemoveField(
            model_name='cart',
            name='cart_product',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_product',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]