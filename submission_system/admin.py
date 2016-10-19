from django.contrib import admin

# Register your models here.

from submission_system.models import Courser, Homework, HomeworkAnswer


class HomeworkAnswerInline(admin.TabularInline):
    model = HomeworkAnswer


class HomeworkAdmin(admin.ModelAdmin):
    # 配置在list页面显示字段
    list_display = ('name', 'courser')
    list_filter = ('courser',)
    inlines = (HomeworkAnswerInline,)


class HomeworkAnswerAdmin(admin.ModelAdmin):
    list_display = ("homework", 'creator')
    list_filter = ('homework',)


admin.site.register(Courser)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(HomeworkAnswer, HomeworkAnswerAdmin)
