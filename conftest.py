import pytest

from api.openstack_client import OpenStackClient


@pytest.fixture(scope='session', autouse=True)
def delete_servers():
    """Фикстура удаляет все сервера (виртуальные машины), созданные в рамках сессии"""
    yield
    client = OpenStackClient()
    for server in client.servers:
        if 'Test_vm' in server.name:
            client.nova.servers.delete(server)

