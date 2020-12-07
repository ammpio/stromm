import logging
import arrow
from copy import deepcopy

logger = logging.getLogger(__name__)

"""
This module is currently used by the datapusher
"""


def convert_to_api_payload(readout, readings_from_config):
    readout = deepcopy(readout)
    # fields is a dict will all the readings of all devices -- without the device id. This is done for backwards compatibility
    fields = {}
    # convert time from unix timestamp to date
    readout['time'] = arrow.get(readout['t']).strftime('%Y-%m-%dT%H:%M:%SZ')
    for rdg in readout['r']:
        # delete device names and vendor ids
        [rdg.pop(k, None) for k in ['_d', '_vid']]
        fields.update(rdg)
    # get the old reading names from the config for backwards compatibility
    for rdg in readings_from_config:
        for key in fields:
            if readings_from_config[rdg]['var'] == key:
                fields[rdg] = fields.pop(key)
                break
    readout['fields'] = fields
    # move snap_rev, config_id, reading_duration, and reading_offset under fields
    for key in ['snap_rev', 'config_id', 'reading_duration', 'reading_offset']:
        readout['fields'][key] = readout['m'][key]

    # removing sections from the devices-based dict
    for k in ['m', 'r', 't']:
        readout.pop(k)
    return readout
