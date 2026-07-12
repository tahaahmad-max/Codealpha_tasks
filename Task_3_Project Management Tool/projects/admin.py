from django.contrib import admin
from .models import Project, ProjectMember


class ProjectMemberInline(admin.TabularInline):
    """Show members inline on the project admin page."""
    model = ProjectMember
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'get_task_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'owner__username']
    inlines = [ProjectMemberInline]

    def get_task_count(self, obj):
        return obj.get_task_count()
    get_task_count.short_description = 'Tasks'


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'joined_at']
    list_filter = ['role']
    search_fields = ['user__username', 'project__name']
