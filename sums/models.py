from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User




# Create your models here.


class Accounts(models.Model):
    account_id = models.AutoField(primary_key=True)
    nickname = models.TextField()
    bank = models.TextField()
    user = models.ForeignKey(User, models.CASCADE)
    account_type = models.TextField(blank=True, null=True)
    account_last_four = models.IntegerField(blank=True, null=True)
    translator = models.JSONField()
    date_formatter = models.TextField()




class Budgets(models.Model):
    budget_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    category_name = models.TextField()
    category_display = models.TextField()
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    annual_budget = models.BooleanField(default=False)
    keywords = models.JSONField(null=True, blank=True)



class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    transaction_date = models.DateField()
    transaction_description = models.TextField(blank=True, null=True)
    budget= models.ForeignKey(Budgets, models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    recurring = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey(User, models.CASCADE)
    account = models.ForeignKey(Accounts, models.CASCADE)
    auto_assigned = models.BooleanField(default=False)
    


class Snapshots(models.Model):
    snapshot_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    snapshot_year = models.SmallIntegerField()
    snapshot_month = models.SmallIntegerField()
    snapshot_budget = models.JSONField()
    snapshot_expenses = models.JSONField()
