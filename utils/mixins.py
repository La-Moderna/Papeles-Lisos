"""Generic mixins."""
from inspect import getmembers

from rest_framework.generics import GenericAPIView


def _is_extra_action(attr):
    return hasattr(attr, 'mapping')


class BaseGenericViewSet(GenericAPIView):

    """The GenericViewSet class does not provide any actions by default.
    But does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """

    def get_serializer_class(self, action=None):
        """Return the serializer class depending on request method."""

        if action is not None:
            class_name = f'{action}_serializer_class'
            return getattr(self, class_name)
        else:
            return super(BaseGenericViewSet, self).get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        """Return the serializer that should be used to the given action.
        If any action was given, returns the serializer_class.
        """
        action = kwargs.pop('action', None)

        serializer_class = self.get_serializer_class(action)

        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @classmethod
    def get_extra_actions(cls):
        """Get the methods that are marked as an extra ViewSet `@action`."""
        return [method for _, method in getmembers(cls, _is_extra_action)]
