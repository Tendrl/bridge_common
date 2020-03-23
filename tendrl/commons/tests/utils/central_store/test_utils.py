import builtins
import etcd
import maps
from mock import patch
import pytest
import time

from tendrl.commons.utils.central_store.utils import delete
from tendrl.commons.utils.central_store.utils import read
from tendrl.commons.utils.central_store.utils import reconnect
from tendrl.commons.utils.central_store.utils import to_tendrl_field
from tendrl.commons.utils.central_store.utils import wreconnect
from tendrl.commons.utils.central_store.utils import write


def client(**args):
    raise etcd.EtcdException


def sleep(*args):
    NS._int.wclient = "Temp_obj"
    NS._int.client = "Temp_obj"


def test_to_tendrl_field():
    ret = to_tendrl_field("test_name", {"message": "test"})
    assert ret is not None
    ret = to_tendrl_field("test_name", {"message": "test"}, 'json')


@patch.object(etcd, "Client")
def test_wreconnect(patch_client):
    setattr(builtins, "NS", maps.NamedDict())
    setattr(NS, "_int", maps.NamedDict())
    patch_client.return_value = etcd.Client()
    NS._int.etcd_kwargs = {
        'port': 1,
        'host': 2,
        'allow_reconnect': True}
    wreconnect()
    with patch.object(etcd, 'Client', client):
        with patch.object(time, 'sleep', sleep):
            with pytest.raises(etcd.EtcdException):
                wreconnect()


@patch.object(etcd, "Client")
def test_reconnect(patch_client):
    setattr(builtins, "NS", maps.NamedDict())
    setattr(NS, "_int", maps.NamedDict())
    patch_client.return_value = etcd.Client()
    NS._int.etcd_kwargs = {
        'port': 1,
        'host': 2,
        'allow_reconnect': True}
    reconnect()
    with patch.object(etcd, 'Client', client):
        with patch.object(time, 'sleep', sleep):
            with pytest.raises(etcd.EtcdException):
                reconnect()


@patch.object(etcd, "Client")
def test_read(patch_client):
    setattr(builtins, "NS", maps.NamedDict())
    setattr(NS, "_int", maps.NamedDict())
    NS._int.client = "Temp_obj"
    patch_client.return_value = etcd.Client()
    NS._int.etcd_kwargs = {
        'port': 1,
        'host': 2,
        'allow_reconnect': True}
    reconnect()
    read()
    NS._int.client.return_value = etcd.EtcdConnectionFailed
    with patch.object(etcd, 'Client', client):
        with patch.object(time, 'sleep', sleep):
            read()


@patch.object(etcd, "Client")
def test_write(patch_client):
    setattr(builtins, "NS", maps.NamedDict())
    setattr(NS, "_int", maps.NamedDict())
    NS._int.wclient = "Temp_obj"
    patch_client.return_value = etcd.Client()
    NS._int.etcd_kwargs = {
        'port': 1,
        'host': 2,
        'allow_reconnect': True}
    wreconnect()
    write()


@patch.object(etcd, "Client")
def test_delete(patch_client):
    setattr(builtins, "NS", maps.NamedDict())
    setattr(NS, "_int", maps.NamedDict())
    NS._int.wclient = "Temp_obj"
    patch_client.return_value = etcd.Client()
    NS._int.etcd_kwargs = {
        'port': 1,
        'host': 2,
        'allow_reconnect': True}
    wreconnect()
    delete()


"""
@patch.object(etcd, "Client")
def test_watch(patch_client):
    setattr(builtins, "NS", maps.NamedDict())
    setattr(NS, "_int", maps.NamedDict())
    NS._int.client = "Temp_obj"
    NS._int.client.eternal_watch = {}
    patch_client.return_value = etcd.Client()
    NS._int.etcd_kwargs = {
        'port': 1,
        'host': 2,
        'allow_reconnect': True}
    obj = importlib.import_module(
        "tendrl.commons.objects.cluster_node_context")
    watch(obj, "test_key")
"""
