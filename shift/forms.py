import datetime as dt
from django import forms
from .models import Shift

HOUR_CHOICES = [(dt.time(hour=x, minute=y), '{:02d}:{:02d}'.format(x, y)) for x in range(7, 24) for y in [00, 30]] + [(dt.time(hour=x, minute=y), '{:02d}:{:02d}'.format(x+24, y)) for x in range(0,4) for y in [00, 30]]



class ShiftCreateForm(forms.ModelForm):
    class Meta:
        model = Shift
        # exclude = ['user', 'create_at', 'description']
        fields = ('is_work', 'start_time', 'end_time', 'date',) 
        widgets = {
            'start_time': forms.Select(choices=HOUR_CHOICES),
            'end_time': forms.Select(choices=HOUR_CHOICES),
            'date': forms.HiddenInput,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']

        # 特殊時間
        if start_time.hour >= 0 and start_time.hour <=3:
            if end_time.hour >= 7 and end_time.hour <= 24:
                raise forms.ValidationError(
                    '終了時間は、開始時間よりも後にしてください'
                )
            elif end_time <= start_time:
                raise forms.ValidationError(
                    '終了時間は、開始時間よりも後にしてください'
                )
        # 平常時間
        if end_time.hour >= 0 and end_time.hour <= 3:
            return end_time
        elif end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )

        return end_time

    # def is_work_save(self):
    #     start_time = self.cleaned_data['start_time']