from django.db.models.signals import pre_save,post_save

def pre_save_func(sender,**kwargs):

    print("pre_save_func")
    print("pre_save_msg:",sender,kwargs)

def post_save_func(sender,**kwargs):
    print("post_save_func")
    print("post_save_msg:",sender,kwargs)

pre_save.connect(pre_save_func)             # models对象保存前触发callback函数
post_save.connect(post_save_func)           # models对象保存后触发函数