from django.db import models


class ChoreoStyles(models.Model):
    choreo = models.ForeignKey('Choreographers', models.DO_NOTHING)
    style = models.ForeignKey('Styles', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'choreo_styles'


class Choreographers(models.Model):
    choreo = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    salary = models.FloatField()

    class Meta:
        managed = False
        db_table = 'choreographers'


class DanceGroups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(unique=True, max_length=50)
    vacant_place = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dance_groups'

    def __str__(self):
        return self.group_name


class DancerVisits(models.Model):
    dancer = models.ForeignKey('Dancers', models.DO_NOTHING)
    lesson = models.ForeignKey('Schedule', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dancer_visits'


class Dancers(models.Model):
    dancer = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    group = models.ForeignKey(DanceGroups, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey('Memberships', models.DO_NOTHING, blank=True, null=True)
    amount_of_lessons_left = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dancers'


class Logs(models.Model):
    log_id = models.AutoField(primary_key=True)
    log_date = models.DateTimeField()
    log_info = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'logs'


class Memberships(models.Model):
    member_id = models.AutoField(primary_key=True)
    price = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    amount_of_lessons = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'memberships'

    def __str__(self):
        return str(self.member_id)


class Permissions(models.Model):
    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'permissions'


class RolePermissions(models.Model):
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    permission = models.ForeignKey(Permissions, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'role_permissions'


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'roles'


class Schedule(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    style = models.ForeignKey('Styles', models.DO_NOTHING)
    group = models.ForeignKey(DanceGroups, models.DO_NOTHING)
    choreo = models.ForeignKey(Choreographers, models.DO_NOTHING)
    class_length = models.FloatField()
    is_completed = models.BooleanField()
    date_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'schedule'


class Styles(models.Model):
    style_id = models.AutoField(primary_key=True)
    style_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'styles'

    def __str__(self):
        return self.style_name


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING, blank=True, null=True)
    login = models.CharField(unique=True, max_length=50)
    user_password = models.CharField(max_length=128)
    email = models.CharField(unique=True, max_length=128)
    user_name = models.CharField(max_length=50)
    user_surname = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'login'

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        str = self.user_surname + ' ' + self.user_name
        return str
