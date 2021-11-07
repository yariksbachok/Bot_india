from django.db import models


class History(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    payments = models.TextField(blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HISTORY'


class User(models.Model):
    id = models.IntegerField(blank=True, null=True)
    address_wallet = models.TextField(blank=True, null=True)
    balance_invest = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    first_referal = models.IntegerField(blank=True, null=True)
    second_referal = models.IntegerField(blank=True, null=True)
    three_referal = models.IntegerField(blank=True, null=True)
    four_referal = models.IntegerField(blank=True, null=True)
    five_referal = models.IntegerField(blank=True, null=True)
    progres = models.IntegerField(blank=True, null=True)
    laung = models.TextField(blank=True, null=True)
    address_btc = models.TextField(blank=True, null=True)
    address_eth = models.TextField(blank=True, null=True)
    id_user = models.AutoField(primary_key=True, blank=True)

    class Meta:
        managed = False
        db_table = 'USER'
        verbose_name = 'USER'
        verbose_name_plural = 'USERS'

    def __str__(self):
        return f'ID: {self.id}'


class TodayProc(models.Model):
    id = models.IntegerField(blank=True, primary_key=True)
    all_sum = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'today_proc'
