import os

from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient.client import Client as nc
from cinderclient.v3.client import Client as cc


class OpenStackClient:
    def __init__(self):
        auth = v3.Password(
            auth_url=os.getenv('OS_AUTH_URL'),
            password=os.getenv('OS_PASSWORD'),
            username=os.getenv('OS_USERNAME'),
            project_id=os.getenv('OS_PROJECT_ID'),
            user_domain_name=os.getenv('OS_USER_DOMAIN_NAME')
        )
        sess = session.Session(auth=auth)
        self.nova = nc(version=2, session=sess, region_name=os.getenv('OS_REGION_NAME'))
        self.cinder = cc(session=sess, region_name=os.getenv('OS_REGION_NAME'))

    @property
    def servers(self):
        """Список серверов"""
        return self.nova.servers.list()

    @property
    def images(self):
        """Список образов"""
        return self.nova.glance.list()

    @property
    def flavors_with_local_disk(self):
        """Список конфигурации с локалным диском."""
        return list(filter(lambda d: d.disk > 0, self.nova.flavors.list()))

    @property
    def flavors_without_local_disk(self):
        """Список конфигураций без локалного диска."""
        return list(filter(lambda d: d.disk == 0, self.nova.flavors.list()))

    @property
    def volume_types(self):
        """Список типов сетевых дисков"""
        return list(self.cinder.volume_types.list())[1::]
