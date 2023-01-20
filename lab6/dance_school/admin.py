from django.contrib import admin

from dance_school.models import Users, Choreographers, Dancers, DanceGroups, DancerVisits, Schedule, Styles, \
    ChoreoStyles, Roles, Permissions, RolePermissions, Logs, Memberships

admin.site.register(Users)
admin.site.register(Choreographers)
admin.site.register(Dancers)
admin.site.register(DanceGroups)
admin.site.register(Logs)
admin.site.register(DancerVisits)
admin.site.register(Styles)
admin.site.register(ChoreoStyles)
admin.site.register(Roles)
admin.site.register(Schedule)
admin.site.register(Permissions)
admin.site.register(RolePermissions)
admin.site.register(Memberships)
