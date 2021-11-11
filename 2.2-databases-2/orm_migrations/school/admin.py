from django.contrib import admin

from .models import Student, Teacher


class StudentsInline(admin.TabularInline):
    model = Teacher.students.through


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')
    list_display_links = ('id', 'name')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject')
    list_display_links = ('id', 'name')
    inlines = (StudentsInline, )
