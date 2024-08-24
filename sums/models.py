from __future__ import unicode_literals
from django.db import models
from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Users(models.Model):
    username = models.TextField(primary_key=True)
    passwd = models.TextField()
    email = models.TextField()


    class Meta:
        managed = False
        db_table = 'users'
    
    def validate_user(self, username, password):
        if self.password == password and self.username == username:
            return True
        else:
            return False


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
    category_display = models.TextField()
    monthly_budget = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    annual_budget = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'budgets'


