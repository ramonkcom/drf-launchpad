from django.utils.translation import gettext_lazy as _

from ...helpers import model_to_dict


class DictFactoryMixin:

    @classmethod
    def _filter_fields(cls, instance_dict, include_fields=None, exclude_fields=None):
        exclude_fields = exclude_fields or []
        include_fields = include_fields or [k for k in instance_dict.keys()
                                            if k not in exclude_fields]

        def check_field(field):
            if field in include_fields and field in exclude_fields:
                error_msg = _('Field `%(field_name)s` cannot be included and '
                              'excluded at the same time.') % {'field_name': field, }
                raise ValueError(error_msg)

            return field in include_fields and field not in exclude_fields

        return {k: v for k, v in instance_dict.items() if check_field(k)}

    @classmethod
    def _build_dict(cls, _model_instance, **kwargs):

        instance_dict = model_to_dict(_model_instance)
        instance_dict.update(kwargs)

        return instance_dict

    @classmethod
    def build_dict(cls, **kwargs):
        include_fields = kwargs.pop('include_fields', [])
        exclude_fields = kwargs.pop('exclude_fields', [])

        if 'id' not in include_fields:
            exclude_fields.extend(['id',])

        instance = cls.build()
        instance_dict = cls._build_dict(instance, **kwargs)
        instance_dict = cls._filter_fields(instance_dict,
                                           include_fields,
                                           exclude_fields)

        return instance_dict
