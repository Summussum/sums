from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User




# Create your models here.


class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    nickname = models.TextField()
    bank = models.TextField()
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id')
    account_type = models.TextField(blank=True, null=True)
    account_last_four = models.IntegerField(blank=True, null=True)
    translator = models.JSONField()
    date_formatter = models.TextField()




class Budgets(models.Model):
    budget_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id')
    category_name = models.TextField()
    category_display = models.TextField()
    monthly_budget = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    annual_budget = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)



class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    transaction_date = models.DateField()
    transaction_description = models.TextField(blank=True, null=True)
    budget_id = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    recurring = models.BooleanField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id')
    account_nickname = models.TextField()
    


class Snapshots(models.Model):
    snapshot_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id')
    snapshot_year = models.SmallIntegerField()
    snapshot_month = models.SmallIntegerField()
    snapshot_budget = models.JSONField()
    snapshot_expenses = models.JSONField()





# INSERT INTO User (username, "password", email) VALUES ('test', 'admin123', 'testing@testing.com');