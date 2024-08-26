from apps.kvm.views import TagViewSet, HypervisorViewSet, VMViewSet
from utils.routes import Route, RouteMap

urlpatterns = []


routes = RouteMap(
    Route(r"tag", TagViewSet,  "tag"),
    Route(r"hypervisor", HypervisorViewSet,  "hypervisor"),
    Route(r"vm", VMViewSet,  "vm"),
)