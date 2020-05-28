from django.db import models

NewBeeBooleanFieldType = 1
NewBeeCharFieldType = 2
NewBeeCommaSeparatedIntegerFieldType = 3
NewBeeDateFieldType = 4
NewBeeDateTimeFieldType = 5
NewBeeDecimalFieldType = 6
NewBeeDurationFieldType = 7
NewBeeEmailFieldType = 8
NewBeeFilePathFieldType = 9
NewBeeFloatFieldType = 10
NewBeeIntegerFieldType = 11
NewBeeBigIntegerFieldType = 12
NewBeeIPAddressFieldType = 13
NewBeeGenericIPAddressFieldType = 14
NewBeeNullBooleanFieldType = 15
NewBeePositiveIntegerFieldType = 16
NewBeePositiveSmallIntegerFieldType = 17
NewBeeSlugFieldType = 18
NewBeeSmallIntegerFieldType = 19
NewBeeTextFieldType = 20
NewBeeTimeFieldType = 21
NewBeeURLFieldType = 22
NewBeeBinaryFieldType = 23
NewBeeUUIDFieldType = 24
NewBeeAutoFieldType = 25
NewBeeBigAutoFieldType = 26


class NewBeeFieldBase:
    """
    自定义
    """

    def __init__(self, new_bee_request_key=None, new_bee_response_key=None, new_bee_can_add=False,
                 new_bee_is_add_tran=False, new_bee_add_key=None, new_bee_can_update=False,
                 new_bee_is_update_tran=False, new_bee_update_key=None, new_bee_can_found=False,
                 new_bee_can_find_by_self=False, new_bee_find_by_self_key=None,
                 new_bee_is_found_as_foreign_return=False,
                 **kwargs):
        """
        NewBee django工具模型字段基类
        :param new_bee_request_key: 字段接受前端传递的key
        :param new_bee_response_key: 字段返回前端传递的key
        :param new_bee_can_add: 字段可否 添加记录时  被传递key
        :param new_bee_is_add_tran: 添加记录时 字段是否必须传递
        :param new_bee_add_key: 执行Django rom create操作时 create_dict中的key
        :param new_bee_can_update: 字段可否 修改记录时  被传递key
        :param new_bee_is_update_tran: 修改记录时  字段是否必须传递被修改
        :param new_bee_update_key: 执行Django rom update操作时 create_dict中的key
        :param new_bee_can_found: 执行查询的时候  该字段是否可以返回
        :param new_bee_can_find_by_self: 组成查询字典时  是否可以接收此字段的值
        :param new_bee_find_by_self_key: find_dict的key  有可能是模糊查询  有可能是大于小于
        :param new_bee_is_found_as_foreign_return: 当此model为其他model的外键模型时，此字段是否在查询操作中被返回
        :param kwargs:
        """
        self.new_bee_request_key = new_bee_request_key
        self.new_bee_response_key = new_bee_response_key
        self.new_bee_can_add = new_bee_can_add
        self.new_bee_is_add_tran = new_bee_is_add_tran
        self.new_bee_add_key = new_bee_add_key
        self.new_bee_can_update = new_bee_can_update
        self.new_bee_is_update_tran = new_bee_is_update_tran
        self.new_bee_update_key = new_bee_update_key
        self.new_bee_can_found = new_bee_can_found
        self.new_bee_can_find_by_self = new_bee_can_find_by_self
        self.new_bee_find_by_self_key = new_bee_find_by_self_key
        self.new_bee_is_found_as_foreign_return = new_bee_is_found_as_foreign_return
        super().__init__(**kwargs)

    def get_attr(self, key):
        if key in ("new_bee_request_key", "request_key"):
            return self.new_bee_request_key
        elif key in ("new_bee_response_key", "response_key"):
            return self.new_bee_response_key
        elif key in ("new_bee_can_add", "can_add"):
            return self.new_bee_can_add
        elif key in ("new_bee_is_add_tran", "is_add_tran"):
            return self.new_bee_is_add_tran
        elif key in ("new_bee_add_key", "add_key"):
            return self.new_bee_add_key
        elif key in ("new_bee_can_update", "can_update"):
            return self.new_bee_can_update
        elif key in ("new_bee_is_update_tran", "is_update_tran"):
            return self.new_bee_is_update_tran
        elif key in ("new_bee_update_key", "update_key"):
            return self.new_bee_update_key
        elif key in ("new_bee_can_found", "can_found"):
            return self.new_bee_can_found
        elif key in ("new_bee_can_find_by_self", "can_find_by_self"):
            return self.new_bee_can_find_by_self
        elif key in ("new_bee_find_by_self_key", "find_by_self_key"):
            return self.new_bee_find_by_self_key
        elif key in ("new_bee_is_found_as_foreign_return", "is_found_as_foreign_return"):
            return self.new_bee_is_found_as_foreign_return
        return

    def get_request_key(self):
        return self.new_bee_request_key

    def get_response_key(self):
        return self.new_bee_response_key

    def get_can_add(self):
        return self.new_bee_can_add

    def get_is_add_tran(self):
        return self.new_bee_is_add_tran

    def get_add_key(self):
        return self.new_bee_add_key

    def get_can_update(self):
        return self.new_bee_can_update

    def get_is_update_tran(self):
        return self.new_bee_is_update_tran

    def get_update_key(self):
        return self.new_bee_update_key

    def get_can_found(self):
        return self.new_bee_can_found

    def get_can_find_by_self(self):
        return self.new_bee_can_find_by_self

    def get_find_by_self_key(self):
        return self.new_bee_find_by_self_key

    def get_is_found_as_foreign_return(self):
        return self.new_bee_is_found_as_foreign_return


class NewBeeBooleanField(NewBeeFieldBase, models.BooleanField):
    def get_field_type(self):
        return NewBeeBooleanFieldType


class NewBeeCharField(NewBeeFieldBase, models.CharField):
    def get_field_type(self):
        return NewBeeCharFieldType


class NewBeeCommaSeparatedIntegerField(NewBeeFieldBase, models.CommaSeparatedIntegerField):
    def get_field_type(self):
        return NewBeeCommaSeparatedIntegerFieldType


class NewBeeDateField(NewBeeFieldBase, models.DateField):
    def get_field_type(self):
        return NewBeeDateFieldType


class NewBeeDateTimeField(NewBeeFieldBase, models.DateTimeField):
    def get_field_type(self):
        return NewBeeDateTimeFieldType


class NewBeeDecimalField(NewBeeFieldBase, models.DecimalField):
    def get_field_type(self):
        return NewBeeDecimalFieldType


class NewBeeDurationField(NewBeeFieldBase, models.DurationField):
    def get_field_type(self):
        return NewBeeDurationFieldType


class NewBeeEmailField(NewBeeFieldBase, models.EmailField):
    def get_field_type(self):
        return NewBeeEmailFieldType


class NewBeeFilePathField(NewBeeFieldBase, models.FilePathField):
    def get_field_type(self):
        return NewBeeFilePathFieldType


class NewBeeFloatField(NewBeeFieldBase, models.FloatField):
    def get_field_type(self):
        return NewBeeFloatFieldType


class NewBeeIntegerField(NewBeeFieldBase, models.IntegerField):
    def get_field_type(self):
        return NewBeeIntegerFieldType


class NewBeeBigIntegerField(NewBeeFieldBase, models.BigIntegerField):
    def get_field_type(self):
        return NewBeeBigIntegerFieldType


class NewBeeIPAddressField(NewBeeFieldBase, models.IPAddressField):
    def get_field_type(self):
        return NewBeeIPAddressFieldType


class NewBeeGenericIPAddressField(NewBeeFieldBase, models.GenericIPAddressField):
    def get_field_type(self):
        return NewBeeGenericIPAddressFieldType


class NewBeeNullBooleanField(NewBeeFieldBase, models.NullBooleanField):
    def get_field_type(self):
        return NewBeeNullBooleanFieldType


class NewBeePositiveIntegerField(NewBeeFieldBase, models.PositiveIntegerField):
    def get_field_type(self):
        return NewBeePositiveIntegerFieldType


class NewBeePositiveSmallIntegerField(NewBeeFieldBase, models.PositiveSmallIntegerField):
    def get_field_type(self):
        return NewBeePositiveSmallIntegerFieldType


class NewBeeSlugField(NewBeeFieldBase, models.SlugField):
    def get_field_type(self):
        return NewBeeSlugFieldType


class NewBeeSmallIntegerField(NewBeeFieldBase, models.SmallIntegerField):
    def get_field_type(self):
        return NewBeeSmallIntegerFieldType


class NewBeeTextField(NewBeeFieldBase, models.TextField):
    def get_field_type(self):
        return NewBeeTextFieldType


class NewBeeTimeField(NewBeeFieldBase, models.TimeField):
    def get_field_type(self):
        return NewBeeTimeFieldType


class NewBeeURLField(NewBeeFieldBase, models.URLField):
    def get_field_type(self):
        return NewBeeURLFieldType


class NewBeeBinaryField(NewBeeFieldBase, models.BinaryField):
    def get_field_type(self):
        return NewBeeBinaryFieldType


class NewBeeUUIDField(NewBeeFieldBase, models.UUIDField):
    def get_field_type(self):
        return NewBeeUUIDFieldType


class NewBeeAutoField(NewBeeFieldBase, models.AutoField):
    def get_field_type(self):
        return NewBeeAutoFieldType


class NewBeeBigAutoField(NewBeeFieldBase, models.BigAutoField):
    def get_field_type(self):
        return NewBeeBigAutoFieldType
