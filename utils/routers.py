from rest_framework.routers import DynamicRoute, Route
from rest_framework.routers import SimpleRouter as BaseRouter


class SimpleRouter(BaseRouter):
    """
    Custom Router that allows methods to its methodnamehyphen variant.
    For example:
        Method do_some_stuff will be translated to url resource/do-some-stuff
    """
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            detail=False,
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes using @action
        DynamicRoute(
            url=r'^{prefix}/{methodnamehyphen}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={},
            detail=False
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            detail=True,
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes using @action
        DynamicRoute(
            url=r'^{prefix}/{methodnamehyphen}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={},
            detail=True
        ),
    ]


class DefaultRouter(SimpleRouter):
    """
    Default router that provides shortcuts to register single object viewsets.
    """
    _single_object_registry = []
    _nested_object_registry = []

    def register(self, prefix, viewset, basename=None, router_class=None):
        """
        Append the given viewset to the proper registry.
        """
        if basename is None:
            basename = self.get_default_basename(viewset)

        if router_class is not None:
            kwargs = {'trailing_slash': bool(self.trailing_slash)}
            single_object_router_classes = (
                AuthenticationRouter, SingleObjectRouter)

            if issubclass(router_class, single_object_router_classes):
                router = router_class(**kwargs)
                router.register(prefix, viewset, basename=basename)
                self._single_object_registry.append(router)

        else:
            self.registry.append((prefix, viewset, basename))

    def get_urls(self):
        """
        Generate the list of URL patterns including the registered single
        object routers urls.
        """
        base_urls = super(SimpleRouter, self).get_urls()
        single_urls = sum([r.urls for r in self._single_object_registry], [])
        nested_urls = sum([r.urls for r in self._nested_object_registry], [])

        return base_urls + single_urls + nested_urls


class AuthenticationRouter(BaseRouter):
    """
    Custom router that shall be used to map authentication methods.
    """
    routes = [
        # Detail route
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'post': 'authenticate',
            },
            detail=False,
            name='{basename}-authenticate',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes using @action
        DynamicRoute(
            url=r'^{prefix}/{methodnamehyphen}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={},
            detail=True
        ),
    ]


class SingleObjectRouter(BaseRouter):
    """
    Custom router for compose urls for single object viewsets.
    """
    routes = [
        # Detail route
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            detail=False,
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes using @action
        DynamicRoute(
            url=r'^{prefix}/{methodnamehyphen}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={},
            detail=True
        ),
    ]
