from django.db import models

# Create your models here.
from auth_system.models import MyUser


class Courser(models.Model):
    name = models.CharField(max_length=20, verbose_name='课程名称')
    name_en = models.CharField(max_length=50, verbose_name='英文名称', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'


class Homework(models.Model):
    courser = models.ForeignKey(Courser, verbose_name='课程')
    name = models.CharField(max_length=50, verbose_name='作业标题')
    content = models.TextField(verbose_name='详细(以md形式保存)', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作业'
        verbose_name_plural = '作业'


class HomeworkAnswer(models.Model):
    homework = models.ForeignKey(Homework, verbose_name='所属作业')
    content = models.TextField(verbose_name='详细', null=True, blank=True)
    creator = models.ForeignKey(MyUser, verbose_name='用户', null=True, blank=True)
    code = models.TextField(verbose_name='代码', null=True, blank=True)
    picture = models.FileField(verbose_name="上传的图", null=True, blank=True)

    def __str__(self):
        return self.creator.username + ' 提交的 ' + self.homework.name + ' 答案 '

    class Meta:
        verbose_name = "提交的作业"
        verbose_name_plural = "提交的作业"
