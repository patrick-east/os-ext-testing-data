#!/usr/bin/env python

import argparse
import re
import purestorage

collection = []


def get_volume_ids_from_logs(log_path):
    # parse screen-c-vol.log to extract volume ids that were created in last test run
    with open("%s/screen-c-vol.log" % log_path) as f:
        for line in f:
            result = re.search("cinder\.volume\.flows\.manager\.create_volume .* 'volume_name': u'volume-(.+?)'", line)
            if result:
                vol_name = result.group(1)
                global collection
                collection.append(vol_name)
                print "Found vol in logs: %s" % vol_name


def is_cinder_vol(volume_name):
    # check for each id in collection to see if volume_name contains that id
    global collection
    for idstring in collection:
        if idstring in volume_name:
            return True
    return False


def disconnect_old_volumes(flash_array):
    print 'Disconnecting any remaining volumes used in this test from hosts on array...'
    hosts = flash_array.list_hosts()
    for host in hosts:
        host_name = host['name']
        try:
            connected_volumes = flash_array.list_host_connections(host_name)
        except purestorage.PureHTTPError as e:
            if e.code == 400 and "not exist" in e.text:
                continue  # We don't care if the host doesn't exist, just keep going
            else:
                print 'failed to list attached volumes for host %s' % host_name

        for connected_volume in connected_volumes:
            print connected_volume
            volume_name = connected_volume['vol']
            if is_cinder_vol(volume_name):
                try:
                    flash_array.disconnect_host(host_name, volume_name)
                except Exception as e:
                    print 'failed to disconnect volume %s from host %s error: %s' \
                          % (volume_name, host_name, e)
            else:
                print 'not disconnecting volume %s' % volume_name


def delete_volumes(flash_array, volumes, should_eradicate=False):
    for volume in volumes:
        volume_name = volume['name']
        if is_cinder_vol(volume_name):
            try:
                if should_eradicate:
                    flash_array.eradicate_volume(volume_name)
                else:
                    flash_array.destroy_volume(volume_name)
            except Exception as e:
                print 'failed to delete volume %s error: %s' % \
                      (volume_name, e)
        else:
            print 'not deleting volume %s' % volume_name


def delete_old_volumes(flash_array):
    print 'Deleting any remaining volumes used in this test from array...'
    volumes = flash_array.list_volumes()
    delete_volumes(flash_array, volumes)


def eradicate_all_volumes(flash_array):
    print 'Eradicating all volumes used in this test from array...'
    volumes = flash_array.list_volumes(pending_only=True)
    delete_volumes(flash_array, volumes, True)


def clean_purity(address, token):
    print 'address %s' % address
    print 'token %s' % token
    fa = purestorage.FlashArray(address, api_token=token)
    print 'Connected to host %s' % address
    disconnect_old_volumes(fa)
    delete_old_volumes(fa)
    eradicate_all_volumes(fa)
    print 'Done!'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean all volumes from a purity host.')
    parser.add_argument('-a', '--address', dest='address', required=True,
                        help='Purity hostname or ip address')
    parser.add_argument('-t', '--token', dest='token', required=True,
                        help='REST API token to be used for requests')
    parser.add_argument('-p', '--path', dest='log_path', required=True,
                        help='log directory')
    args = parser.parse_args()

    get_volume_ids_from_logs(args.log_path)
    
    clean_purity(args.address, args.token)

