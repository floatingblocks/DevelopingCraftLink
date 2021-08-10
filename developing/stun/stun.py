import argparse
import logging
import sys

import stunfunc

def get_nat_type(source_ip_,source_port_,stun_host_,stun_port_):
    try:
        nat_type, external_ip, external_port = stunfunc.get_ip_info(
            source_ip=source_ip_,
            source_port=source_port_,
            stun_host=stun_host_,
            stun_port=stun_port_
        )
        return nat_type,external_ip,external_port
    except KeyboardInterrupt:
        sys.exit()
