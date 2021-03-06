from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from smart_selects.db_fields import GroupedForeignKey
from django.db import models

# Create your models here.

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('项目名称', max_length=50, unique=True, null=False)
    proj_owner = models.CharField('项目负责人', max_length=20, null=False)
    test_owner = models.CharField('测试负责人', max_length=20, null=False)
    dev_owner = models.CharField('开发负责人', max_length=20, null=False)
    desc = models.CharField('项目描述', max_length=100, null=True)
    create_time = models.DateTimeField('项目创建时间', auto_now_add=True)
    update_time = models.DateTimeField('项目更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目信息表'
        verbose_name_plural = '项目信息表'

class Module(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('模块名称', max_length=50, null=False)
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    test_owner = models.CharField('测试负责人', max_length=50, null=False)
    desc = models.CharField('简要描述', max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '模块信息表'
        verbose_name_plural = '模块信息表'


class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('测试用例名称', max_length=50, null=False)
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    belong_module = GroupedForeignKey(Module, "belong_project", on_delete=models.CASCADE, verbose_name='所属模块')
    #belong_module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name='所属模块')
    author = models.CharField('编写人员', max_length=20, null=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='所属用户',null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = '测试用例表'

class KeyWord(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('关键字名称',max_length=300, null=False)
    params = models.CharField('关键字参数说明',max_length=300, null=True)
    desc = models.TextField('关键字用途描述',null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "关键字表"
        verbose_name_plural = '关键字表'

class CaseStep(models.Model):
    id = models.AutoField(primary_key=True)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='用例名称')
    test_step_no = models.CharField('测试步聚序号', max_length=200)  # 测试步聚
    desc = models.CharField('测试步骤描述', max_length=200, blank=True, null=True)  # 测试对象名称描述
    key_word = models.ForeignKey(KeyWord, on_delete=models.CASCADE, blank=True, null=True, verbose_name='操作关键字')  # 操作方法
    locator_method = models.CharField('定位方式', max_length=200, blank=True, null=True)  # 定位方式
    locator_exp = models.CharField('定位表达式', max_length=800, blank=True, null=True)  # 控件元素
    test_data = models.CharField('测试数据值', max_length=200, blank=True, null=True)  # 测试数据
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    def __str__(self):
        return self.test_step_no

    class Meta:
        verbose_name = '测试用例步骤表'
        verbose_name_plural = '测试用例步骤表'


class TestCaseExecuteRecord(models.Model):
    id = models.AutoField(primary_key=True)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='测试用例')
    status = models.IntegerField(null=True, help_text="0：表示未执行，1：表示已执行")
    result = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    exception_info= models.CharField(max_length=500, blank=True, null=True)
    capture_screen = models.CharField(max_length=500, blank=True, null=True)
    execute_start_time = models.CharField('执行开始时间', max_length=300, blank=True, null=True)
    execute_end_time = models.CharField('执行结束时间', max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.id)


    class Meta:
        verbose_name = "测试用例结果记录表"
        verbose_name_plural = '测试用例结果记录表'

class TestCaseStepExecuteRecord(models.Model):
    id = models.AutoField(primary_key=True)
    test_case_execute_record = models.ForeignKey(TestCaseExecuteRecord, on_delete=models.CASCADE, verbose_name='执行id')
    case_step = models.ForeignKey(CaseStep, on_delete=models.CASCADE, verbose_name='测试步骤id')
    result = models.CharField('执行结果',max_length=100, blank=True, null=True)
    exception_info= models.CharField(max_length=500, blank=True, null=True)
    capture_screen = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "测试用例步骤执行结果表"
        verbose_name_plural = '测试用例步骤执行结果表'   


        
class ModuleInline(admin.TabularInline):
    model = Module

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]  # Inline
    list_display = ("id","name","proj_owner","test_owner","dev_owner","desc","create_time","update_time")

class TestCaseInline(admin.TabularInline):
    model = TestCase
    
class ModuleAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]  # Inline  
    list_display = ("id","name","belong_project","test_owner","desc","create_time","update_time") 

class CaseStepInline(admin.TabularInline):
    model = CaseStep  

class TestCaseAdmin(admin.ModelAdmin):
    inlines  = [CaseStepInline]
    list_display = ("id","name","belong_project","belong_module","author","user","create_time","update_time") 

class CaseStepAdmin(admin.ModelAdmin):
    list_display = ("id","test_case","test_step_no","key_word","locator_method","locator_exp","test_data","create_time")

class KeyWordAdmin(admin.ModelAdmin):
    list_display = ("id","name","params","desc","create_time","update_time")       

class TestSuit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    creator = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    class Meta:
        verbose_name = "测试集合"
        verbose_name_plural = '测试集合'

class TestSuitTestCases(models.Model):
    id = models.AutoField(primary_key=True)
    test_suit = models.ForeignKey(TestSuit, on_delete=models.CASCADE, verbose_name='测试集合')   
    test_case= models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='测试用例')   
    is_active = models.IntegerField(verbose_name='是否有效',null=False,default=1)
    create_time = models.DateTimeField('创建时间', auto_now=True)  #创建时间-自动获取当前时间    

class TestSuitExecuteRecord(models.Model):
    id = models.AutoField(primary_key=True)
    test_suit= models.ForeignKey(TestSuit, on_delete=models.CASCADE, verbose_name='测试集合')   
    run_time_interval = models.IntegerField(verbose_name='延迟时间',null=True,default=0)
    status= models.IntegerField(verbose_name='执行状态',null=True,default=0)
    test_result = models.CharField(max_length=50, blank=True, null=True)
    creator = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)  #创建时间-自动获取当前时间
    execute_start_time = models.CharField('执行开始时间', max_length=300, blank=True, null=True)    

class TestSuitTestCaseExecuteRecord(models.Model):
    id = models.AutoField(primary_key=True)
    test_suit_record = models.ForeignKey(TestSuitExecuteRecord, on_delete=models.CASCADE, verbose_name='执行的测试集合执行记录')   
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, verbose_name='执行的测试用例')   
    test_result = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(verbose_name='执行状态',null=True,default=0)
    exception_info= models.CharField(max_length=500, blank=True, null=True)
    capture_screen = models.CharField(max_length=500, blank=True, null=True)    
    execute_start_time = models.CharField('执行开始时间', max_length=300, blank=True, null=True)
    execute_end_time = models.CharField('执行结束时间', max_length=300, blank=True, null=True) 

class TestSuitTestStepExecuteRecord(models.Model):
    id = models.AutoField(primary_key=True)
    test_case_record = models.ForeignKey(TestSuitTestCaseExecuteRecord, on_delete=models.CASCADE, verbose_name='测试用例')
    step_id = models.ForeignKey(CaseStep, on_delete=models.CASCADE, verbose_name='测试步骤id')
    step_desc = models.CharField(max_length=300, null=False)
    result = models.CharField('执行结果',max_length=100, blank=True, null=True)
    exception_info= models.CharField(max_length=500, blank=True, null=True)
    capture_screen = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "用例步骤执行结果表"
        verbose_name_plural = '用例步骤执行结果表'

class TestSuitAdmin(admin.ModelAdmin):
    list_display = ("id","name","creator","create_time")  
