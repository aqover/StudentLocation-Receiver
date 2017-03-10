import struct

class AdPayLoad(object):
	"""docstring for AdPayLoad"""
	def __init__(self, data):
	    super(AdPayLoad, self).__init__()
	    self.ad_lenght  = data[0]
	    self.ad_type    = data[1]
	    self.data       = data[2]

	def __str__(self):
	    return "{lenght}, {type}, {data}".format(\
	    	lenght=self.ad_lenght, \
	    	type='%02X' % ord(self.ad_type), \
	    	data=' '.join(['%02X' % ord(b) for b in self.data]))

class AdInfoHeader(object):
    """docstring for AdInfoHeader"""
    def __init__(self, data):
        super(AdInfoHeader, self).__init__()
        self.event_type     = data[0]
        self.bdaddr_type    = data[1]
        self.bdaddr         = ':'.join(reversed(['%02X' % ord(b) for b in data[2:8]]))
        self.lenght         = struct.unpack('<B', data[8])[0]

    def __str__(self):
        return "{even}, {bd_ty}, {bd}, {len}".format(\
        	even 	= '%02X' % ord(self.event_type), \
        	bd_ty 	= '%02X' % ord(self.bdaddr_type), \
        	bd 		= self.bdaddr,\
        	len 	= self.lenght)

class MetaEvent(object):
    #HCI Events

    """docstring for MetaEvent"""
    def __init__(self, data):
        super(MetaEvent, self).__init__()
        self.subevent       = struct.unpack('<B', data[0])[0]
        self.report_num     = struct.unpack('<B', data[1])[0]             #AdInfoHeader

    def __str__(self):
        return "{sub}, {report}".format(sub=hex(self.subevent), report=self.report_num)

class BlueZHeader(object):
    #Host Controller and Baseband Commands (OGF=0x03)

    """docstring for BlueZHeader"""
    def __init__(self, data):
        super(BlueZHeader, self).__init__()
        self.hci_packet_type    = struct.unpack('<B', data[0])[0]
        self.event              = struct.unpack('<B', data[1])[0]
        self.lenght             = struct.unpack('<B', data[2])[0]

    def __str__(self):
        return "{hci}, {event}, {lenght}".format(hci=self.hci_packet_type, \
        	event=hex(self.event), lenght=self.lenght)