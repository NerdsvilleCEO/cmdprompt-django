from django.contrib import admin
from pgweb.util.admin import PgwebAdmin
from models import TeamMember, AboutContentBlock, Career

class TeamMemberAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('title',)


admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(AboutContentBlock)
admin.site.register(Career)
