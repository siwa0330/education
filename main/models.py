from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

class User(AbstractUser):
    #用户类型
    #1: 超管 | 1000: 普通管理员 | 2000: 普通用户
    #usertype = models.PositiveIntegerField()

    #用户类型
    #1.老师 | 2.学生
    typechoice = ((1, '老师'), (2, '学生'))
    usertype = models.CharField(max_length=10, choices=typechoice)

    #真实姓名
    realname = models.CharField(max_length=30, db_index=True)



    #工号|学号
    workid = models.CharField(
        max_length=10,
        db_index=True,
        null=True, blank=True
    )
    #所属学院
    #1.经济 #2. 计算机
    collegechoice = ((1, '经济'), (2, '计算机'))
    collegetype = models.CharField(max_length=10, choices=collegechoice)

    #备注描述
    desc = models.CharField(max_length=500, null=True, blank=True)

    REQUIRED_FIELDS = ['usertype', 'realname']

    class Meta:
        #设置数据库表名
        db_table = 'lessons_user'

class lesson(models.Model):
    #课程名称
    title = models.CharField(max_length=60)
    #所属学院
    collegechoice = ((1, '经济'), (2, '计算机'))
    collegetype = models.CharField(max_length=10, choices=collegechoice)
    #课程简介
    desc = models.CharField(max_length=500, null=True, blank=True)
    #任课教师（外键：关联user表）
    teacher = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        #设置数据库表名
        db_table = 'lessons_lesson'

class user2lesson(models.Model):
    uit = models.ForeignKey('User', related_name='uit', on_delete=models.CASCADE)
    lid = models.ForeignKey('lesson', related_name='lid', on_delete=models.CASCADE)
