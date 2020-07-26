from django.db import models
from ..userprofiles.models import User
from ..securities.models import Data_Tag, PERIOD_CHOICES
# Create your models here.
class User_Ticker_Tag_Periods(models.Model):
    ticker = models.CharField(max_length=255, db_index=True)
    tag = models.CharField(max_length=25, db_index=True)
    period = models.CharField(max_length=4, choices=PERIOD_CHOICES, default=PERIOD_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name = "tickertags", on_delete=models.CASCADE)

class Watchlist_Head(models.Model):
    name = models.CharField(max_length=255) # The human readable name
    description = models.TextField()
    # wval_1 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wval_2 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wval_3 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wval_4 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wval_5 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wpct_1 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wpct_2 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wpct_3 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wpct_4 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wpct_5 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # wvald1 = models.CharField(max_length=255, default='Value1')
    # wvald2 = models.CharField(max_length=255, default='Value2')
    # wvald3 = models.CharField(max_length=255, default='Value3')
    # wvald4 = models.CharField(max_length=255, default='Value4')
    # wvald5 = models.CharField(max_length=255, default='Value5')
    # wpctd1 = models.CharField(max_length=255, default='Percentage1')
    # wpctd2 = models.CharField(max_length=255, default='Percentage2')
    # wpctd3 = models.CharField(max_length=255, default='Percentage3')
    # wpctd4 = models.CharField(max_length=255, default='Percentage4')
    # wpctd5 = models.CharField(max_length=255, default='Percentage5')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name = "watchlists", on_delete=models.CASCADE)

class Formula(models.Model):
    name = models.CharField(max_length=50)
    col_name = models.CharField(max_length=255, default="Heading") # The human readable name
    formula = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name = "formulas", on_delete=models.CASCADE)

class Watchlist_Cols(models.Model):
    seq = models.FloatField(default=0)
    tag = models.CharField(max_length=25, default="") # The Intrinio Data Tag
    period = models.CharField(max_length=4)
    # formula_name = models.CharField(max_length=50) # Specific data_tag/calculation fields, possibly as simple as a tag
    # test = models.TextField() # A conditional that might be applied to the formula result as a test for filtering or ???
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    watchlist = models.ForeignKey(Watchlist_Head, related_name = "columns", on_delete=models.CASCADE)
    formula = models.ForeignKey(Formula, related_name = "formulas", on_delete=models.PROTECT, null=True)

class Watchlist_Rows(models.Model):
    seq = models.FloatField(default=0)
    ticker = models.CharField(max_length=255) # The human readable name
    target = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tval_1 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tval_2 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tval_3 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tval_4 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tval_5 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tpct_1 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tpct_2 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tpct_3 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tpct_4 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    # tpct_5 = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    watchlist = models.ForeignKey(Watchlist_Head, related_name = "rows", on_delete=models.CASCADE)
