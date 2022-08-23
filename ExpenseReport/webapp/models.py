from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    '''カスタムUserManager
    ターミナルでユーザーを作成するときに使用（manage.py createsuperuser）
    '''
    use_in_migrations = True

    def _create_user(self, username, password=None, **extra_fields):
        username = self.model.normalize_username(username)
        user = self.model(username=username,  **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります。')
        return self._create_user(username,  password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    '''アカウントテーブル
    ユーザモデルを拡張したクラス
    '''

    account_id = models.CharField(verbose_name="アカウントID", max_length=255,primary_key=True)
    username = models.CharField(verbose_name="氏名",max_length=50,blank=True)
    # 管理画面のログイン許可
    is_staff = models.BooleanField(default=False)
    # Webアプリへのログイン許可
    is_active = models.BooleanField(default=True)

    # objects変数に指定するクラスは、ターミナルでユーザーを作成する際に呼ばれる。
    objects = UserManager()

    # ここで指定したフィールドはログイン認証やメール送信などで利用される
    USERNAME_FIELD = "account_id"
    # ターミナルでユーザー作成するときに入力する項目
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        db_table = "Account"


class Transportation(models.Model):
    '''交通機関テーブル
    参照用テーブル
    '''
    transportation = models.CharField(verbose_name="交通機関", max_length=255,unique=True)
    
    def __str__(self) -> str:
        return self.transportation

    class Meta:
        db_table = "Transportation"


class Subjects(models.Model):
    '''科目テーブル(経費種別)
    参照用テーブル
    '''
    subjects = models.CharField(verbose_name="科目", max_length=255,unique=True)
    
    def __str__(self) -> str:
        return self.subjects

    class Meta:
        db_table = "Subjects"


class Route(models.Model):
    '''経路テーブル'''
    departure_point = models.CharField(verbose_name="出発地点", max_length=255)
    arrival_point = models.CharField(verbose_name="到着地点", max_length=255)
    transportation = models.ForeignKey(Transportation,to_field='transportation',on_delete=models.PROTECT,verbose_name="交通手段")
    fare = models.IntegerField(verbose_name="金額",default=0)
    account = models.ForeignKey(Account,on_delete=models.PROTECT,verbose_name="アカウントID")

    def __str__(self) -> str:
        return self.departure_point + " → " + self.arrival_point

    def get_fare(self):
        return self.fare

    class Meta:
        db_table = "Route"


class ExpenseReport(models.Model):
    payment_date = models.DateField(verbose_name="日付")
    subjects = models.ForeignKey(Subjects,to_field='subjects',on_delete=models.PROTECT,verbose_name="科目")
    partner = models.CharField(verbose_name="相手", max_length=255)
    purpose = models.CharField(verbose_name="目的", max_length=255)
    route = models.ForeignKey(Route,on_delete=models.PROTECT,verbose_name="経路")
    lap = models.IntegerField("往復",choices=[[1,'片道'],[2,'往復']])
    account = models.ForeignKey(Account,on_delete=models.PROTECT,verbose_name="アカウントID")

    def __str__(self) -> str:
        return self.partner

    class Meta:
        db_table = "Report"