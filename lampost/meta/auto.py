import copy


class AutoField():
    field = None

    def __init__(self, default=None):
        self.default = default
        if default is None or isinstance(default, (int, str, bool, tuple, float)):
            self._get_default = lambda instance: self.default
        else:
            self._get_default = self._complex_default

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        try:
            return instance.__dict__[self.field]
        except KeyError:
            return self._get_default(instance)

    def __set__(self, instance, value):
        if value == self.default:
            instance.__dict__.pop(self.field, None)
        else:
            instance.__dict__[self.field] = value

    def __delete__(self, instance):
        instance.__dict__.pop(self.field, None)

    def _complex_default(self, instance):
        new_value = copy.copy(self.default)
        instance.__dict__[self.field] = new_value
        return new_value

    def _meta_init(self, field):
        self.field = field


class TemplateField(AutoField):

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        try:
            return instance.__dict__[self.field]
        except KeyError:
            try:
                return getattr(instance.template, self.field)
            except AttributeError:
                return self._get_default(instance)
