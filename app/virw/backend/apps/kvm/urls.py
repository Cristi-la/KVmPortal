# urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    TagViewSet,
    HostDeviceViewSet,
    StorageVolumeViewSet,
    NetworkInterfaceViewSet,
    NetworkFilterViewSet,
    SnapshotViewSet,
    DomainCheckpointViewSet,
    HypervisorViewSet,
    NodeDeviceViewSet,
    StoragePoolViewSet,
    DomainViewSet,
)

router = DefaultRouter()
router.register(r'tags', TagViewSet, 'tags')
router.register(r'hostdevices', HostDeviceViewSet, 'hostdevices')
router.register(r'storagevolumes', StorageVolumeViewSet, 'storagevolumes')
router.register(r'networkinterfaces', NetworkInterfaceViewSet, 'networkinterfaces')
router.register(r'networkfilters', NetworkFilterViewSet, 'networkfilters')
router.register(r'snapshots', SnapshotViewSet, 'snapshots')
router.register(r'domaincheckpoints', DomainCheckpointViewSet, 'domaincheckpoints')
router.register(r'hypervisors', HypervisorViewSet, 'hypervisors')
router.register(r'nodedevices', NodeDeviceViewSet, 'nodedevices')
router.register(r'storagepools', StoragePoolViewSet, 'storagepools')
router.register(r'domains', DomainViewSet, 'domains')

urlpatterns = [] + router.urls