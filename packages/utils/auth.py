from keystoneauth1.identity import v3 
from keystoneauth1 import session
from keystoneclient.v3 import client as keystone
from novaclient import client as nova
from cinderclient import client as cinder
from neutronclient.v2_0 import client as neutron
from glanceclient.v2 import client as glance

from packages.utils import base as auth_base

region = 'RegionOne'

class authentication(auth_base.options):

	def __init__(self):
		super(authentication, self).__init__()
		self._keystone_ = self._keystone_client()
		self._glance_ = self._glance_client()
		self._nova_ = self._nova_client()
		self._neutron_ = self._neutron_client()
		self._cinder_ = self._cinder_client()

	def get_session():
		auth = v3.Password(**self._ops)
		sess = session.Session(auth=auth)
		return sess

 	def _keystone_client(self):
		sess = self.get_session()
		return keystone.Client(session=sess, region_name = region)

	def _glance_client(self):
		sess = self.get_session()
		return glance.Client('2', session=sess, region_name = region)

	def _nova_client(self):
		sess = self.get_session()
		return nova.Client('2', session=sess, region_name = region)

	def _neutron_client(self):
		sess = self.get_session()
		return neutron.Client(session=sess, region_name = region)

	def _cinder_client(self):
		sess = self.get_session()
		return cinder.Client('3', session=sess, region_name = region)