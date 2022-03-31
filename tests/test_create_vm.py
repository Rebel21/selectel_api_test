from datetime import datetime

import pytest
from allpairspy import AllPairs

from api.openstack_client import OpenStackClient


class TestCreateVM:
    client = OpenStackClient()

    @pytest.mark.parametrize(['image', 'flavor'], [
        values for values in AllPairs([client.images, client.flavors_with_local_disk])
    ])
    def test_create_vm_with_local_disk(self, image, flavor):
        """Тест создания виртуальной машины с локальным диском"""

        # Создаём виртуальную машину
        vm_name = f'Test_vm_{int(datetime.now().timestamp())}'
        instance = self.client.nova.servers.create(name=vm_name, image=image, flavor=flavor)
        # Проверяем, что виртуальная машина создалась с праметрами, указанными при создании. Прверяем, что виртуалка
        # собирается
        assert instance.name == vm_name
        assert instance.image['id'] == image.id
        assert instance.flavor['id'] == flavor.id
        assert instance.status == 'BUILD'

    @pytest.mark.parametrize(['image', 'flavor', 'volume_type'], [
        values for values in AllPairs([client.images, client.flavors_without_local_disk, client.volume_types])
    ])
    def test_create_vm_with_network_disk(self, image, flavor, volume_type):
        """Тест создания виртуальной машины с сетевым диском"""

        # Создаём сетевой диск
        volume = self.client.cinder.volumes.create(size=10, volume_type=volume_type.id, name=f'disk_{int(datetime.now().timestamp())}')
        # Создаём виртуальную машину
        vm_name = f'Test_vm_{int(datetime.now().timestamp())}'
        block_dev_mapping = {'vda': volume.id}
        instance = self.client.nova.servers.create(name=vm_name, image=image, flavor=flavor, block_device_mapping=block_dev_mapping)
        # Проверяем, что виртуальная машина создалась с праметрами, указанными при создании. Прверяем, что виртуалка
        # собирается
        assert instance.name == vm_name
        assert instance.image['id'] == image.id
        assert instance.flavor['id'] == flavor.id
        assert instance.status == 'BUILD'
