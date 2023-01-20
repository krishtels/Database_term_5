from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import connection
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, RedirectView, ListView
from .models import Dancers, Users, Choreographers, ChoreoStyles, Styles, DanceGroups, Schedule
from .forms import UserCreateForm, UserUpdateForm, ChoreoForm, ChoreoFormSet, ChoreoStyleForm, DancerForm, DancerFormSet, \
    ScheduleCreateForm, DancerVisitForm


class ChoreographersListView(ListView):
    template_name = 'dance_school/choreo_list.html'
    context_object_name = 'choreo_list'

    def get_queryset(self):
        queryset = Users.objects.raw("SELECT user_id, user_name, user_surname FROM users WHERE role_id = (SELECT role_id FROM roles WHERE role_name = 'choreographer')")
        return queryset


class ChoreoDetailView(DetailView):
    model = Choreographers
    template_name = 'dance_school/choreo_detail.html'
    context_object_name = 'choreo_detail'

    def get_context_data(self, **kwargs):
        my_user = self.kwargs['pk']
        context = super(ChoreoDetailView, self).get_context_data(**kwargs)
        choreographer = Choreographers.objects.raw('SELECT choreo_id, user_name, user_surname, date_of_birth, email, salary, phone_number FROM choreographers JOIN users ON choreo_id = user_id WHERE choreo_id = %s', [my_user])
        styles = Styles.objects.raw('SELECT * FROM choreo_styles JOIN styles ON styles.style_id = choreo_styles.style_id WHERE choreo_styles.choreo_id =  %s', [my_user])
        context['choreographer'] = choreographer
        context['styles'] = styles
        return context


class ChoreoCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'dance_school/choreo_create.html'
    success_url = reverse_lazy('choreo_add')
    success_message = 'Хореограф успешно добавлен.'

    def get_context_data(self, **kwargs):
        data = super(ChoreoCreateView, self).get_context_data(**kwargs)
        data['choreo_form'] = ChoreoForm()
        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        choreo_form = ChoreoForm(self.request.POST)
        if form.is_valid() and choreo_form.is_valid():
            user = form.cleaned_data
            choreo = choreo_form.cleaned_data
            params = [user['login'], user['user_password'], user['email'], user['user_name'], user['user_surname'], user['date_of_birth'], choreo['phone_number'], choreo['salary']]
            with connection.cursor() as cursor:
                sql = "CALL add_new_choreo(%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, params)
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form, 'choreo_form': choreo_form})


class ChoreoUpdateView(SuccessMessageMixin, UpdateView):
    model = Users
    queryset = Users.objects.filter(role_id=1)
    form_class = UserUpdateForm
    template_name = 'dance_school/choreo_update.html'
    success_message = 'Данные хореографа успешно обновлены.'

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(self.request.POST)
        choreo_formset = ChoreoFormSet(self.request.POST, prefix='choreo')
        if choreo_formset.is_valid():
            choreo_formset.save()
            return super(ChoreoUpdateView, self).post(self.request.POST)

        else:
            return self.render_to_response(
                {'form': form, 'choreo_form': choreo_formset}
            )

    def get_context_data(self, **kwargs):
        data = super(ChoreoUpdateView, self).get_context_data(**kwargs)
        choreo_formset = ChoreoFormSet(queryset=Choreographers.objects.filter(choreo_id=self.kwargs['pk']), prefix='choreo')

        data['choreo_form'] = choreo_formset
        return data

    def get_success_url(self):
        return reverse_lazy('choreo_update', kwargs={'pk': self.kwargs['pk']})


class ChoreoStyleUpdateView(SuccessMessageMixin, CreateView):
    model = ChoreoStyles
    form_class = ChoreoStyleForm
    template_name = 'dance_school/choreo_style.html'
    success_message = 'Стили хореографа успешно обновлены.'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        my_user = self.kwargs['pk']
        if form.is_valid():
            styles = form.cleaned_data['style_id']
            with connection.cursor() as cursor:
                sql = "INSERT INTO choreo_styles VALUES ((SELECT choreo_id FROM choreographers WHERE choreo_id=%s), (SELECT style_id FROM styles WHERE style_name=%s))"
                for style in styles:
                    params = [my_user, str(style)]
                    try:
                        cursor.execute(sql, params)
                    except:
                        pass
            return self.form_valid(form)

        else:
            return self.render_to_response({'form': form})

    def get_success_url(self):
        return reverse_lazy('choreo_detail', kwargs={'pk': self.kwargs['pk']})


class GroupDanceListView(ListView):
    template_name = 'dance_school/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        queryset = DanceGroups.objects.raw("SELECT * FROM dance_groups")
        return queryset


class GroupDetailView(DetailView):
    model = DanceGroups
    template_name = 'dance_school/group_detail.html'
    context_object_name = 'group_detail'

    def get_context_data(self, **kwargs):
        my_group = self.kwargs['pk']
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        group = DanceGroups.objects.raw('SELECT * FROM dance_groups WHERE group_id = %s', [my_group])
        styles = Styles.objects.raw('SELECT DISTINCT styles.style_id, style_name FROM styles JOIN schedule ON styles.style_id = schedule.style_id WHERE group_id = %s', [my_group])
        dancers = Dancers.objects.raw(('SELECT dancer_id, amount_of_lessons_left, user_name, user_surname from dancers JOIN users ON dancers.dancer_id = user_id WHERE dancers.group_id = %s'), [my_group])
        schedule = Schedule.objects.raw('select * from schedule JOIN styles ON styles.style_id = schedule.style_id  JOIN choreographers ON choreographers.choreo_id = schedule.choreo_id JOIN users ON choreographers.choreo_id = users.user_id WHERE group_id = %s', [my_group])
        context['dancers'] = dancers
        context['group'] = group
        context['styles'] = styles
        context['schedule'] = schedule
        return context


class DancerDetailView(DetailView):
    model = Dancers
    template_name = 'dance_school/dancer_detail.html'
    context_object_name = 'dancer_detail'

    def get_context_data(self, **kwargs):
        my_user = self.kwargs['pk']
        context = super(DancerDetailView, self).get_context_data(**kwargs)
        dancer = Dancers.objects.raw('SELECT dancer_id, group_name, dancers.member_id, price, start_date, end_date, amount_of_lessons, amount_of_lessons_left, login, email, user_name, user_surname, date_of_birth from dancers JOIN users ON dancer_id = user_id JOIN dance_groups ON dancers.group_id = dance_groups.group_id JOIN memberships ON dancers.member_id = memberships.member_id WHERE dance_groups.group_id = %s', [my_user])
        context['dancer'] = dancer
        return context


class DancerCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'dance_school/dancer_create.html'
    success_url = reverse_lazy('dancer_add')
    success_message = 'Танцор успешно добавлен.'

    def get_context_data(self, **kwargs):
        data = super(DancerCreateView, self).get_context_data(**kwargs)
        data['dancer_form'] = DancerForm()
        return data


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        dancer_form = DancerForm(self.request.POST)
        if form.is_valid() and dancer_form.is_valid():
            user = form.cleaned_data
            dancer = dancer_form.cleaned_data
            group = dancer['group']
            member = dancer['member']
            params = [user['login'], user['user_password'], user['email'], user['user_name'], user['user_surname'],
                      user['date_of_birth'], group.group_name, member.member_id]
            with connection.cursor() as cursor:
                sql = "CALL add_new_dancer(%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, params)
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form, 'dancer_form': dancer_form})


class DancerUpdateView(SuccessMessageMixin, UpdateView):
    model = Users
    queryset = Users.objects.filter(role_id=2)
    form_class = UserUpdateForm
    template_name = 'dance_school/dancer_update.html'
    success_message = 'Данные танцора успешно обновлены.'

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(self.request.POST)
        dancer_formset = DancerFormSet(self.request.POST, prefix='dancer')
        if dancer_formset.is_valid():
            dancer_formset.save()
            return super(DancerUpdateView, self).post(self.request.POST)
        else:
            return self.render_to_response(
                {'form': form, 'student_form': dancer_formset}
            )

    def get_context_data(self, **kwargs):
        data = super(DancerUpdateView, self).get_context_data(**kwargs)
        dancer_formset = DancerFormSet(queryset=Dancers.objects.filter(dancer_id=self.kwargs['pk']), prefix='dancer')

        data['dancer_form'] = dancer_formset
        return data

    def get_success_url(self):
        return reverse_lazy('dancer_update', kwargs={'pk': self.kwargs['pk']})


class UserTypeRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('choreo_list')


class ScheduleCreateView(CreateView):
    form_class = ScheduleCreateForm
    template_name = 'dance_school/schedule_create.html'
    success_message = 'Занятие успешно добавлено.'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid() :
            schedule = form.cleaned_data
            group = schedule['group']
            style = schedule['style']
            user = schedule['user']
            class_length = schedule['class_length']
            is_completed = schedule['is_completed']
            datetime = schedule['date_time']
            params = [style.style_name, group.group_name, user.login, class_length, is_completed, datetime]
            with connection.cursor() as cursor:
                sql = "INSERT INTO schedule (style_id, group_id, choreo_id, class_length, is_completed, date_time) VALUES ((SELECT style_id FROM styles WHERE style_name = %s), (SELECT group_id FROM dance_groups WHERE group_name = %s),  (SELECT user_id FROM users WHERE login = %s), %s, %s, %s)"
                cursor.execute(sql, params)
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form})

    def get_success_url(self):
        form = self.get_form()
        if form.is_valid():
            schedule = form.cleaned_data
            group = schedule['group']
            groups = DanceGroups.objects.raw("SELECT * FROM dance_groups WHERE group_name = %s", [group.group_name])
            group_id = 1
            for gr in groups:
                group_id = gr.group_id
            lessons = Schedule.objects.raw("SELECT * FROM schedule")
            for les in lessons:
                lesson_id = les.lesson_id
            return reverse_lazy('dancer_visit', kwargs={'group_id': group_id, 'lesson_id': lesson_id})



class DancerVisitView(CreateView):
    template_name = 'dance_school/dancer_visit.html'
    success_url = reverse_lazy('group_list')
    success_message = 'Занятие успешно добавлено.'
    form_class = DancerVisitForm

    def get(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        form = DancerVisitForm(group_id=group_id)
        context = {'form': form}

        return render(request, "dance_school/dancer_visit.html", context)

    def post(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        form = self.form_class(group_id, request.POST)

        if form.is_valid():
            dancer_visit = form.cleaned_data
            users = dancer_visit['dancers']
            with connection.cursor() as cursor:
                sql = "INSERT INTO dancer_visits VALUES (%s, %s)"
                lesson_id = self.kwargs['lesson_id']
                for user in users:
                    params = [user.user_id, lesson_id]
                    try:
                        cursor.execute(sql, params)
                    except:
                        pass
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form})