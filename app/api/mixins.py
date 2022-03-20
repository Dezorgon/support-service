from django.core.exceptions import ImproperlyConfigured


class GetSerializerMixin:
    serializer_classes = None

    def get_serializer_class(self):
        if self.serializer_classes is None:
            raise ImproperlyConfigured('Field serializer_classes must be declared')

        serializers = self.serializer_classes.get(self.action, None)

        if serializers is None:
            if 'default' not in self.serializer_classes:
                raise KeyError('Key default must be in serializer_class')
            serializers = self.serializer_classes['default']

        if isinstance(serializers, dict):
            if self.request.user.is_staff:
                return serializers['staff']
            else:
                return serializers['user']

        return serializers
