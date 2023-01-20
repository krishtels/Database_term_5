from django import forms
from django.core import validators
from django.db.models import QuerySet
from django.db.models.expressions import RawSQL
from django.forms import modelformset_factory

from dance_school.models import Users, Choreographers, Dancers, Styles, ChoreoStyles, DanceGroups, Memberships, Schedule


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'user_password', 'email', 'user_name', 'user_surname',
                  'date_of_birth']
        widgets = {
                   'login': forms.TextInput(attrs={'placeholder': 'Логин пользователя'}),
                   'user_password': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
                   'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
                   'user_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
                   'user_surname': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                   'date_of_birth': forms.DateInput(attrs={'placeholder': 'Дата рождения', 'type': 'date'}),
                   }

    def save(self, commit=False):
        user = super(UserCreateForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['login', 'email', 'user_name', 'user_surname',
                  'date_of_birth']
        widgets = {'role': forms.Select(attrs={'placeholder': 'Роль'}),
                   'login': forms.TextInput(attrs={'placeholder': 'Логин пользователя'}),
                   'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
                   'user_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
                   'user_surname': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                   'date_of_birth': forms.DateInput(attrs={'placeholder': 'Дата рождения', 'type': 'date'}),
                   }


class DancerForm(forms.ModelForm):
    class Meta:
        model = Dancers
        group = forms.ModelChoiceField(queryset=DanceGroups.objects.all(), to_field_name='group_name')
        member = forms.ModelChoiceField(queryset=Memberships.objects.all(), to_field_name='price')
        fields = ('group', 'member')


class ChoreoForm(forms.ModelForm):
    class Meta:
        model = Choreographers
        phone_number = forms.CharField(
            max_length=15,
            validators=[validators.RegexValidator(regex=r'^[+][-\s0-9]+$',
                                                  message='Введите номер телефона')],
            widget=forms.Textarea
        )
        salary = forms.CharField(
            max_length=10,
            validators=[validators.RegexValidator(regex=r'[0-9]+\.?[0-9]*',
                                                  message='Заработная плата должна быть числом')],
            widget=forms.Textarea
        )
        fields = ('phone_number', 'salary')


class ChoreoStyleForm(forms.ModelForm):
    style_id = forms.ModelMultipleChoiceField(queryset=Styles.objects.all(), to_field_name='style_name')

    class Meta:
        model = Styles
        fields = ['style_id']

    def save(self, commit=False):
        style_id = super(ChoreoStyleForm, self).save(commit=False)
        if commit:
            style_id.save()
        return style_id


DancerFormSet = modelformset_factory(Dancers, form=DancerForm, max_num=1, extra=1)
ChoreoFormSet = modelformset_factory(Choreographers, form=ChoreoForm, max_num=1, extra=1)


class ScheduleCreateForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=DanceGroups.objects.all(), to_field_name='group_name')
    style = forms.ModelChoiceField(queryset=Styles.objects.all(), to_field_name='style_name')
    user = forms.ModelChoiceField(queryset=Users.objects.filter(role_id=1), to_field_name='user_surname')
    CHOICES_BOOL = ((True, 'Yes'), (False, 'No'),)
    CHOICES_LENGTH = ((1, '1 час'), (1.5, '1.5 часа'), (2, '2 часа'), (2.5, '2.5 часа'), (3, '3 часа'),)
    is_completed = forms.ChoiceField(choices=CHOICES_BOOL)
    class_length = forms.ChoiceField(choices=CHOICES_LENGTH)

    class Meta:
        model = Schedule
        fields = ['group', 'style', 'user', 'class_length', 'is_completed',
                  'date_time']
        widgets = {
                   'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                   }

    def save(self, commit=False):
        style_id = super(ScheduleCreateForm, self).save(commit=False)
        if commit:
            style_id.save()
        return style_id


class DancerVisitForm(forms.ModelForm):
    dancers = forms.ModelMultipleChoiceField(queryset=Users.objects.all())

    def __init__(self, group_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        raw_query = Users.objects.filter(user_id__in=RawSQL('select user_id from users join dancers on user_id = dancer_id where group_id = %s', [group_id]))
        self.fields['dancers'] = forms.ModelMultipleChoiceField(queryset=raw_query)

    class Meta:
        model = Schedule
        fields = ['dancers']

    def save(self, commit=False):
        style_id = super(DancerVisitForm, self).save(commit=False)
        if commit:
            style_id.save()
        return style_id

