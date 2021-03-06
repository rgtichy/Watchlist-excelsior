# Generated by Django 2.2 on 2020-06-30 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Ticker_Tag_Periods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(db_index=True, max_length=255)),
                ('tag', models.CharField(db_index=True, max_length=25)),
                ('period', models.CharField(choices=[('QTR0', 'Most Recent Quarter'), ('QTR1', '2nd Most Recent Quarter'), ('QTR2', '3rd Most Recent Quarter'), ('QTR2', '3rd Most Recent Quarter'), ('QTR3', '4th Most Recent Quarter'), ('QTR4', '5th Most Recent Quarter'), ('QTR5', '6th Most Recent Quarter'), ('QTR6', '7th Most Recent Quarter'), ('QTR7', '8th Most Recent Quarter'), ('TTM0', 'Most Recent Trailing 12 Months'), ('TTM1', 'Trailing 12 Months, 1 Quarter Arrears'), ('TTM2', 'Trailing 12 Months, 2 Quarters Arrears'), ('TTM3', 'Trailing 12 Months, 3 Quarters Arrears'), ('TTM4', 'Trailing 12 Months, 1 Year in Arrears'), ('TTM5', 'Trailing 12 Months, 5 Quarters Arrears'), ('TTM6', 'Trailing 12 Months, 6 Quarters Arrears'), ('TTM7', 'Trailing 12 Months, 7 Quarters Arrears'), ('TTM8', 'Trailing 12 Months, 2 Years in Arrears')], default='QTR0', max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickertags', to='userprofiles.User')),
            ],
        ),
    ]
