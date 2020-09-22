from django.db import models
from django.contrib.auth.models import User
# from djchoices import DjangoChoices, ChoiceItem

#choices
# ? [<DB value>,<display value>]
GENDER_CHOICES = [
    ('1','男性'),
    ('2','女性'),
    ('3','その他'),
]


SECTION_CHOICES = [
    ('1','フロント'),
    ('2','ショップ'),
    ('3','ボックス'),
    ('4','コンセ'),
    ('5','映写'),
    ('6','早朝清掃')
]

DUTIES_CHOICES = [
    ('1','リーダー'),
    ('2','ベテラン'),
    ('3','新人'),
]

# Create your models here.
class Section(models.Model):
    name = models.CharField(max_length=1, choices=SECTION_CHOICES)

    def __str__(self):
        return self.name 


class Account(models.Model):
    """ アカウント情報 """

    # class GenderType(DjangoChoices):
    #     men = ChoiceItem(0,'男性')
    #     women = ChoiceItem(1, '女性')
    #     other = ChoiceItem(2, 'その他')

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(verbose_name='名前', max_length=50)
    section = models.ManyToManyField(Section, verbose_name='セクション', blank=True)
    gender = models.CharField(verbose_name='性別', max_length=1, choices=GENDER_CHOICES, default='1')
    duties =  models.CharField(verbose_name='役職', max_length=1, choices=DUTIES_CHOICES, default='3')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('account_detail', kwargs={'pk': self.pk})

# TODO imageは更新ページ用UpdateView




# ? choicesのディスプレイ値を取り出すには,テンプレートで {{object.get_fieldName_display}}