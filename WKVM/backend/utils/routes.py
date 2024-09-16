from dataclasses import dataclass
from rest_framework import viewsets
from typing import List
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from channels.generic.websocket import AsyncWebsocketConsumer

@dataclass
class Route:
    regex: str
    viewset: viewsets.ViewSet
    basename: str


class RouteMap:
    ROUTE_TYPE = Route

    def __init__(self, *Routes: ROUTE_TYPE):
        self.routes: List[self.ROUTE_TYPE] = Routes

    def add_route(self, route: ROUTE_TYPE):
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