from django.urls import path
from . import views

# app_name = 'shift'

urlpatterns = [
    path('shift_create/', views.shift_create, name='shift_create'),
    # 月間カレンダー表示
    path('', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/<int:day>', views.MonthCalendar.as_view(), name='month'),
    #月間カレンダーschedule
    path(
        'user/<int:user_pk>/month_with_schedule/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'user/<int:user_pk>/month_with_schedule/<int:year>/<int:month>/<int:day>',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    # 月間カレンダーform
    path(
        'user/<int:user_pk>/month_with_forms/',
        views.MonthWithFormsCalendar.as_view(), name='month_with_forms'
    ),
    path(
        'user/<int:user_pk>/month_with_forms/<int:year>/<int:month>/<int:day>',
        views.MonthWithFormsCalendar.as_view(), name='month_with_forms'
    ),
]