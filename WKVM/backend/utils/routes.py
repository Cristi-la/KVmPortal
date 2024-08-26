from dataclasses import dataclass
from rest_framework import viewsets
from typing import List
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets

@dataclass
class Route:
    regex: str
    viewset: viewsets.ViewSet
    basename: str


class RouteMap:
    def __init__(self, *Routes: Route):
        self.routes: List[Route] = Routes

    def add_route(self, route: Route):
        self.routes.append(route)
    
    def __add__(self, other: 'RouteMap') -> 'RouteMap':
        if not isinstance(other, RouteMap):
            raise TypeError(f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")
        new_route_map = RouteMap()
        new_route_map.routes = self.routes + other.routes
        return new_route_map

    @property
    def export(self) -> DefaultRouter:
        router = DefaultRouter()
        for route in self.routes:
            router.register(
                prefix=route.regex,
                viewset=route.viewset,
                basename=route.basename
            )
        return router.urls
