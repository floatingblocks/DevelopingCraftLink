import argparse
import logging
import sys

import stunfunc
from stunfunc import Blocked,OpenInternet,FullCone,SymmetricUDPFirewall,\
    RestricNAT,RestricPortNAT,SymmetricNAT,ChangedAddress

info = {'nat_type':None,'external_ip':None,'external_port':None}

def get_nat_type(source_ip_=stunfunc.DEFAULTS['source_ip'],source_port_=stunfunc.DEFAULTS['source_port'],\
                stun_host_=stunfunc.STUN_SERVERS[0],stun_port_=stunfunc.DEFAULTS['stun_port']):
    info['external_ip']="127.0.0.1";info['external_port']=20000
