import argparse
import logging
import sys

import stunfunc
from stunfunc import Blocked,OpenInternet,FullCone,SymmetricUDPFirewall,\
    RestricNAT,RestricPortNAT,SymmetricNAT,ChangedAddress

info = {'nat_type':None,'external_ip':None,'external_port':None}

def get_nat_type(source_ip_=stunfunc.DEFAULTS['source_ip'],source_port_=stunfunc.DEFAULTS['source_port'],\
                stun_host_=stunfunc.STUN_SERVERS[0],stun_port_=stunfunc.DEFAULTS['stun_port']):
    if info['nat_type']==None :
        try:
            nat_type, external_ip, external_port = stunfunc.get_ip_info(
                source_ip=source_ip_,
                source_port=source_port_,
                stun_host=stun_host_,
                stun_port=stun_port_
            )
            info['nat_type']=nat_type
            info['external_ip']=external_ip
            info['external_port']=external_port
            return nat_type,external_ip,external_port
        except KeyboardInterrupt:
            pass
