import time
from packages.utils import auth
from packages.common import log as loggging

LOG = log.getLogger(__name__)

class Openstack(auth.authentication):

    def __init__(self):
        super(Openstack, self).__init__()

    def _get_all_servers(self, page: int = 1, limit: int = 5):
        try:
            servers = self.__nova__.servers.list(
                        search_opts={
                            'all_tenants': 1, 
                            'availability_zone': 'nova'
                            }, 
                        limit=limit + 1
                    )
            offset = (page - 1) * limit
            server_infos = []
            while offset < len(servers) and len(server_infos) < limit:
                server_info = self._get_server_by_id(servers[offset]._info['id'])
                server_infos.append(server_info)
                offset += 1
            return server_infos
        except Exception as e:
            LOG.error("Failed to get instances info: %s" % e)

        return None
    
    def _get_server_by_id(self, ins_id):
        try: 
            info = self._nova_.servers.get(ins_id)._info
            _id = info['id']
            _name = info['name']
            _status = info['status']
            _flavor = self._nova_.flavors.get(info['flavor']['id']).name
            server_network = ""
            _lan_ip = ""
            _wan_ip = ""

            for key in info["addresses"].keys():
                server_network = key +": " + info["addresses"][key][0]["addr"] +" , "+ server_network
                if 'internal' in key:
                    _lan_ip = info["addresses"][key][0]["addr"]
                elif 'public' in key:
                    _wan_ip = info["addresses"][key][0]["addr"]
                sevrer = {
                    'id': _id,
                    'name': _name,
                    'status': _status,
                    'flavor': _flavor,
                    'lan': _lan_ip,
                    'wan': _wan_ip
                }
            return sevrer
        except Exception as e:
            LOG.error('Failed to get instance info: %s' %e)

        return None
    
    def _get_images(self):
        images = {}
        try:
            list_images = self._glance_.images.list(
                            search_opts={
                            'all_tenants': 1, 
                            'availability_zone': '_nova_'
                            }
                        )
            for image in list_images:
                images[image['id']] = str(image['name']) 
            return images
        except Exception as e:
            LOG.error('Cannot get images!! Error occurred: %s' %e)=
        return None
        
    def _get_flavors(self):
        try: 
            flavors = {}
            list_flavors = self._nova_.flavors.list()
            for flavor in list_flavors:
                flavors[flavor.id] = str(flavor.name)
            return flavors
        except Exception as e:
            LOG.error('Cannot get flavors!! Error occurred: %s' %e)

        return None
   
    def _get_networks(self):
        try:
            networks = {}
            subnets = self._neutron_.list_subnets()['subnets']
            for subnet in subnets:          
                networks[subnet['network_id']] = str(subnet['cidr']) 
            return networks
        except Exception as e:
            LOG.error('Cannot get networks!! Error occurred: %s' %e)

        return None

    def _create_volume(self, name, size, image):
        try:
            volume_name = name + '_rootdisk'
            volume = self._cinder_.volumes.create(name=name, size=size, imageRef=image)
            self._cinder_.volumes.set_bootable(volume.id, True)
            while True:
                info = self._cinder_.volumes.get(volume.id)
                if info.status == "available":
                    break
                elif info.status == "error":
                    raise Exception("Volume creation failed") 
            return volume.id
        except Exception as e:
            LOG.error('Openstack._create_volume.created volume failed: %s' %e)

    def _create_server(self, name, size, image, flavor, network):
        try:
            volume_id = self._create_volume(name, size, image)
            block_device = { 
                'vda': str(volume_id) 
            }
            server = self._nova_.servers.create(  name=name, 
                                                flavor=flavor, 
                                                image='', 
                                                block_device_mapping=block_device, 
                                                nics=[{'net-id': network}]
                                            )
            while True:
                info = self._nova_.servers.get(server.id)
                if info.status == 'ACTIVE':
                    break
                elif info.status == 'ERROR':
                    raise Exception("Server creation failed")
                time.sleep(5)
            server_info = self._get_server_by_id(server.id)
            return server_info
        except Exception as e:
            LOG.error('Openstack._create_server.created server failed: %s' %e)

    def _list_server_port(self, ins_id):
        server_port = {} 
        ports = self._neutron_.list_ports(device_id=ins_id)['ports'] 
        for port in ports: 
            server_port[port['id']] = str(port['fixed_ips'][0]['ip_address']) 
        return server_port

    def _create_port_for_server(self, ins_id, network_id):
        try:    
            port_info = { 
                'port': {
                    'network_id': network_id }
                }

            port_id = self._neutron_.create_port(port_info)['port']['id']
            self._nova_.servers.interface_attach(ins_id, port_id, net_id="", fixed_ip="")
            time.sleep(10)
            server = self._get_server_by_id(ins_id)
            return server
        except Exception as e:
            LOG.error('Openstack._create_port_for_server.cannot create port. Failed: %s' %e)

    def _detach_port_for_server(self, ins_id, port_id):
        try:
            self._nova_.servers.interface_detach(ins_id, port_id)
            time.sleep(10)
            server = self._get_server_by_id(ins_id)
            return server
        except Exception as e:
            LOG.error('Detach port for server failed: %s' %e)

    def _console_url(self, ins_id):
        _console = self._nova_.servers.get(ins_id).get_vnc_console(console_type='novnc')
        console_url = _console['console']['url']
        return console_url

    def _start_server(self, ins_id):
        self._nova_.servers.start(ins_id)
        while True:
            info = self._nova_.servers.get(ins_id)
            if info.status == 'ACTIVE':
                break
        return status

    def _stop_server(self, ins_id):
        self._nova_.servers.stop(ins_id)
        while True:
            info = self._nova_.servers.get(ins_id)
            if info.status == 'SHUTOFF':
                break
        status = {'status': info.status}
        return status
    
    # Func to delete server, use with caution
    def _delete_server(self, ins_id):
        info = self._nova_.servers.get(ins_id)._info
        volume_id = info['os-extended-volumes:volumes_attached'][0]['id']
        self._nova_.servers.delete(ins_id)
        while True:
            volume = self._cinder_.volumes.get(volume_id)._info
            if volume['status'] == 'available':
                self._cinder_.volumes.delete(volume_id, cascade=True)
                break