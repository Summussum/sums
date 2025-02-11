from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Users(models.Model):
    username = models.TextField(primary_key=True)
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
    nickname = models.TextField()
    bank = models.TextField()
    account_owner = models.ForeignKey('Users', models.DO_NOTHING, db_column='account_owner')
    account_type = models.TextField(blank=True, null=True)
    account_last_four = models.IntegerField(blank=True, null=True)
    translator = models.JSONField()
    date_formatter = models.TextField()
    negative_expenses = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'accounts'



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

class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    transaction_date = models.DateField()
    transaction_description = models.TextField(blank=True, null=True)
    budget_id = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    recurring = models.BooleanField(blank=True, null=True)
    account_owner = models.ForeignKey('Users', models.DO_NOTHING, db_column='account_owner')
    account_nickname = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'transactions'

# INSERT INTO users (username, "password", email) VALUES ('test', 'admin123', 'testing@testing.com');