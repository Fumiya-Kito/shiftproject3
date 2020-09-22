import calendar
from collections import deque
import datetime
import itertools
from django import forms
from .models import Shift

class BaseCalendarMixin:
    first_weekday = 5 #土曜始まり
    week_names = ['月', '火', '水', '木', '金', '土', '日']

    def setup_calendar(self):
        # ? calendar.Calendarクラスのインスタンス化
        # ? monthdatescalendarメソッドの利用：first_weekdayの対応を行っている
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        # ? dequeを使ってfirst_weekdayからweek_namesをシフトする。
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names


class MonthCalendarMixin(BaseCalendarMixin):
    # 月間カレンダー機能 Mixin
    def get_previous_half(self, date):
        # 前月を返す
        # ? dateオブジェクトはわかるけどなぜ、datetime.dateじゃないんだろ？
        if date.day <= 15:
            if date.month == 1:
                return date.replace(year=date.year-1, month=12, day=16)
            else:
                return date.replace(month=date.month-1, day=16)
        else:
            return date.replace(month=date.month, day=1)
    
    def get_next_half(self, date):
        # 次を返す
        if date.day > 15:
            if date.month == 12:
                return date.replace(year=date.year+1, month=1, day=1)
            else:
                return date.replace(month=date.month+1, day=1)    
        else:
            return date.replace(month=date.month, day=16)
    
    def get_half_days(self, date):
        # 月の前半の日を返す
        if date.day<=15:
            return [self._calendar.monthdatescalendar(date.year, date.month)[i] for i in range(3)]
        return [self._calendar.monthdatescalendar(date.year, date.month)[i] for i in range(2,5)]
        

    def get_current_month(self):
        # 現在の月を返す
        day = self.kwargs.get('day')
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year and day:
            month = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        # 月間カレンダー情報の入った辞書を返す
        self.setup_calendar()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'month_half_days': self.get_half_days(current_month),
            'month_current': current_month,
            'half_previous': self.get_previous_half(current_month),
            'half_next': self.get_next_half(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data


class MonthWithFormsMixin(MonthCalendarMixin):
    
    #TODO コピペして、新規用と更新用フォームを別で作る。templateの方で分岐or 新しいページを作る

    def get_month_forms(self, start, end, days):
        # TODO それぞれの日と紐づいたformを作成
        lookup = {
            '{}__range'.format(self.date_field): (start, end),
            'user__pk': self.kwargs.get('user_pk'),
            # 'start_time__icontains' : self.time_field ,
        }
        queryset = self.model.objects.filter(**lookup)
        # queryset = self.model.objects.all()
        days_count = sum(len(week) for week in days)
        FormClass = forms.modelformset_factory(self.model, self.form_class, extra=days_count)
        if self.request.method == 'POST':
            formset = self.month_formset = FormClass(self.request.POST, queryset=queryset)
        else:
            formset = self.month_formset = FormClass(queryset=queryset)

        # {1日のdatetime: 1日に関連するフォーム, 2日のdatetime: 2日のフォーム...}のような辞書を作る
        day_forms = {day: [] for week in days for day in week}

        # 各日に、新規作成用フォームを1つずつ配置
        # zip()は2つのリストを同時にfor分で回す。indexが揃っているものが対応して出てくる
        for empty_form, (date, empty_list) in zip(formset.extra_forms, day_forms.items()):
            # 更新用フォームがないときだけ、新規フォームを配置
            empty_form.initial = {self.date_field: date}
            empty_list.append(empty_form)

        # スケジュールがある各日に、そのスケジュールの更新用フォームを配置
        for bound_form in formset.initial_forms:
            instance = bound_form.instance
            date = getattr(instance, self.date_field)
            day_forms[date].append(bound_form)

        # # スケジュールがある各日に、そのスケジュールの更新用フォームを配置
        # for bound_form in formset.initial_forms:
        #     instance = bound_form.instance
        #     date = getattr(instance, self.date_field)
        #     day_forms[date].append(bound_form)

        # # 各日に、新規作成用フォームを配置
        # for empty_form, (date, form_list) in zip(formset.extra_forms, day_forms.items()):
        #     # 更新用フォームがないときだけ、新規フォームを配置
        #     if not form_list:
        #         empty_form.initial = {self.date_field: date}
        #         form_list.append(empty_form)

        

        # day_forms辞書を、周毎に分割する。[{1日: 1日のフォーム...}, {8日: 8日のフォーム...}, ...]
        # 7個ずつ取り出して分割しています。
        return [{key: day_forms[key] for key in itertools.islice(day_forms, i, i+7)} for i in range(0, days_count, 7)]




    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_half_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_context['month_day_forms'] = self.get_month_forms(
            month_first,
            month_last,
            month_days
        )
        calendar_context['month_formset'] = self.month_formset
        return calendar_context

    
class MonthWithScheduleMixin(MonthCalendarMixin):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def get_month_schedules(self, start, end, days):
        """それぞれの日とスケジュールを返す"""
        lookup = {
            # '例えば、date__range: (1日, 31日)'を動的に作る
            '{}__range'.format(self.date_field): (start, end),
            'user__pk': self.kwargs.get('user_pk'),
        }
        # 例えば、Schedule.objects.filter(date__range=(1日, 31日)) になる
        queryset = self.model.objects.filter(**lookup)

        # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for week in days for day in week}
        for schedule in queryset:
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)

        # day_schedules辞書を、周毎に分割する。[{1日: 1日のスケジュール...}, {8日: 8日のスケジュール...}, ...]
        # 7個ずつ取り出して分割しています。
        size = len(day_schedules)
        return [{key: day_schedules[key] for key in itertools.islice(day_schedules, i, i+7)} for i in range(0, size, 7)]

    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_half_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_context['month_day_schedules'] = self.get_month_schedules(
            month_first,
            month_last,
            month_days
        )
        return calendar_context