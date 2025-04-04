# Generated by Django 5.1 on 2025-03-30 19:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sums', '0002_alter_budgets_annual_budget_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounts',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='budgets',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='snapshots',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='account_nickname',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='budget_id',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='user_id',
        ),
        migrations.AddField(
            model_name='accounts',
            name='user',
            field=models.ForeignKey(db_column='user', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='budgets',
            name='user',
            field=models.ForeignKey(db_column='user', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='snapshots',
            name='user',
            field=models.ForeignKey(db_column='user', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transactions',
            name='account',
            field=models.ForeignKey(db_column='account', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='sums.accounts'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='budget',
            field=models.ForeignKey(db_column='budget', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='sums.budgets'),
        ),
        migrations.AddField(
            model_name='transactions',
            name='user',
            field=models.ForeignKey(db_column='user', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
