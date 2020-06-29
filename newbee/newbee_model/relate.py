from django.db import models
NewBeeForeignKeyType = 101
NewBeeOneToOneFieldType = 102
NewBeeManyToManyFieldType = 103


class NewBeeRelatedBase:
    """
    自定义
    """

    def __init__(self, new_bee_request_key=None, new_bee_response_key=None, new_bee_can_add=False,
                 new_bee_add_key=None, new_bee_can_update=False, new_bee_update_key=None, new_bee_can_find=False,
                 new_bee_can_find_by_self=False, new_bee_find_by_self_key=None,
                 *args, **kwargs):
        """
        :param new_bee_request_key: request key是什么
        :param new_bee_response_key: response key是什么
        :param new_bee_can_add: 新增的时候能传递该字段吗
        :param new_bee_add_key: 新增的时候create的key是什么
        :param new_bee_can_update: 允许修改此字段吗
        :param new_bee_update_key: 修改的时候update的key是什么
        :param new_bee_can_find: 允许查询此字段(带着关联的模型数据)吗
        :param args:
        :param kwargs:
        """
        self.new_bee_request_key = new_bee_request_key
        self.new_bee_response_key = new_bee_response_key
        self.new_bee_can_add = new_bee_can_add
        self.new_bee_add_key = new_bee_add_key
        self.new_bee_can_update = new_bee_can_update
        self.new_bee_update_key = new_bee_update_key
        self.new_bee_can_find = new_bee_can_find
        self.new_bee_can_find_by_self = new_bee_can_find_by_self
        self.new_bee_find_by_self_key = new_bee_find_by_self_key
        super().__init__(*args, **kwargs)

    def get_attr(self, key):
        if key in ("new_bee_request_key", "request_key"):
            return self.new_bee_request_key
        elif key in ("new_bee_response_key", "response_key"):
            return self.new_bee_response_key
        elif key in ("new_bee_can_add", "can_add"):
            return self.new_bee_can_add
        elif key in ("new_bee_add_key", "add_key"):
            return self.new_bee_add_key
        elif key in ("new_bee_can_update", "can_update"):
            return self.new_bee_can_update
        elif key in ("new_bee_update_key", "update_key"):
            return self.new_bee_update_key
        elif key in ("new_bee_can_find", "can_find"):
            return self.new_bee_can_find
        elif key in ("new_bee_can_find_by_self", "can_find_by_self"):
            return self.new_bee_can_find_by_self
        elif key in ("new_bee_find_by_self_key", "find_by_self_key"):
            return self.new_bee_find_by_self_key

    def get_request_key(self):
        return self.new_bee_request_key

    def get_response_key(self):
        return self.new_bee_response_key

    def get_can_add(self):
        return self.new_bee_can_add

    def get_create_key(self):
        return self.new_bee_add_key

    def get_can_update(self):
        return self.new_bee_can_update

    def get_update_key(self):
        return self.new_bee_update_key

    def get_can_find(self):
        return self.new_bee_can_find

    def get_can_find_by_self(self):
        return self.new_bee_can_find_by_self

    def get_find_by_self_key(self):
        return self.new_bee_find_by_self_key



class NewBeeForeignKey(NewBeeRelatedBase, models.ForeignKey):
    def get_field_type(self):
        return NewBeeForeignKey


class NewBeeOneToOneField(NewBeeRelatedBase, models.OneToOneField):
    def get_field_type(self):
        return NewBeeOneToOneField


class NewBeeManyToManyField(NewBeeRelatedBase, models.ManyToManyField):
    def get_field_type(self):
        return NewBeeManyToManyFieldType