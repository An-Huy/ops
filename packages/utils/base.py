from packages.common import conf as cfg  

CONF = cfg.CONF 

class options(object):
	ops = {
		'project_domain_name': CONF['openstack']['project_domain_name'],
		'user_domain_name': CONF['openstack']['user_domain_name'],
		'project_name': CONF['openstack']['project_name'],
		'username': CONF['openstack']['username'],
		'password': CONF['openstack']['password'],
		'auth_url': CONF['openstack']['auth_url']
		}
	self._ops = ops