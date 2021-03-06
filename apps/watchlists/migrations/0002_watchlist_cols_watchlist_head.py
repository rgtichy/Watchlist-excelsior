# Generated by Django 2.2 on 2020-07-02 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
        ('watchlists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist_Head',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('wval_1', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wval_2', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wval_3', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wval_4', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wval_5', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wpct_1', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wpct_2', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wpct_3', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wpct_4', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('wpct_5', models.DecimalField(decimal_places=6, default=0, max_digits=24)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to='userprofiles.User')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist_cols',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq', models.FloatField(default=0)),
                ('col_name', models.CharField(max_length=255)),
                ('formula', models.TextField()),
                ('test', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='watchlists.Watchlist_Head')),
            ],
        ),
    ]
