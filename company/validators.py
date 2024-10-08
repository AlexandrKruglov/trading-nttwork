import re
from rest_framework.serializers import ValidationError


class NameCompanyValidator:
    """валидатор для названия компании"""
    def __init__(self, field):
        self.field = field

    def __call__(self,value):
        reg = re.compile('^[a-zA-Zа-яА-я0-9\.\-\ ]+$')
        temp_value = dict(value).get(self.field)
        if not bool(reg.match(temp_value)):
            raise ValidationError(f'{self.field}  в имени допескются тольк: буквы, цифры, точка, тире ')
        return value
