# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    nickname = models.TextField(blank=True, null=True)
    account_owner = models.ForeignKey('Users', models.DO_NOTHING, db_column='account_owner')
    account_type = models.TextField(blank=True, null=True)
    account_last_four = models.IntegerField(blank=True, null=True)
    bank = models.ForeignKey('Banks', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts'


class Banks(models.Model):
    bank_id = models.AutoField(primary_key=True)
    name = models.TextField()
    fieldnames = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'banks'


class BanksUsers(models.Model):
    username = models.OneToOneField('Users', models.DO_NOTHING, db_column='username', primary_key=True)  # The composite primary key (username, bank_id) found, that is not supported. The first column is selected.
    bank = models.ForeignKey(Banks, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'banks_users'
        unique_together = (('username', 'bank'),)


class Budgets(models.Model):
    budget_id = models.AutoField(primary_key=True)
    username = models.ForeignKey('Users', models.DO_NOTHING, db_column='username')
    category_name = models.TextField()
    monthly_budget = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    annual_budget = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets'


class Users(models.Model):
    username = models.TextField(primary_key=True)
    password = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'
