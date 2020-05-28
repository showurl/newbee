from django.db import models


class NewBeeBaseModel(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    update_time = models.DateTimeField(auto_now=True)
    # 是否删除
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        super(NewBeeBaseModel, self).delete(using=using, keep_parents=keep_parents)

    @staticmethod
    def get_field_attr(model, field_name, para):
        field = model._meta.get_field(field_name)
        return field.get_attr(para)

    @staticmethod
    def get_field_type(model, field_name):
        field = model._meta.get_field(field_name)
        return field.get_field_type()

    @staticmethod
    def get_related_name(model, field_name):
        field = model._meta.get_field(field_name)
        return field.related_name


def get_attr_by_model_field_key(model, field_name, para):
    """
    获取一个model中一个字段的一个属性  和  字段的类型
    :param model:
    :param field_name:
    :param para:
    :return:
    """
    try:
        return model.get_field_attr(model, field_name, para)
    except:
        if para in ("request_key", "new_bee_request_key"):
            return model.get_related_name(model, field_name)


def get_type_by_model_field_key(model, field_name):
    """
    获取一个model中一个字段的一个属性  和  字段的类型
    :param model:
    :param field_name:
    :param para:
    :return:
    """
    return model.get_field_type(model, field_name)
