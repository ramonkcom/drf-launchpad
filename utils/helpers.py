from itertools import chain


def debug_model_instance(instance):
    """Prints a model instance in a more readable format.

    Args:
        instance (Model): A model instance.
    """

    fields = chain(instance._meta.concrete_fields,
                   instance._meta.private_fields)
    m2m_fields = instance._meta.many_to_many

    print('='*80)
    print(instance)
    print('-'*80)

    for field in fields:
        print(f'{field.name}: {field.value_from_object(instance)}')

    for field in m2m_fields:
        print(f'{field.name}: {field.value_from_object(instance)}')

    print('='*80)


def load_entity(path):
    """Loads a module entity from a string path.

    Args:
        path (str): A string path to the entity (e.g. 'utils.load_function').

    Returns:
        any: The entity at the given path.
    """

    import importlib

    module_path, entity_name = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, entity_name)


def model_to_dict(instance):
    """Returns a dict representation of a model instance.

    This function is an alternative to the Django built-in
    (django.forms.models.model_to_dict) function. As opposed to Django's
    function, this also includes uneditable fields and many-to-many fields
    as a list of ID's.

    Args:
        instance (Model): A model instance.

    Returns:
        dict: A dict representation of the model instance.
    """

    fields = chain(instance._meta.concrete_fields,
                   instance._meta.private_fields)
    m2m_fields = instance._meta.many_to_many

    data = {}
    for field in fields:
        data[field.name] = field.value_from_object(instance)

    for field in m2m_fields:
        data[field.name] = [i.id for i in field.value_from_object(instance)]

    return data
