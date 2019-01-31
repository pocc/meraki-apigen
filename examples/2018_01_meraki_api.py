# -*- coding: utf-8 -*-
"""Generated and linted at 2019-01-30T23:18:10.640588
Pulled via the Meraki API v0 (https://dashboard.meraki.com/api_docs/)
API calls: 203 {GET: 118, POST: 26, PUT: 42, DELETE: 17}

Meraki API Generator v0.0.0
    Convert all Meraki API calls into [python] function calls.
    As new API calls are released all the time, rerun this occasionally.

More Info
    Author: Ross Jacobs (rosjacob [AT] cisco.com)
    Github: https://github.com/pocc/meraki-apigen
    Issues: https://github.com/pocc/meraki-apigen/issues
"""
import json
import urllib.parse

import requests

BASE_URL = 'https://api.meraki.com/api/v0'
HEADERS = {
    'X-Cisco-Meraki-API-Key': '<YOUR API KEY HERE>',
    'Content-Type': 'application/json'
}


def graceful_exit(response):
    """Gracefully exit from the function.
    
    JSON:
        200: Successful GET, UPDATE
        201: Successful POST
    
    {}:
        204: Successful DELETE
        400: Bad request. Correct/check your params
        404: Resource not found. Correct/check your params
        500: Server error
    
    Args:
        response (Requests): The requests object from the function call.
    Returns:
        JSON if one is available. Return status code (int) if not.
    """
    try:
        resp_json = json.loads(response.text)
        if 'errors' in resp_json:
            raise ConnectionError(resp_json['errors'])
        if type(resp_json) == json:
            resp_json['status_code'] = response.status_code
        return resp_json
    except ValueError:
        return response.status_code


def get_admins_by_org_id(org_id):
    """List the dashboard administrators in this organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/admins'.format(org_id), headers=HEADERS)
    return graceful_exit(response)


def create_admin_by_org_id(org_id, params=''):
    """Create a new dashboard administrator

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - email: The email of the dashboard administrator. This
           attribute can not be updated.
        - name: The name of the dashboard administrator
        - orgAccess: The privilege of the dashboard administrator on
           the organization (full, read-only, none)
        - tags: The list of tags that the dashboard administrator has
           privileges on
        - networks: The list of networks that the dashboard
           administrator has privileges on

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/organizations/{}/admins'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_admin_by_admin_id(org_id, admin_id, params=''):
    """Update an administrator

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @admin_id: (eg 545173)
            ↳  get_admins_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - email: The email of the dashboard administrator. This
           attribute can not be updated.
        - name: The name of the dashboard administrator
        - orgAccess: The privilege of the dashboard administrator on
           the organization (full, read-only, none)
        - tags: The list of tags that the dashboard administrator has
           privileges on
        - networks: The list of networks that the dashboard
           administrator has privileges on

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/organizations/{}/admins/{}'.format(org_id, admin_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_admin_by_admin_id(org_id, admin_id):
    """Revoke all access for a dashboard administrator within this organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @admin_id: (eg 545173)
            ↳  get_admins_by_org_id(org_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/organizations/{}/admins/{}'.format(org_id, admin_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_alert_settings_by_network_id(network_id):
    """Return the alert configuration for this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/alertSettings'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_alert_settings_by_network_id(network_id, params=''):
    """Update the alert configuration for this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - defaultDestinations: The network_wide destinations for all
           alerts on the network.
        - alerts: Alert-specific configuration for each type. Only
           alerts that pertain to the network can be updated.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/alertSettings'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_camera_analytics_zones_by_device_serial(serial):
    """Returns all configured analytic zones for this camera

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/devices/{}/camera/analytics/zones'.format(serial),
        headers=HEADERS)
    return graceful_exit(response)


def get_camera_analytics_recent_by_device_serial(serial):
    """Returns most recent record for analytics zones

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/devices/{}/camera/analytics/recent'.format(serial),
        headers=HEADERS)
    return graceful_exit(response)


def get_camera_analytics_live_by_device_serial(serial):
    """Returns live state from camera of analytics zones

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/devices/{}/camera/analytics/live'.format(serial),
        headers=HEADERS)
    return graceful_exit(response)


def get_camera_analytics_overview_by_device_serial(serial):
    """Returns an overview of aggregate analytics data for a timespan

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/devices/{}/camera/analytics/overview'.format(serial),
        headers=HEADERS)
    return graceful_exit(response)


def get_history_by_zone_id(serial, zone_id):
    """Return historical records for analytic zones

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @zone_id: Camera Analytics Zone ID
            ↳ get_analytics_zones_by_serial(serial)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/devices/{}/camera/analytics/zones/{}/history'.format(
            serial, zone_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_bluetooth_clients_by_network_id(network_id, params=''):
    """List the Bluetooth clients seen by APs in this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timespan: The timespan, in seconds, used to look back from
           now for bluetooth clients
        - includeConnectivityHistory: Include the connectivity history
           for this client
        - perPage: The number of entries per page returned
        - startingAfter: A token used by the server to indicate the
           start of the page. Often this is a timestamp or an ID but it
           is not limited to those. This parameter should not be defined
           by client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.
        - endingBefore: A token used by the server to indicate the end
           of the page. Often this is a timestamp or an ID but it is not
           limited to those. This parameter should not be defined by
           client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/bluetoothClients{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_bluetooth_clients_by_bluetooth_client_id(network_id,
                                                 bluetooth_client_id,
                                                 params=''):
    """Return a Bluetooth client

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @bluetooth_client_id: Bluetooth MAC (eg 00:11:22:33:44:55)
            ↳ get_bluetooth_clients_by_network_id(network_id, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - includeConnectivityHistory: Include the connectivity history
           for this client
        - connectivityHistoryTimespan: The timespan, in seconds, for
           the connectivityHistory data. By default 1 day, 86400, will
           be used.

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/bluetoothClients/{}{}'.format(
            network_id, bluetooth_client_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_video_link_by_camera_serial(network_id, serial, params=''):
    """Returns video link for the specified camera. If a timestamp supplied, it
       links to that time.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timestamp: The video link will start at this timestamp. The
           timestamp is in UNIX Epoch time (milliseconds).

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/cameras/{}/videoLink{}'.format(
            network_id, serial, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_clients_by_device_serial(serial, params=''):
    """List the clients of a device, up to a maximum of a month ago. The usage
       of each client is returned in kilobytes. If the device is a
       switch, the switchport is returned; otherwise the switchport
       field is null.

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timespan: The timespan for which clients will be fetched.
           Must be in seconds and less than or equal to a month (2592000
           seconds).

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/devices/{}/clients{}'.format(serial, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_clients_by_client_id_or_mac_or_ip(network_id, id_or_mac_or_ip):
    """Return the client associated with the given identifier. This endpoint
       will lookup by client ID or either the MAC or IP depending on
       whether the network uses Track-by-IP.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @id_or_mac_or_ip: Client ID or Mac or IP
            ↳

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}'.format(network_id,
                                                    id_or_mac_or_ip),
        headers=HEADERS)
    return graceful_exit(response)


def create_client_provision_by_network_id(network_id, params=''):
    """Provisions a client with a name and policy. Clients can be provisioned
       before they associate to the network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - mac: The MAC address of the client. Required.
        - name: The display name for the client. Optional. Limited to
           255 bytes.
        - devicePolicy: The policy to apply to the specified client.
           Can be Whitelisted, Blocked, Normal, and Group policy.
           Required.
        - groupPolicyId: The ID of the desired group policy to apply to
           the client. Required if 'devicePolicy' is set to "Group
           policy". Otherwise this is ignored.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/clients/provision'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_usage_history_by_client_id_or_mac_or_ip(network_id, id_or_mac_or_ip):
    """Return the client's daily usage history. Usage data is in kilobytes.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @id_or_mac_or_ip: Client ID or Mac or IP
            ↳

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/usageHistory'.format(
            network_id, id_or_mac_or_ip),
        headers=HEADERS)
    return graceful_exit(response)


def get_traffic_history_by_client_id_or_mac_or_ip(network_id,
                                                  id_or_mac_or_ip,
                                                  params=''):
    """Return the client's network traffic data over time. Usage data is in
       kilobytes. This endpoint requires detailed traffic analysis to be
       enabled on the Network-wide > General page.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @id_or_mac_or_ip: Client ID or Mac or IP
            ↳
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - perPage: The number of entries per page returned
        - startingAfter: A token used by the server to indicate the
           start of the page. Often this is a timestamp or an ID but it
           is not limited to those. This parameter should not be defined
           by client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.
        - endingBefore: A token used by the server to indicate the end
           of the page. Often this is a timestamp or an ID but it is not
           limited to those. This parameter should not be defined by
           client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/trafficHistory{}'.format(
            network_id, id_or_mac_or_ip, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_events_by_client_id_or_mac_or_ip(network_id,
                                         id_or_mac_or_ip,
                                         params=''):
    """Return the events associated with this client.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @id_or_mac_or_ip: Client ID or Mac or IP
            ↳
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - perPage: The number of entries per page returned
        - startingAfter: A token used by the server to indicate the
           start of the page. Often this is a timestamp or an ID but it
           is not limited to those. This parameter should not be defined
           by client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.
        - endingBefore: A token used by the server to indicate the end
           of the page. Often this is a timestamp or an ID but it is not
           limited to those. This parameter should not be defined by
           client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/events{}'.format(
            network_id, id_or_mac_or_ip, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_latency_history_by_client_id_or_mac_or_ip(network_id,
                                                  id_or_mac_or_ip,
                                                  params=''):
    """Return the latency history for a client. The latency data is from a
       sample of 2% of packets and is grouped into 4 traffic categories:
       background, best effort, video, voice. Within these categories
       the sampled packet counters are bucketed by latency in
       milliseconds.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @id_or_mac_or_ip: Client ID or Mac or IP
            ↳
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timespan: The timespan in seconds for the data
        - t0: The start time, in seconds from epoch, for the data
        - t1: The end time, in seconds from epoch, for the data

    Returns: (None)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/latencyHistory{}'.format(
            network_id, id_or_mac_or_ip, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_policy_by_client_mac(network_id, mac, params=''):
    """Return the policy assigned to a client on the network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @mac: Client MAC
            ↳ get_clients_by_serial(serial, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timespan: The timespan for which clients will be fetched.
           Must be in seconds and less than or equal to a month (2592000
           seconds).

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/policy{}'.format(
            network_id, mac, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def update_policy_by_client_mac(network_id, mac, params=''):
    """Update the policy assigned to a client on the network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @mac: Client MAC
            ↳ get_clients_by_serial(serial, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - devicePolicy: The group policy (Whitelisted, Blocked, Normal,
           Group policy)
        - groupPolicyId: [optional] If devicePolicy param is set to
           'Group policy' this param is used to specify the group ID.
        - timespan: The timespan for which clients will be fetched.
           Must be in seconds and less than or equal to a month (2592000
           seconds).

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/clients/{}/policy'.format(network_id, mac),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_splash_authorization_status_by_client_mac(network_id, mac):
    """Return the splash authorization for a client, for each SSID they've
       associated with through splash.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @mac: Client MAC
            ↳ get_clients_by_serial(serial, params)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/splashAuthorizationStatus'.format(
            network_id, mac),
        headers=HEADERS)
    return graceful_exit(response)


def update_splash_authorization_status_by_client_mac(network_id,
                                                     mac,
                                                     params=''):
    """Update a client's splash authorization.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @mac: Client MAC
            ↳ get_clients_by_serial(serial, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - ssids: The target SSIDs. For each SSID where isAuthorized is
           true, the expiration time will automatically be set according
           to the SSID's splash frequency.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/clients/{}/splashAuthorizationStatus'.format(
            network_id, mac),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_config_templates_by_org_id(org_id):
    """List the configuration templates for this organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/configTemplates'.format(org_id),
        headers=HEADERS)
    return graceful_exit(response)


def delete_config_template_by_config_template_id(org_id, config_template_id):
    """Remove a configuration template

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @config_template_id: (eg N_24329156)
            ↳ get_config_templates_by_org_id(org_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/organizations/{}/configTemplates/{}'.format(
            org_id, config_template_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_devices_by_network_id(network_id):
    """List the devices in a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/devices'.format(network_id), headers=HEADERS)
    return graceful_exit(response)


def get_devices_by_device_serial(network_id, serial):
    """Return a single device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/devices/{}'.format(network_id, serial),
        headers=HEADERS)
    return graceful_exit(response)


def get_performance_by_device_serial(network_id, serial):
    """Return the performance score for a single device. Only primary MX
       devices supported. If no data is available, a 204 error code is
       returned.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/devices/{}/performance'.format(
            network_id, serial),
        headers=HEADERS)
    return graceful_exit(response)


def get_uplink_by_device_serial(network_id, serial):
    """Return the uplink information for a device.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/devices/{}/uplink'.format(network_id, serial),
        headers=HEADERS)
    return graceful_exit(response)


def update_device_by_device_serial(network_id, serial, params=''):
    """Update the attributes of a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of a device
        - tags: The tags of a device
        - lat: The latitude of a device
        - lng: The longitude of a device
        - address: The address of a device
        - notes: The notes for the device. String. Limited to 255
           characters.
        - moveMapMarker: Whether or not to set the latitude and
           longitude of a device based on the new address. Only applies
           when lat and lng are not specified.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/devices/{}'.format(network_id, serial),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_device_claim_by_network_id(network_id, params=''):
    """Claim a device into a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - serial: The serial of a device

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/devices/claim'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_remove_by_device_serial(network_id, serial):
    """Remove a single device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/devices/{}/remove'.format(network_id, serial),
        headers=HEADERS)
    return graceful_exit(response)


def get_lldp_cdp_by_device_serial(network_id, serial, params=''):
    """List LLDP and CDP information for a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timespan: The timespan for which LLDP and CDP information
           will be fetched. Must be in seconds and less than or equal to
           a month (2592000 seconds). LLDP and CDP information is sent
           to the Meraki dashboard every 10 minutes. In instances where
           this LLDP and CDP information matches an existing entry in
           the Meraki dashboard, the data is updated once every two
           hours. Meraki recommends querying LLDP and CDP information at
           an interval slightly greater than two hours, to ensure that
           unchanged CDP / LLDP information can be queried consistently.

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/devices/{}/lldp_cdp{}'.format(
            network_id, serial, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_loss_and_latency_history_by_device_serial(network_id,
                                                  serial,
                                                  params=''):
    """Get the uplink loss percentage and latency in milliseconds for a wired
       network device.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: The beginning of the timespan for the data. The maximum
           lookback period is 12 months from today.
        - t1: The end of the timespan for the data. t1 can be a max of
           1 month after t0.
        - timespan: The timespan for which the information will be
           fetched. If specifying timespan, do not specify parameters t0
           and t1. The value must be in seconds and less than or equal
           to a month (2592000 seconds).
        - resolution: The time resolution in seconds for returned data.
           The valid resolutions are 60, 600, 3600, 86400. The default
           is 60.
        - uplink: The WAN uplink used to obtain the requested stats.
           Valid uplinks are wan1, wan2. The default is wan1.
        - ip: The destination IP used to obtain the requested stats.
           This is required.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/devices/{}/lossAndLatencyHistory{}'.format(
            network_id, serial, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_cellular_firewall_rules_by_network_id(network_id):
    """Return the cellular firewall rules for an MX network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/cellularFirewallRules'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_cellular_firewall_rule_by_network_id(network_id, params=''):
    """Update the cellular firewall rules of an MX network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - rules: An ordered array of the firewall rules (not including
           the default rule)

    Returns: (list)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/cellularFirewallRules'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_l3_firewall_rules_by_network_id(network_id):
    """Return the L3 firewall rules for an MX network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/l3FirewallRules'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_l3_firewall_rule_by_network_id(network_id, params=''):
    """Update the L3 firewall rules of an MX network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - rules: An ordered array of the firewall rules (not including
           the default rule)
        - syslogDefaultRule: Log the special default rule (boolean
           value - enable only if you've configured a syslog server)
           (optional)

    Returns: (list)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/l3FirewallRules'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_vpn_firewall_rules_by_org_id(org_id):
    """Return the firewall rules for an organization's site-to-site VPN

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/vpnFirewallRules'.format(org_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_vpn_firewall_rule_by_org_id(org_id, params=''):
    """Update firewall rules of an organization's site-to-site VPN

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - rules: An ordered array of the firewall rules (not including
           the default rule)
        - syslogDefaultRule: Log the special default rule (boolean
           value - enable only if you've configured a syslog server)
           (optional)

    Returns: (list)

    """
    response = requests.put(
        BASE_URL + '/organizations/{}/vpnFirewallRules'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_l3_firewall_rules_by_ssid_number(network_id, ssid_number):
    """Return the L3 firewall rules for an SSID on an MR network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @ssid_number: Positional number of the SSID in the list (0-14)
            ↳ get_ssids_by_network_id(network_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/ssids/{}/l3FirewallRules'.format(
            network_id, ssid_number),
        headers=HEADERS)
    return graceful_exit(response)


def update_l3_firewall_rule_by_ssid_number(network_id, ssid_number, params=''):
    """Update the L3 firewall rules of an SSID on an MR network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @ssid_number: Positional number of the SSID in the list (0-14)
            ↳ get_ssids_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - rules: An ordered array of the firewall rules for this SSID
           (not including the local LAN access rule or the default rule)
        - allowLanAccess: Allow wireless client access to local LAN
           (boolean value - true allows access and false denies access)
           (optional)

    Returns: (list)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/ssids/{}/l3FirewallRules'.format(
            network_id, ssid_number),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_group_policies_by_network_id(network_id):
    """List the group policies in a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/groupPolicies'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_http_servers_by_network_id(network_id):
    """List the HTTP servers for a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/httpServers'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_http_servers_by_http_server_id(network_id, http_server_id):
    """Return an HTTP server

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @http_server_id: Webhook HTTP server ID. See
                https://documentation.meraki.com/z
                General_Administration/Other_Topics/Webhooks
            ↳ get_http_servers_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/httpServers/{}'.format(
            network_id, http_server_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_http_server_by_http_server_id(network_id, http_server_id,
                                         params=''):
    """Update an HTTP server

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @http_server_id: Webhook HTTP server ID. See
                https://documentation.meraki.com/z
                General_Administration/Other_Topics/Webhooks
            ↳ get_http_servers_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: A name for easy reference to the HTTP server
        - url: The URL of the HTTP server
        - sharedSecret: A shared secret that will be included in POSTs
           sent to the HTTP server. This secret can be used to verify
           that the request was sent by Meraki.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/httpServers/{}'.format(
            network_id, http_server_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_http_server_by_network_id(network_id, params=''):
    """Add an HTTP server

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: A name for easy reference to the HTTP server
        - url: The URL of the HTTP server
        - sharedSecret: A shared secret that will be included in POSTs
           sent to the HTTP server. This secret can be used to verify
           that the request was sent by Meraki.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/httpServers'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_http_server_by_http_server_id(network_id, http_server_id):
    """Delete an HTTP server

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @http_server_id: Webhook HTTP server ID. See
                https://documentation.meraki.com/z
                General_Administration/Other_Topics/Webhooks
            ↳ get_http_servers_by_network_id(network_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/httpServers/{}'.format(
            network_id, http_server_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_http_server_webhook_test_by_network_id(network_id, params=''):
    """Send a test webhook

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - url: The URL where the test webhook will be sent

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/httpServers/webhookTests'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_webhook_tests_by_webhook_test_id(network_id, webhook_test_id):
    """Return the status of a webhook test

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @webhook_test_id: ID of webhook test sent to your HTTP server. See
                https://documentation.meraki.com/z
                General_Administration/Other_Topics/Webhooks
            ↳ create_http_servers_webhook_tests_by_network_id(
                network_id, params)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/httpServers/webhookTests/{}'.format(
            network_id, webhook_test_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_meraki_auth_users_by_network_id(network_id):
    """List the splash or RADIUS users configured under Meraki Authentication
       for a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/merakiAuthUsers'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_meraki_auth_users_by_meraki_auth_user_id(network_id,
                                                 meraki_auth_user_id):
    """Return the Meraki Auth splash or RADIUS user

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @meraki_auth_user_id: Splash or RADIUS user hash (eg aGlAaGkuY29t)
            ↳ get_meraki_auth_users_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/merakiAuthUsers/{}'.format(
            network_id, meraki_auth_user_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_networks_by_org_id(org_id, params=''):
    """List the networks in an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - configTemplateId: An optional parameter that is the ID of a
           config template. Will return all networks bound to that
           template.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/organizations/{}/networks{}'.format(
            org_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_networks_by_network_id(network_id):
    """Return a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}'.format(network_id), headers=HEADERS)
    return graceful_exit(response)


def update_network_by_network_id(network_id, params=''):
    """Update a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the new network
        - timeZone: The timezone of the network. For a list of allowed
           timezones, please see the
        - tags: A space-separated list of tags to be applied to the
           network
        - disableMyMerakiCom: Disables the local device status pages (h
           ttp://my.meraki.com/http://ap.meraki.com/http://switch.meraki
           .com/http://wired.meraki.com/). Optional (defaults to false)
        - disableRemoteStatusPage: Disables access to the device status
           page (<a target=. Optional. Can only be set if
           disableMyMerakiCom is set to false

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_network_by_org_id(org_id, params=''):
    """Create a network

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the new network
        - type: The type of the new network. Valid types are wireless,
           appliance, switch, phone, systemsManager, camera or a space-
           separated list of those for a combined network.
        - tags: A space-separated list of tags to be applied to the
           network
        - timeZone: The timezone of the network. For a list of allowed
           timezones, please see the
        - copyFromNetworkId: The ID of the network to copy
           configuration from. Other provided parameters will override
           the copied configuration, except type which must match this
           network's type exactly.
        - disableMyMerakiCom: Disables the local device status pages (h
           ttp://my.meraki.com/http://ap.meraki.com/http://switch.meraki
           .com/http://wired.meraki.com/). Optional (defaults to false)
        - disableRemoteStatusPage: Disables access to the device status
           page (<a target=. Optional. Can only be set if
           disableMyMerakiCom is set to false

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/organizations/{}/networks'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_network_by_network_id(network_id):
    """Delete a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}'.format(network_id), headers=HEADERS)
    return graceful_exit(response)


def create_bind_by_network_id(network_id, params=''):
    """Bind a network to a template.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - configTemplateId: The ID of the template to which the network
           should be bound.
        - autoBind: Optional boolean indicating whether the network's
           switches should automatically bind to profiles of the same
           model. Defaults to false if left unspecified. This option
           only affects switch networks and switch templates. Auto-bind
           is not valid unless the switch template has at least one
           profile and has at most one profile per switch model.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/bind'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_unbind_by_network_id(network_id):
    """Unbind a network from a template.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/unbind'.format(network_id), headers=HEADERS)
    return graceful_exit(response)


def get_site_to_site_vpn_by_network_id(network_id):
    """Return the site-to-site VPN settings of a network. Only valid for MX
       networks.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/siteToSiteVpn'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_site_to_site_vpn_by_network_id(network_id, params=''):
    """Update the site-to-site VPN settings of a network. Only valid for MX
       networks in NAT mode.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - mode: The site-to-site VPN mode: hub, spoke, or none
        - hubs: The list of VPN hubs, in order of preference. In spoke
           mode, at least 1 hub is required.
        - subnets: The list of subnets and their VPN presence.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/siteToSiteVpn'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_traffic_by_network_id(network_id, params=''):
    """The traffic analysis data for this network. https://documentation.meraki
       .com/MR/Monitoring_and_Reporting/Hostname_Visibility must be
       enabled on the network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timespan: The timespan for the data.  Must be an integer
           representing a duration in seconds between two hours and one
           month. (Mandatory.)
        - deviceType: Filter the data by device type: combined
           (default), wireless, switch, appliance. When using combined,
           for each rule the data will come from the device type with
           the most usage.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/traffic{}'.format(network_id, params,
                                                   url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_access_policies_by_network_id(network_id):
    """List the access policies for this network. Only valid for MS networks.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/accessPolicies'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_air_marshal_by_network_id(network_id, params=''):
    """List Air Marshal scan results from a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timespan: The timespan for which results will be fetched.
           Must be at most one month in seconds.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/airMarshal{}'.format(network_id, params,
                                                      url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_bluetooth_settings_by_network_id(network_id):
    """Return the Bluetooth settings for a network.
       https://documentation.meraki.com/MR/Bluetooth/Bluetooth_Low_Energ
       y_(BLE) must be enabled on the network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/bluetoothSettings'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_bluetooth_settings_by_network_id(network_id, params=''):
    """Update the Bluetooth settings for a network. See the docs page for https
       ://documentation.meraki.com/MR/Bluetooth/Bluetooth_Low_Energy_(BL
       E).

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - scanningEnabled: Whether APs will scan for Bluetooth enabled
           clients. (true, false)
        - advertisingEnabled: Whether APs will advertise beacons.
           (true, false)
        - uuid: The UUID to be used in the beacon identifier.
        - majorMinorAssignmentMode: The way major and minor number
           should be assigned to nodes in the network. ('Unique', 'Non-
           unique')
        - major: The major number to be used in the beacon identifier.
           Only valid in 'Non-unique' mode.
        - minor: The minor number to be used in the beacon identifier.
           Only valid in 'Non-unique' mode.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/bluetoothSettings'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_orgs():
    """List the organizations that the user has privileges on

    Returns: (list)
"""
    response = requests.get(
        BASE_URL + '/organizations'.format(), headers=HEADERS)
    return graceful_exit(response)


def get_orgs_by_org_id(org_id):
    """Return an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}'.format(org_id), headers=HEADERS)
    return graceful_exit(response)


def update_org_by_org_id(org_id, params=''):
    """Update an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the organization

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/organizations/{}'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_org(params=''):
    """Create a new organization

    Args:
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the organization

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/organizations'.format(),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_clone_by_org_id(org_id, params=''):
    """Create a new organization by cloning the addressed organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the new organization

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/organizations/{}/clone'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_claim_by_org_id(org_id, params=''):
    """Claim a device, license key, or order into an organization. When
       claiming by order, all devices and licenses in the order will be
       claimed; licenses will be added to the organization and devices
       will be placed in the organization's inventory. These three types
       of claims are mutually exclusive and cannot be performed in one
       request.

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - order: The order number that should be claimed
        - serial: The serial of the device that should be claimed
        - licenseKey: The license key that should be claimed
        - licenseMode: Either  for more information.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/organizations/{}/claim'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_license_state_by_org_id(org_id):
    """Return the license state for an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/licenseState'.format(org_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_inventory_by_org_id(org_id):
    """Return the inventory for an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/inventory'.format(org_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_device_statuses_by_org_id(org_id):
    """List the status of every Meraki device in the organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/deviceStatuses'.format(org_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_snmp_by_org_id(org_id):
    """Return the SNMP settings for an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/snmp'.format(org_id), headers=HEADERS)
    return graceful_exit(response)


def update_snmp_by_org_id(org_id, params=''):
    """Update the SNMP settings for an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - v2cEnabled: Boolean indicating whether SNMP version 2c is
           enabled for the organization
        - v3Enabled: Boolean indicating whether SNMP version 3 is
           enabled for the organization
        - v3AuthMode: The SNMP version 3 authentication mode either MD5
           or SHA
        - v3AuthPass: The SNMP version 3 authentication password.  Must
           be at least 8 characters if specified.
        - v3PrivMode: The SNMP version 3 privacy mode DES or AES128
        - v3PrivPass: The SNMP version 3 privacy password.  Must be at
           least 8 characters if specified.
        - peerIps: The IPs that are allowed to access the SNMP server.
           This list should be IPv4 addresses separated by semi-colons
           (ie. "1.2.3.4;2.3.4.5").

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/organizations/{}/snmp'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_third_party_vpn_peers_by_org_id(org_id):
    """Return the third party VPN peers for an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/thirdPartyVPNPeers'.format(org_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_third_party_vpn_peer_by_org_id(org_id, params=''):
    """Update the third party VPN peers for an organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the VPN peer
        - publicIp: The public IP of the VPN peer
        - privateSubnets: The list of the private subnets of the VPN
           peer
        - ipsecPolicies: Custom IPsec policies for the VPN peer. If not
           included and a preset has not been chosen, the default preset
           for IPsec policies will be used.
        - ipsecPoliciesPreset: One of the following available presets:
           "default", "aws", "azure". If this is provided, the
           IPsecPolicies parameter is ignored.
        - secret: The shared secret with the VPN peer
        - networkTags: A list of network tags that will connect with
           this peer. Use "all" for all networks. Use "none" for no
           networks. If missing, default is "all".

    Returns: (list)

    """
    response = requests.put(
        BASE_URL + '/organizations/{}/thirdPartyVPNPeers'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_announcements_by_network_id(network_id):
    """List all announcement groups in a network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneAnnouncements'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_phone_announcement_by_network_id(network_id, params=''):
    """Add an announcement group.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The full name of the new announcement group.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/phoneAnnouncements'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_phone_announcement_by_phone_announcement_id(network_id,
                                                       phone_announcement_id):
    """Delete an announcement group.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @phone_announcement_id: Announcement ID (eg 1284392014819)
            ↳ get_phone_announcements_by_network_id(network_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/phoneAnnouncements/{}'.format(
            network_id, phone_announcement_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_assignments_by_network_id(network_id):
    """List all phones in a network and their contact assignment

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneAssignments'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_assignments_by_phone_assignment_serial(network_id, serial):
    """Return a phone's contact assignment

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneAssignments/{}'.format(
            network_id, serial),
        headers=HEADERS)
    return graceful_exit(response)


def update_phone_assignment_by_phone_assignment_serial(network_id,
                                                       serial,
                                                       params=''):
    """Assign a contact and number(s) to a phone

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - contactId: The ID of the contact (obtained from 'Phone
           Contacts' API)
        - contactType: The type of contact to bind: 'Dashboard' or
           'Google' (obtained from 'Phone Contacts' API)
        - publicNumber: The public number(s) in E.164 format (obtained
           from 'Phone Numbers' API) as an array of strings. Multiple
           numbers per phone are allowed.
    Omitting this paramater
           will remove the public number assignment(s).
        - ext: The 4-6 digit extension. Extension cannot be in use.
           Omitting this parameter will remove the extension assignment.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/phoneAssignments/{}'.format(
            network_id, serial),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_phone_assignment_by_phone_assignment_serial(network_id, serial):
    """Remove a phone assignment (unprovision a phone)

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/phoneAssignments/{}'.format(
            network_id, serial),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_callgroups_by_network_id(network_id):
    """List all call groups in a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneCallgroups'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_callgroups_by_phone_callgroup_id(network_id, phone_callgroup_id):
    """Show a call group's details

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @phone_callgroup_id: Callgroup ID (eg 178449602133687616)
            ↳ get_phone_callgroups_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneCallgroups/{}'.format(
            network_id, phone_callgroup_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_phone_callgroup_by_network_id(network_id, params=''):
    """Create a new call group.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The call group name.
        - ext: The 4-6 digit extension. Extension cannot be in use.
        - publicNumber: The public number in E.164 format (obtained
           from 'Phone Numbers' API)
        - ringStrategy: Ring strategy: options: 'ring-all', 'longest-
           idle-agent', 'round-robin'
        - scope: Device Scope: options: 'all' - All devices, 'some' -
           Devices with ANY of the following tags (specify tags field),
           'all_tags' - Devices with ALL of the following tags (specify
           tags field), 'without_all_tags' - Devices WITHOUT ALL of the
           following tags (specify tags field)
        - tags: Scope tags (use if scope is 'some', 'all_tags', or
           'without_all_tags'). Submit as array of text. ex: ["sales",
           "eng"]
        - allowExternalForwards: Allow external forwards. Boolean true
           or false
        - waitTimeEnabled: Enable Max Wait Time. Boolean true or false
        - maxWaitTime: Max wait time in seconds.
        - noAnswerAction: No answer action: options: 'hang-up',
           'transfer-to-ext'. If 'transfer-to-ext', use the
           transferExtension field
        - transferExtension: Use if noAnswerAction is 'transfer-to-ext.
           The extension to transfer to after wait time expires. The
           extension must exist on the network. Submit the 4-6 digit
           extension as text.'

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/phoneCallgroups/'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_phone_callgroup_by_phone_callgroup_id(network_id,
                                                 phone_callgroup_id,
                                                 params=''):
    """Update a call group's details. Only submit parameters you would like to
       update. Omitting any parameters will leave them as-is.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @phone_callgroup_id: Callgroup ID (eg 178449602133687616)
            ↳ get_phone_callgroups_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The call group name.
        - ext: The 4-6 digit extension. Extension cannot be in use.
        - publicNumber: The public number(s) in E.164 format (obtained
           from 'Phone Numbers' API)
        - ringStrategy: Ring strategy: options: 'ring-all', 'longest-
           idle-agent', 'round-robin'
        - scope: Device Scope: options: 'all' - All devices, 'some' -
           Devices with ANY of the following tags (specify tags field),
           'all_tags' - Devices with ALL of the following tags (specify
           tags field), 'without_all_tags' - Devices WITHOUT ALL of the
           following tags (specify tags field)
        - tags: Scope tags (use if scope is 'some', 'all_tags', or
           'without_all_tags'). Submit as array of text. ex: ["sales",
           "eng"]
        - allowExternalForwards: Allow external forwards. Boolean true
           or false
        - waitTimeEnabled: Enable Max Wait Time. Boolean true or false
        - maxWaitTime: Max wait time in seconds.
        - noAnswerAction: No answer action: options: 'hang-up',
           'transfer-to-ext'. If 'transfer-to-ext', use the
           transferExtension field
        - transferExtension: The extension to transfer to after wait
           time expires. Submit the 4-6 digit extension as text. Use if
           noAnswerAction is 'transfer-to-ext'

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/phoneCallgroups/{}'.format(
            network_id, phone_callgroup_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_phone_callgroup_by_phone_callgroup_id(network_id,
                                                 phone_callgroup_id):
    """Delete a call group

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @phone_callgroup_id: Callgroup ID (eg 178449602133687616)
            ↳ get_phone_callgroups_by_network_id(network_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/phoneCallgroups/{}'.format(
            network_id, phone_callgroup_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_conference_rooms_by_network_id(network_id):
    """List all the phone conference rooms in a network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneConferenceRooms'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_conference_rooms_by_phone_conference_room_id(
        network_id, phone_conference_room_id):
    """Show a conference room's details.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @phone_conference_room_id: Room ID (eg 563512903374733359)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneConferenceRooms/{}'.format(
            network_id, phone_conference_room_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_phone_conference_room_by_network_id(network_id, params=''):
    """Add a conference room.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The full name of the new conference room.
        - description: The description of the new conference room.
        - ext: The extension of the new conference room.
        - publicNumber: The public number of the new conference room.
        - maxMembers: The max members allowed in the new conference
           room.
        - pin: Password that must be entered before being allowed in
           the conference room.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/phoneConferenceRooms'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_phone_conference_room_by_phone_conference_room_id(
        network_id, phone_conference_room_id, params=''):
    """Update a conference room's. Only submit parameters you would like to
       update. Omitting any parameters will leave them as-is.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @phone_conference_room_id: Room ID (eg 563512903374733359)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The full name of the conference room.
        - description: The description of the conference room.
        - ext: The extension of the conference room.
        - publicNumber: The public number of the conference room.
        - maxMembers: The max members allowed in the conference room.
        - pin: Password that must be entered before being allowed in
           the conference room.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/phoneConferenceRooms/{}'.format(
            network_id, phone_conference_room_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_phone_conference_room_by_phone_conference_room_id(
        network_id, phone_conference_room_id):
    """Delete a conference room.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @phone_conference_room_id: Room ID (eg 563512903374733359)
            ↳ get_networks_by_org_id(org_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/phoneConferenceRooms/{}'.format(
            network_id, phone_conference_room_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_contacts_by_network_id(network_id):
    """List the phone contacts in a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneContacts'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_phone_contact_by_network_id(network_id, params=''):
    """Add a contact

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The full name of the new contact

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/phoneContacts'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_phone_contact_by_phone_contact_contact_id(network_id,
                                                     contact_id,
                                                     params=''):
    """Update a phone contact. Google Directory contacts cannot be modified.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @contact_id: Phone contact ID (eg 823)
            ↳ get_phone_assignments_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the contact

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/phoneContacts/{}'.format(
            network_id, contact_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_phone_contact_by_phone_contact_contact_id(network_id, contact_id):
    """Delete a phone contact. Google Directory contacts cannot be removed.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @contact_id: Phone contact ID (eg 823)
            ↳ get_phone_assignments_by_network_id(network_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/phoneContacts/{}'.format(
            network_id, contact_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_numbers_by_network_id(network_id):
    """List all the phone numbers in a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneNumbers'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_phone_numbers_available_by_network_id(network_id):
    """List the available phone numbers in a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/phoneNumbers/available'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_pii_pii_keys_by_network_id(network_id, params=''):
    """List the keys required to access Personally Identifiable Information
       (PII) for a given identifier. Exactly one identifier will be
       accepted. If the organization contains org-wide Systems Manager
       users matching the key provided then there will be an entry with
       the key "0" containing the applicable keys.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - username: The username of a Systems Manager user
        - email: The email of a network user account or a Systems
           Manager device
        - mac: The MAC of a network client device or a Systems Manager
           device
        - serial: The serial of a Systems Manager device
        - imei: The IMEI of a Systems Manager device
        - bluetoothMac: The MAC of a Bluetooth client

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/pii/piiKeys{}'.format(network_id, params,
                                                       url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_pii_sm_devices_for_key_by_network_id(network_id, params=''):
    """Given a piece of Personally Identifiable Information (PII), return the
       Systems Manager device ID(s) associated with that identifier.
       These device IDs can be used with the Systems Manager API
       endpoints to retrieve device details. Exactly one identifier will
       be accepted.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - username: The username of a Systems Manager user
        - email: The email of a network user account or a Systems
           Manager device
        - mac: The MAC of a network client device or a Systems Manager
           device
        - serial: The serial of a Systems Manager device
        - imei: The IMEI of a Systems Manager device
        - bluetoothMac: The MAC of a Bluetooth client

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/pii/smDevicesForKey{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_pii_sm_owners_for_key_by_network_id(network_id, params=''):
    """Given a piece of Personally Identifiable Information (PII), return the
       Systems Manager owner ID(s) associated with that identifier.
       These owner IDs can be used with the Systems Manager API
       endpoints to retrieve owner details. Exactly one identifier will
       be accepted.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - username: The username of a Systems Manager user
        - email: The email of a network user account or a Systems
           Manager device
        - mac: The MAC of a network client device or a Systems Manager
           device
        - serial: The serial of a Systems Manager device
        - imei: The IMEI of a Systems Manager device
        - bluetoothMac: The MAC of a Bluetooth client

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/pii/smOwnersForKey{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_pii_requests_by_network_id(network_id):
    """List the PII requests for this network or organization

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/pii/requests'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_requests_by_request_id(network_id, request_id):
    """Return a PII request

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @request_id: PII request ID (eg 1234)
            ↳ get_pii_requests_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/pii/requests/{}'.format(
            network_id, request_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_pii_request_by_network_id(network_id, params=''):
    """Submit a new delete or restrict processing PII request

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - type: One of "delete" or "restrict processing"
        - datasets: The datasets related to the provided key that
           should be deleted. Only applies to "delete" requests. The
           value "all" will be expanded to all datasets applicable to
           this type. The datasets by applicable to each type are: mac
           (usage, events, traffic), email (users, loginAttempts),
           username (users, loginAttempts), bluetoothMac (client,
           connectivity), smDeviceId (device), smUserId (user)
        - username: The username of a network log in. Only applies to
           "delete" requests.
        - email: The email of a network user account. Only applies to
           "delete" requests.
        - mac: The MAC of a network client device. Applies to both
           "restrict processing" and "delete" requests.
        - smDeviceId: The sm_device_id of a Systems Manager device. The
           only way to "restrict processing" or "delete" a Systems
           Manager device. Must include "device" in the dataset for a
           "delete" request to destroy the device.
        - smUserId: The sm_user_id of a Systems Manager user. The only
           way to "restrict processing" or "delete" a Systems Manager
           user. Must include "user" in the dataset for a "delete"
           request to destroy the user.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/pii/requests'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_request_by_request_id(network_id, request_id):
    """Delete a restrict processing PII request

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @request_id: PII request ID (eg 1234)
            ↳ get_pii_requests_by_network_id(network_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/pii/requests/{}'.format(
            network_id, request_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_saml_roles_by_org_id(org_id):
    """List the SAML roles for this organization

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/samlRoles'.format(org_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_saml_roles_by_saml_role_id(org_id, saml_role_id):
    """Return a SAML role

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @saml_role_id: ID unique to SAML User (eg TEdJIEN1c3RvbWVy)
            ↳ get_saml_roles_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/organizations/{}/samlRoles/{}'.format(
            org_id, saml_role_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_saml_role_by_saml_role_id(org_id, saml_role_id, params=''):
    """Update a SAML role

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @saml_role_id: ID unique to SAML User (eg TEdJIEN1c3RvbWVy)
            ↳ get_saml_roles_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - role: The role of the SAML administrator
        - orgAccess: The privilege of the SAML administrator on the
           organization
        - tags: The list of tags that the SAML administrator has
           privileges on
        - networks: The list of networks that the SAML administrator
           has privileges on

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/organizations/{}/samlRoles/{}'.format(
            org_id, saml_role_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_saml_role_by_org_id(org_id, params=''):
    """Create a SAML role

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - role: The role of the SAML administrator
        - orgAccess: The privilege of the SAML administrator on the
           organization
        - tags: The list of tags that the SAML administrator has
           privileges on
        - networks: The list of networks that the SAML administrator
           has privileges on

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/organizations/{}/samlRoles'.format(org_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_saml_role_by_saml_role_id(org_id, saml_role_id):
    """Remove a SAML role

    Args:
        @org_id: (eg 212406)
            ↳ get_orgs()
        @saml_role_id: ID unique to SAML User (eg TEdJIEN1c3RvbWVy)
            ↳ get_saml_roles_by_org_id(org_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/organizations/{}/samlRoles/{}'.format(
            org_id, saml_role_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_security_events_by_client_id(network_id, client_id, params=''):
    """List the security events

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @client_id: Client ID Hash (eg k74272e)
            ↳ get_clients_by_serial(serial)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - timespan: The timespan, in seconds, to look back from now for
           events
        - perPage: The number of entries per page returned
        - startingAfter: A token used by the server to indicate the
           start of the page. Often this is a timestamp or an ID but it
           is not limited to those. This parameter should not be defined
           by client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.
        - endingBefore: A token used by the server to indicate the end
           of the page. Often this is a timestamp or an ID but it is not
           limited to those. This parameter should not be defined by
           client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/securityEvents{}'.format(
            network_id, client_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_sm_target_groups_by_network_id(network_id, params=''):
    """List the target groups in this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - withDetails: Boolean indicating if the the ids of the devices
           or users scoped by the target group should be included in the
           response

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/targetGroups{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_target_groups_by_target_group_id(network_id,
                                         target_group_id,
                                         params=''):
    """Return a target group

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @target_group_id: WARNING: Untracked API Primitive: `target_group_id`. Please create an issue.
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - withDetails: Boolean indicating if the the ids of devices or
           users scoped by the target group should be included in the
           response

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/targetGroups/{}{}'.format(
            network_id, target_group_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def update_target_group_by_target_group_id(network_id,
                                           target_group_id,
                                           params=''):
    """Update a target group

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @target_group_id: WARNING: Untracked API Primitive: `target_group_id`. Please create an issue.
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of this target group
        - scope: The scope and tag options of the target group. Comma
           separated values beginning with one of withAny, withAll,
           withoutAny, withoutAll, all, none, followed by tags

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/targetGroups/{}'.format(
            network_id, target_group_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_sm_target_group_by_network_id(network_id, params=''):
    """Add a target group

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of this target group
        - scope: The scope and tag options of the target group. Comma
           separated values beginning with one of withAny, withAll,
           withoutAny, withoutAll, all, none, followed by tags

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/sm/targetGroups'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_target_group_by_target_group_id(network_id, target_group_id):
    """Delete a target group from a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @target_group_id: WARNING: Untracked API Primitive: `target_group_id`. Please create an issue.

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/sm/targetGroups/{}'.format(
            network_id, target_group_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_sm_profile_clarity_by_network_id(network_id, params=''):
    """Create a new profile containing a Cisco Clarity payload

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name to be given to the new profile
        - scope: The scope (one of all, none, withAny, withAll,
           withoutAny, or withoutAll) and a set of tags of the devices
           to be assigned
        - PluginBundleID: The bundle ID of the application, defaults to
           com.cisco.ciscosecurity.app
        - FilterBrowsers: Whether or not to enable browser traffic
           filtering (one of true, false). Default true.
        - FilterSockets: Whether or not to enable socket traffic
           filtering (one of true, false). Default true.
        - VendorConfig: The specific VendorConfig to be passed to the
           filtering framework, as JSON. VendorConfig should be an array
           of objects, as:
[ { "key": "some_key", type: "some_type",
           "value": "some_value" }, ... ]

type is one of manual_string,
           manual_int, manual_boolean, manual_choice,
           manual_multiselect, manual_list,
auto_username, auto_email,
           auto_mac_address, auto_serial_number, auto_notes, auto_name

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/sm/profile/clarity'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_clarity_by_clarity_profile_id(network_id, profile_id, params=''):
    """Update an existing profile containing a Cisco Clarity payload

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @profile_id: Cisco Clarity Profile ID (eg 12345)
            ↳ create_profile_clarity_by_network_id(network_id, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: optional: A new name for the profile
        - scope: optional: A new scope for the profile (one of all,
           none, withAny, withAll, withoutAny, or withoutAll) and a set
           of tags of the devices to be assigned
        - PluginBundleID: optional: The new bundle ID of the
           application
        - FilterBrowsers: optional: Whether or not to enable browser
           traffic filtering (one of true, false).
        - FilterSockets: optional: Whether or not to enable socket
           traffic filtering (one of true, false).
        - VendorConfig: optional: The specific VendorConfig to be
           passed to the filtering framework, as JSON. VendorConfig
           should be an array of objects, as:
[ { "key": "some_key",
           type: "some_type", "value": "some_value" }, ... ]

type is
           one of manual_string, manual_int, manual_boolean,
           manual_choice, manual_multiselect, manual_list,
           auto_username, auto_email, auto_mac_address,
           auto_serial_number, auto_notes, auto_name

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/profile/clarity/{}'.format(
            network_id, profile_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_clarity_by_clarity_profile_id(network_id, profile_id, params=''):
    """Add a Cisco Clarity payload to an existing profile

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @profile_id: Cisco Clarity Profile ID (eg 12345)
            ↳ create_profile_clarity_by_network_id(network_id, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - PluginBundleID: The bundle ID of the application, defaults to
           com.cisco.ciscosecurity.app
        - FilterBrowsers: Whether or not to enable browser traffic
           filtering (one of true, false).
        - FilterSockets: Whether or not to enable socket traffic
           filtering (one of true, false).
        - VendorConfig: The specific VendorConfig to be passed to the
           filtering framework, as JSON. VendorConfig should be an array
           of objects, as:
[ { "key": "some_key", type: "some_type",
           "value": "some_value" }, ... ]

type is one of manual_string,
           manual_int, manual_boolean, manual_choice,
           manual_multiselect, manual_list,
auto_username, auto_email,
           auto_mac_address, auto_serial_number, auto_notes, auto_name

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/sm/profile/clarity/{}'.format(
            network_id, profile_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_clarities_by_clarity_profile_id(network_id, profile_id):
    """Get details for a Cisco Clarity payload

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @profile_id: Cisco Clarity Profile ID (eg 12345)
            ↳ create_profile_clarity_by_network_id(network_id, params)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/profile/clarity/{}'.format(
            network_id, profile_id),
        headers=HEADERS)
    return graceful_exit(response)


def delete_clarity_by_clarity_profile_id(network_id, profile_id):
    """Delete a Cisco Clarity payload. Deletes the entire profile if it's empty
       after removing the payload.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @profile_id: Cisco Clarity Profile ID (eg 12345)
            ↳ create_profile_clarity_by_network_id(network_id, params)

    Returns: (dict)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/sm/profile/clarity/{}'.format(
            network_id, profile_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_sm_profile_umbrella_by_network_id(network_id, params=''):
    """Create a new profile containing a Cisco Umbrella payload

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name to be given to the new profile
        - scope: The scope (one of all, none, withAny, withAll,
           withoutAny, or withoutAll) and a set of tags of the devices
           to be assigned
        - AppBundleIdentifier: The bundle ID of the application,
           defaults to com.cisco.ciscosecurity.app
        - ProviderBundleIdentifier: The bundle ID of the provider,
           defaults to com.cisco.ciscosecurity.app.CiscoUmbrella
        - ProviderConfiguration: The specific ProviderConfiguration to
           be passed to the filtering framework, as JSON.
           ProviderConfiguration should be an array of objects, as:
[ {
           "key": "some_key", type: "some_type", "value": "some_value"
           }, ... ]

type is one of manual_string, manual_int,
           manual_boolean, manual_choice, manual_multiselect,
           manual_list,
auto_username, auto_email, auto_mac_address,
           auto_serial_number, auto_notes, auto_name
        - usesCert: Whether the certificate should be attached to this
           profile (one of true, false).

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/sm/profile/umbrella'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_umbrella_by_umbrella_profile_id(network_id, profile_id, params=''):
    """Update an existing profile containing a Cisco Umbrella payload

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @profile_id: Cisco Clarity Profile ID (eg 12345)
            ↳ create_profile_clarity_by_network_id(network_id, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: optional: A new name for the profile
        - scope: optional: A new scope for the profile (one of all,
           none, withAny, withAll, withoutAny, or withoutAll) and a set
           of tags of the devices to be assigned
        - AppBundleIdentifier: optional: The bundle ID of the
           application
        - ProviderBundleIdentifier: optional: The bundle ID of the
           provider
        - ProviderConfiguration: optional: The specific
           ProviderConfiguration to be passed to the filtering
           framework, as JSON. ProviderConfiguration should be an array
           of objects, as:
[ { "key": "some_key", type: "some_type",
           "value": "some_value" }, ... ]

type is one of manual_string,
           manual_int, manual_boolean, manual_choice,
           manual_multiselect, manual_list,
auto_username, auto_email,
           auto_mac_address, auto_serial_number, auto_notes, auto_name
        - usesCert: Whether the certificate should be attached to this
           profile (one of true, false). False by default.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/profile/umbrella/{}'.format(
            network_id, profile_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_umbrella_by_umbrella_profile_id(network_id, profile_id, params=''):
    """Add a Cisco Umbrella payload to an existing profile

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @profile_id: Cisco Clarity Profile ID (eg 12345)
            ↳ create_profile_clarity_by_network_id(network_id, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - AppBundleIdentifier: The bundle ID of the application,
           defaults to com.cisco.ciscosecurity.app
        - ProviderBundleIdentifier: The bundle ID of the provider,
           defaults to com.cisco.ciscosecurity.app.CiscoUmbrella
        - ProviderConfiguration: The specific ProviderConfiguration to
           be passed to the filtering framework, as JSON.
           ProviderConfiguration should be an array of objects, as:
[ {
           "key": "some_key", type: "some_type", "value": "some_value"
           }, ... ]

type is one of manual_string, manual_int,
           manual_boolean, manual_choice, manual_multiselect,
           manual_list,
auto_username, auto_email, auto_mac_address,
           auto_serial_number, auto_notes, auto_name
        - usesCert: Whether the certificate should be attached to this
           profile (one of true, false). False by default.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/sm/profile/umbrella/{}'.format(
            network_id, profile_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_umbrellas_by_umbrella_profile_id(network_id, profile_id):
    """Get details for a Cisco Umbrella payload

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @profile_id: Cisco Clarity Profile ID (eg 12345)
            ↳ create_profile_clarity_by_network_id(network_id, params)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/profile/umbrella/{}'.format(
            network_id, profile_id),
        headers=HEADERS)
    return graceful_exit(response)


def delete_umbrella_by_umbrella_profile_id(network_id, profile_id):
    """Delete a Cisco Umbrella payload. Deletes the entire profile if it's
       empty after removing the payload

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @profile_id: Cisco Clarity Profile ID (eg 12345)
            ↳ create_profile_clarity_by_network_id(network_id, params)

    Returns: (dict)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/sm/profile/umbrella/{}'.format(
            network_id, profile_id),
        headers=HEADERS)
    return graceful_exit(response)


def create_sm_app_polari_by_network_id(network_id, params=''):
    """Create a new Polaris app

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - scope: The scope (one of all, none, automatic, withAny,
           withAll, withoutAny, or withoutAll) and a set of tags of the
           devices to be assigned
        - manifestUrl: The manifest URL of the Polaris app (one of
           manifestUrl and bundleId must be provided)
        - bundleId: The bundleId of the Polaris app (one of manifestUrl
           and bundleId must be provided)
        - preventAutoInstall: (optional) Whether or not SM should auto-
           install this app (one of true or false). False by default.
        - usesVPP: (optional) Whether or not the app should use VPP by
           device assignment (one of true or false). False by default.

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/sm/app/polaris'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_polari_by_polari_app_id(network_id, app_id, params=''):
    """Update an existing Polaris app

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @app_id: SM Cisco Polaris app ID (eg 123456)
            ↳ get_app_polaris_by_network_id(network_id, params)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - scope: The scope (one of all, none, automatic, withAny,
           withAll, withoutAny, or withoutAll) and a set of tags of the
           devices to be assigned
        - preventAutoInstall: Whether or not SM should auto-install
           this app (one of true or false). False by default.
        - usesVPP: Whether or not the app should use VPP by device
           assignment (one of true or false). False by default.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/app/polaris/{}'.format(network_id, app_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_sm_app_polaris_by_network_id(network_id, params=''):
    """Get details for a Cisco Polaris app if it exists

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - bundleId: The bundle ID of the app to be found, defaults to
           com.cisco.ciscosecurity.app

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/app/polaris{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def delete_polari_by_polari_app_id(network_id, app_id):
    """Delete a Cisco Polaris app

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @app_id: SM Cisco Polaris app ID (eg 123456)
            ↳ get_app_polaris_by_network_id(network_id, params)

    Returns: (dict)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/sm/app/polaris/{}'.format(network_id, app_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_sm_devices_by_network_id(network_id, params=''):
    """List the devices enrolled in an SM network with various specified fields
       and filters

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - fields: Additional fields that will be displayed for each
           device. Multiple fields can be passed in as comma separated
           values.
      The default fields are: id, name, tags, ssid,
           wifiMac, osName, systemModel, uuid, and serialNumber. The
           additional fields are: ip,
      systemType,
           availableDeviceCapacity, kioskAppName, biosVersion,
           lastConnected, missingAppsCount, userSuppliedAddress,
           location, lastUser,
      ownerEmail, ownerUsername,
           publicIp, phoneNumber, diskInfoJson, deviceCapacity,
           isManaged, hadMdm, isSupervised, meid, imei, iccid,
           simCarrierNetwork, cellularDataUsed, isHotspotEnabled,
           createdAt, batteryEstCharge, quarantined, avName, avRunning,
           asName, fwName,
      isRooted, loginRequired,
           screenLockEnabled, screenLockDelay, autoLoginDisabled,
           autoTags, hasMdm, hasDesktopAgent, diskEncryptionEnabled,
           hardwareEncryptionCaps, passCodeLock, usesHardwareKeystore,
           and androidSecurityPatchVersion.
        - wifiMacs: Filter devices by wifi mac(s). Multiple wifi macs
           can be passed in as comma separated values.
        - serials: Filter devices by serial(s). Multiple serials can be
           passed in as comma separated values.
        - ids: Filter devices by id(s). Multiple ids can be passed in
           as comma separated values.
        - scope: Specify a scope (one of all, none, withAny, withAll,
           withoutAny, or withoutAll) and a set of tags as comma
           separated values.
        - batchToken: On networks with more than 1000 devices, the
           device list will be limited to 1000 devices per query.
           If there are more devices to be seen, a batch token will be
           returned as a part of the device list. To see the remainder
           of
      the devices, pass in the batchToken as a parameter
           in the next request. Requests made with the batchToken do not
           require
      additional parameters as the batchToken
           includes the parameters passed in with the original request.
           Additional parameters
      passed in with the batchToken
           will be ignored.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/devices{}'.format(network_id, params,
                                                      url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_sm_users_by_network_id(network_id, params=''):
    """List the owners in an SM network with various specified fields and
       filters

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - usernames: Filter users by username(s). Multiple usernames
           can be passed in as comma separated values.
        - emails: Filter users by email(s). Multiple emails can be
           passed in as comma separated values.
        - ids: Filter users by id(s). Multiple ids can be passed in as
           comma separated values.
        - scope: Specify a scope (one of all, none, withAny, withAll,
           withoutAny, or withoutAll) and a set of tags as comma
           separated values.

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/users{}'.format(network_id, params,
                                                    url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_device_profiles_by_user_id(network_id, user_id):
    """Get the profiles associated with a user

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @user_id: User ID used for SM (eg 1284392014819)
            ↳ get_sm_users_by_network_id(network_id, params)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/user/{}/deviceProfiles'.format(
            network_id, user_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_device_profiles_by_sm_id(network_id, sm_id):
    """Get the profiles associated with a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/deviceProfiles'.format(
            network_id, sm_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_softwares_by_user_id(network_id, user_id):
    """Get a list of softwares associated with a user

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @user_id: User ID used for SM (eg 1284392014819)
            ↳ get_sm_users_by_network_id(network_id, params)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/user/{}/softwares'.format(
            network_id, user_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_softwares_by_sm_id(network_id, sm_id):
    """Get a list of softwares associated with a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/softwares'.format(network_id, sm_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_network_adapters_by_sm_id(network_id, sm_id):
    """List the network adapters of a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/networkAdapters'.format(
            network_id, sm_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_wlan_lists_by_sm_id(network_id, sm_id):
    """List the saved SSID names on a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/wlanLists'.format(network_id, sm_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_security_centers_by_sm_id(network_id, sm_id):
    """List the security centers on a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/securityCenters'.format(
            network_id, sm_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_restrictions_by_sm_id(network_id, sm_id):
    """List the restrictions on a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/restrictions'.format(network_id, sm_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_certs_by_sm_id(network_id, sm_id):
    """List the certs on a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/certs'.format(network_id, sm_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_sm_device_tag_by_network_id(network_id, params=''):
    """Add, delete, or update the tags of a set of devices

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - wifiMacs: The wifiMacs of the devices to be modified.
        - ids: The ids of the devices to be modified.
        - serials: The serials of the devices to be modified.
        - scope: The scope (one of all, none, withAny, withAll,
           withoutAny, or withoutAll) and a set of tags of the devices
           to be modified.
        - tags: The tags to be added, deleted, or updated.
        - updateAction: One of add, delete, or update. Only devices
           that have been modified will be returned.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/devices/tags'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_sm_device_field_by_network_id(network_id, params=''):
    """Modify the fields of a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - wifiMac: The wifiMac of the device to be modified.
        - id: The id of the device to be modified.
        - serial: The serial of the device to be modified.
        - deviceFields: The new fields of the device. Passed in as a
           JSON object. The list of available fields are: name, notes

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/device/fields'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_sm_device_lock_by_network_id(network_id, params=''):
    """Lock a set of devices

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - wifiMacs: The wifiMacs of the devices to be locked.
        - ids: The ids of the devices to be locked.
        - serials: The serials of the devices to be locked.
        - scope: The scope (one of all, none, withAny, withAll,
           withoutAny, or withoutAll) and a set of tags of the devices
           to be wiped.
        - pin: The pin number for locking macOS devices (a six digit
           number). Required only for macOS devices.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/devices/lock'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_sm_device_wipe_by_network_id(network_id, params=''):
    """Wipe a device

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - wifiMac: The wifiMac of the device to be wiped.
        - id: The id of the device to be wiped.
        - serial: The serial of the device to be wiped.
        - pin: The pin number (a six digit value) for wiping a macOS
           device. Required only for macOS devices.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/device/wipe'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_sm_device_checkin_by_network_id(network_id, params=''):
    """Force check-in a set of devices

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - wifiMacs: The wifiMacs of the devices to be checked-in.
        - ids: The ids of the devices to be checked-in.
        - serials: The serials of the devices to be checked-in.
        - scope: The scope (one of all, none, withAny, withAll,
           withoutAny, or withoutAll) and a set of tags of the devices
           to be checked-in.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/devices/checkin'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def update_sm_device_move_by_network_id(network_id, params=''):
    """Move a set of devices to a new network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - wifiMacs: The wifiMacs of the devices to be moved.
        - ids: The ids of the devices to be moved.
        - serials: The serials of the devices to be moved.
        - scope: The scope (one of all, none, withAny, withAll,
           withoutAny, or withoutAll) and a set of tags of the devices
           to be moved.
        - newNetwork: The new network to which the devices will be
           moved.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/sm/devices/move'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_sm_profiles_by_network_id(network_id):
    """List all the profiles in the network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/profiles'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_cellular_usage_history_by_sm_id(network_id, sm_id):
    """Return the client's daily cellular data usage history. Usage data is in
       kilobytes.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/cellularUsageHistory'.format(
            network_id, sm_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_performance_history_by_sm_id(network_id, sm_id, params=''):
    """Return historical records of various Systems Manager client metrics for
       desktop devices.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - perPage: The number of entries per page returned
        - startingAfter: A token used by the server to indicate the
           start of the page. Often this is a timestamp or an ID but it
           is not limited to those. This parameter should not be defined
           by client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.
        - endingBefore: A token used by the server to indicate the end
           of the page. Often this is a timestamp or an ID but it is not
           limited to those. This parameter should not be defined by
           client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/performanceHistory{}'.format(
            network_id, sm_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_desktop_logs_by_sm_id(network_id, sm_id, params=''):
    """Return historical records of various Systems Manager network connection
       details for desktop devices.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - perPage: The number of entries per page returned
        - startingAfter: A token used by the server to indicate the
           start of the page. Often this is a timestamp or an ID but it
           is not limited to those. This parameter should not be defined
           by client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.
        - endingBefore: A token used by the server to indicate the end
           of the page. Often this is a timestamp or an ID but it is not
           limited to those. This parameter should not be defined by
           client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/desktopLogs{}'.format(
            network_id, sm_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_device_command_logs_by_sm_id(network_id, sm_id, params=''):
    """    Return historical records of commands sent to Systems Manager
       devices.     <p>Note that this will include the name of the
       Dashboard user who initiated the command if it was generated
       by a Dashboard admin rather than the automatic behavior of the
       system; you may wish to filter this out     of any reports.</p>

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - perPage: The number of entries per page returned
        - startingAfter: A token used by the server to indicate the
           start of the page. Often this is a timestamp or an ID but it
           is not limited to those. This parameter should not be defined
           by client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.
        - endingBefore: A token used by the server to indicate the end
           of the page. Often this is a timestamp or an ID but it is not
           limited to those. This parameter should not be defined by
           client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/deviceCommandLogs{}'.format(
            network_id, sm_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_connectivity_by_sm_id(network_id, sm_id, params=''):
    """Returns historical connectivity data (whether a device is regularly
       checking in to Dashboard).

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sm_id: ???
            ↳ ???
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - perPage: The number of entries per page returned
        - startingAfter: A token used by the server to indicate the
           start of the page. Often this is a timestamp or an ID but it
           is not limited to those. This parameter should not be defined
           by client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.
        - endingBefore: A token used by the server to indicate the end
           of the page. Often this is a timestamp or an ID but it is not
           limited to those. This parameter should not be defined by
           client applications. The link for the first, last, next or
           prev page in the HTTP Link header should define it.

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/sm/{}/connectivity{}'.format(
            network_id, sm_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_splash_login_attempts_by_network_id(network_id, params=''):
    """List the splash login attempts for a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - ssidNumber: Only return the login attempts for the specified
           SSID
        - loginIdentifier: The username, email, or phone number used
           during login
        - timespan: The timespan, in seconds, for the login attempts.
           The period will be from [timespan] seconds ago until now. The
           maximum timespan is 3 months

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/splashLoginAttempts{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_splash_settings_by_ssid_number(network_id, ssid_number):
    """Display the splash page settings for the given SSID

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @ssid_number: Positional number of the SSID in the list (0-14)
            ↳ get_ssids_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/ssids/{}/splashSettings'.format(
            network_id, ssid_number),
        headers=HEADERS)
    return graceful_exit(response)


def update_splash_settings_by_ssid_number(network_id, ssid_number, params=''):
    """Modify the splash page settings for the given SSID

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @ssid_number: Positional number of the SSID in the list (0-14)
            ↳ get_ssids_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - splashUrl: The custom splash URL of the click-through splash
           page. Optional. Note that the URL can be configured without
           necessarily being used. In order to enable the custom URL,
           see 'useSplashUrl'
        - useSplashUrl: Boolean indicating whether the user will be
           redirected to the custom splash url. A custom splash URL must
           be set if this is true. Optional. Note that depending on your
           SSID's access control settings, it may not be possible to use
           the custom splash URL.

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/ssids/{}/splashSettings'.format(
            network_id, ssid_number),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_ssids_by_network_id(network_id):
    """List the SSIDs in a network. Supports networks with access points or
       wireless-enabled security appliances and teleworker gateways.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/ssids'.format(network_id), headers=HEADERS)
    return graceful_exit(response)


def get_ssids_by_ssid_number(network_id, ssid_number):
    """Return a single SSID

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @ssid_number: Positional number of the SSID in the list (0-14)
            ↳ get_ssids_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/ssids/{}'.format(network_id, ssid_number),
        headers=HEADERS)
    return graceful_exit(response)


def update_ssid_by_ssid_number(network_id, ssid_number, params=''):
    """Update the attributes of an SSID

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @ssid_number: Positional number of the SSID in the list (0-14)
            ↳ get_ssids_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of an SSID
        - enabled: Whether or not an SSID is enabled
        - authMode: The association control method for the SSID
           ('open', 'psk', 'open-with-radius', '8021x-meraki',
           '8021x-radius')
        - encryptionMode: The psk encryption mode for the SSID ('wpa',
           'wep', 'wpa-eap')
        - psk: The passkey for the SSID. This param is only valid if
           the authMode is 'psk'
        - wpaEncryptionMode: The types of WPA encryption. ('WPA1 and
           WPA2', 'WPA2 only')
        - splashPage: The type of splash page for the SSID ('None',
           'Click-through splash page', 'Billing', 'Password-protected
           with Meraki RADIUS', 'Password-protected with custom RADIUS',
           'Password-protected with Active Directory', 'Password-
           protected with LDAP', 'SMS authentication', 'Systems Manager
           Sentry', 'Facebook Wi-Fi', 'Google OAuth', 'Sponsored
           guest'). This attribute is not supported for template
           children.
        - radiusServers: The RADIUS 802.1x servers to be used for
           authentication. This param is only valid if the authMode is
           'open-with-radius' or '8021x-radius'
        - radiusCoaEnabled: If true, Meraki devices will act as a
           RADIUS Dynamic Authorization Server and will respond to
           RADIUS Change-of-Authorization and Disconnect messages sent
           by the RADIUS server.
        - radiusFailoverPolicy: This policy determines how
           authentication requests should be handled in the event that
           all of the configured RADIUS servers are unreachable ('Deny
           access', 'Allow access')
        - radiusLoadBalancingPolicy: This policy determines which
           RADIUS server will be contacted first in an authentication
           attempt and the ordering of any necessary retry attempts
           ('Strict priority order', 'Round robin')
        - radiusAccountingEnabled: Whether or not RADIUS accounting is
           enabled. This param is only valid if the authMode is 'open-
           with-radius' or '8021x-radius'
        - radiusAccountingServers: The RADIUS accounting 802.1x servers
           to be used for authentication. This param is only valid if
           the authMode is 'open-with-radius' or '8021x-radius' and
           radiusAccountingEnabled is 'true'
        - ipAssignmentMode: The client IP assignment mode ('NAT mode',
           'Bridge mode', 'Layer 3 roaming', 'Layer 3 roaming with a
           concentrator', 'VPN')
        - useVlanTagging: Direct trafic to use specific VLANs. This
           param is only valid with 'Bridge mode' and 'Layer 3 roaming'
        - concentratorNetworkId: The concentrator to use for 'Layer 3
           roaming with a concentrator' or 'VPN'.
        - vlanId: The VLAN ID used for VLAN tagging. This param is only
           valid with 'Layer 3 roaming with a concentrator' and 'VPN'
        - defaultVlanId: The default VLAN ID used for 'all other APs'.
           This param is only valid with 'Bridge mode' and 'Layer 3
           roaming'
        - apTagsAndVlanIds: The list of tags and VLAN IDs used for VLAN
           tagging. This param is only valid with 'Bridge mode', 'Layer
           3 roaming'
        - walledGardenEnabled: Allow access to a configurable list of
           IP ranges, which users may access prior to sign-on.
        - walledGardenRanges: Specify your walled garden by entering
           space-separated addresses, ranges using CIDR notation, domain
           names, and domain wildcards (e.g. 192.168.1.1/24
           192.168.37.10/32 www.yahoo.com *.google.com). Meraki's splash
           page is automatically included in your walled garden.
        - minBitrate: The minimum bitrate in Mbps. (1, 2, 5.5, 6, 9,
           11, 12, 18, 24, 36, 48, 54)
        - bandSelection: The client-serving radio frequencies. (Dual
           band operation, 5 GHz band only, Dual band operation with
           Band Steering)
        - perClientBandwidthLimitUp: The upload bandwidth limit in
           Kbps. (0 represents no limit.)
        - perClientBandwidthLimitDown: The download bandwidth limit in
           Kbps. (0 represents no limit.)

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/ssids/{}'.format(network_id, ssid_number),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_switch_settings_by_network_id(network_id):
    """Returns the switch network settings

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/switch/settings'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_switch_settings_by_network_id(network_id, params=''):
    """Update switch network settings

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - useCombinedPower: The behavior of secondary power supplies on
           supported devices ("redundant", "combined")
        - powerExceptions: Exceptions on a per switch basis to
           "useCombinedPower"

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/switch/settings'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_switch_ports_by_device_serial(serial):
    """List the switch ports for a switch

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/devices/{}/switchPorts'.format(serial), headers=HEADERS)
    return graceful_exit(response)


def get_switch_ports_by_switch_port_number(serial, switch_port_number):
    """Return a switch port

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @switch_port_number: like (1-48)
            ↳ get_switch_ports_by_serial(serial)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/devices/{}/switchPorts/{}'.format(serial,
                                                       switch_port_number),
        headers=HEADERS)
    return graceful_exit(response)


def update_switch_port_by_switch_port_number(serial,
                                             switch_port_number,
                                             params=''):
    """Update a switch port

    Args:
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @switch_port_number: like (1-48)
            ↳ get_switch_ports_by_serial(serial)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the switch port
        - tags: The tags of the switch port
        - enabled: The status of the switch port
        - type: The type of the switch port ("access" or "trunk")
        - vlan: The VLAN of the switch port
        - voiceVlan: The voice VLAN of the switch port. Only applicable
           to access ports.
        - allowedVlans: The VLANs allowed on the switch port. Only
           applicable to trunk ports.
        - poeEnabled: The PoE status of the switch port
        - isolationEnabled: The isolation status of the switch port
        - rstpEnabled: The rapid spanning tree protocol status
        - stpGuard: The state of the STP guard ("disabled", "Root
           guard", "BPDU guard", "Loop guard")
        - accessPolicyNumber: The number of the access policy of the
           switch port. Only applicable to access ports.
        - linkNegotiation: The link speed for the switch port

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/devices/{}/switchPorts/{}'.format(serial,
                                                       switch_port_number),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_syslog_servers_by_network_id(network_id):
    """List the syslog servers for a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/syslogServers'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_syslog_server_by_network_id(network_id, params=''):
    """Update the syslog servers for a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - servers: A list of the syslog servers for this network

    Returns: (list)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/syslogServers'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_content_filtering_categories_by_network_id(network_id):
    """List all available content filtering categories for an MX network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL +
        '/networks/{}/contentFiltering/categories'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_content_filtering_by_network_id(network_id):
    """Return the content filtering settings for an MX network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/contentFiltering'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_content_filtering_by_network_id(network_id, params=''):
    """Update the content filtering settings for an MX network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - allowedUrlPatterns: A whitelist of URL patterns to allow
        - blockedUrlPatterns: A blacklist of URL patterns to block
        - blockedUrlCategories: A list of URL categories to block
        - urlCategoryListSize: URL category list size which is either
           'topSites' or 'fullList'

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/contentFiltering'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_firewalled_services_by_network_id(network_id):
    """List the appliance services and their accessibility rules

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/firewalledServices'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_firewalled_services_by_firewalled_service_type(network_id, service):
    """Return the accessibility settings of the given service ('ICMP', 'web',
       or 'SNMP')

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @service: MX Services (eg 'web')
            ↳ get_firewalled_services_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/firewalledServices/{}'.format(
            network_id, service),
        headers=HEADERS)
    return graceful_exit(response)


def update_firewalled_service_by_firewalled_service_type(
        network_id, service, params=''):
    """Updates the accessibility settings for the given service ('ICMP', 'web',
       or 'SNMP')

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @service: MX Services (eg 'web')
            ↳ get_firewalled_services_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - access: A string indicating the rule for which IPs are
           allowed to use the specified service. Acceptable values are
           "blocked" (no remote IPs can access the service),
           "restricted" (only whitelisted IPs can access the service),
           and "unrestriced" (any remote IP can access the service).
           This field is required
        - allowedIps: An array of whitelisted IPs that can access the
           service. This field is required if "access" is set to
           "restricted". Otherwise this field is ignored

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/firewalledServices/{}'.format(
            network_id, service),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_static_routes_by_network_id(network_id):
    """List the static routes for this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/staticRoutes'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_static_routes_by_static_route_id(network_id, sr_id):
    """Return a static route

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sr_id: Static route ID like d7fa4948-7921-4dfa-af6b-ae8b16c20c39
            ↳ get_static_routes_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/staticRoutes/{}'.format(network_id, sr_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_static_route_by_static_route_id(network_id, sr_id, params=''):
    """Update a static route

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sr_id: Static route ID like d7fa4948-7921-4dfa-af6b-ae8b16c20c39
            ↳ get_static_routes_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the static route
        - subnet: The subnet of the static route
        - gatewayIp: The gateway IP (next hop) of the static route
        - enabled: The enabled state of the static route
        - fixedIpAssignments: The DHCP fixed IP assignments on the
           static route
        - reservedIpRanges: The DHCP reserved IP ranges on the static
           route

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/staticRoutes/{}'.format(network_id, sr_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_static_route_by_network_id(network_id, params=''):
    """Add a static route

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the new static route
        - subnet: The subnet of the static route
        - gatewayIp: The gateway IP (next hop) of the static route

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/staticRoutes'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_static_route_by_static_route_id(network_id, sr_id):
    """Delete a static route from a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @sr_id: Static route ID like d7fa4948-7921-4dfa-af6b-ae8b16c20c39
            ↳ get_static_routes_by_network_id(network_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/staticRoutes/{}'.format(network_id, sr_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_uplink_settings_by_network_id(network_id):
    """Returns the uplink settings for your MX network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/uplinkSettings'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_uplink_settings_by_network_id(network_id, params=''):
    """Updates the uplink settings for your MX network.

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - bandwidthLimits: A mapping of uplinks (wan1, wan2, and
           cellular) to their bandwidth settings (be sure to check which
           uplinks are supported for your network). Bandwidth setting
           objects have the following structure

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/network/{}/uplinkSettings'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_vlans_by_network_id(network_id):
    """List the VLANs for this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (list)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/vlans'.format(network_id), headers=HEADERS)
    return graceful_exit(response)


def get_vlans_by_vlan_id(network_id, vlan_id):
    """Return a VLAN

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @vlan_id: VLAN number (eg 1234)
            ↳ get_vlans_by_network_id(network_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/vlans/{}'.format(network_id, vlan_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_vlan_by_vlan_id(network_id, vlan_id, params=''):
    """Update a VLAN

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @vlan_id: VLAN number (eg 1234)
            ↳ get_vlans_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - name: The name of the VLAN
        - subnet: The subnet of the VLAN
        - applianceIp: The local IP of the appliance on the VLAN
        - fixedIpAssignments: The DHCP fixed IP assignments on the VLAN
        - reservedIpRanges: The DHCP reserved IP ranges on the VLAN
        - vpnNatSubnet: The translated VPN subnet if VPN and VPN subnet
           translation are enabled on the VLAN
        - dnsNameservers: The DNS nameservers used for DHCP responses,
           either "upstream_dns", "google_dns", "opendns", or a newline
           seperated string of IP addresses or domain names

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/vlans/{}'.format(network_id, vlan_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def create_vlan_by_network_id(network_id, params=''):
    """Add a VLAN

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - id: The VLAN ID of the new VLAN (must be between 1 and 4094)
        - name: The name of the new VLAN
        - subnet: The subnet of the VLAN
        - applianceIp: The local IP of the appliance on the VLAN

    Returns: (dict)

    """
    response = requests.post(
        BASE_URL + '/networks/{}/vlans'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def delete_vlan_by_vlan_id(network_id, vlan_id):
    """Delete a VLAN from a network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @vlan_id: VLAN number (eg 1234)
            ↳ get_vlans_by_network_id(network_id)

    Returns: (None)

    """
    response = requests.delete(
        BASE_URL + '/networks/{}/vlans/{}'.format(network_id, vlan_id),
        headers=HEADERS)
    return graceful_exit(response)


def get_vlans_enabled_state_by_network_id(network_id):
    """Returns the enabled status of VLANs for the network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)

    Returns: (dict)

    """
    response = requests.get(
        BASE_URL + '/networks/{}/vlansEnabledState'.format(network_id),
        headers=HEADERS)
    return graceful_exit(response)


def update_vlans_enabled_state_by_network_id(network_id, params=''):
    """Enable/Disable VLANs for the given network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - enabled: Boolean indicating whether to enable (true) or
           disable (false) VLANs for the network

    Returns: (dict)

    """
    response = requests.put(
        BASE_URL + '/networks/{}/vlansEnabledState'.format(network_id),
        data=json.dumps(params),
        headers=HEADERS)
    return graceful_exit(response)


def get_connection_stats_by_network_id(network_id, params=''):
    """Aggregated connectivity info for this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/connectionStats{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_devices_connection_stats_by_network_id(network_id, params=''):
    """Aggregated connectivity info for this network, grouped by node

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/devices/connectionStats{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_connection_stats_by_device_serial(network_id, serial, params=''):
    """Aggregated connectivity info for a given AP on this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/devices/{}/connectionStats{}'.format(
            network_id, serial, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_clients_connection_stats_by_network_id(network_id, params=''):
    """Aggregated connectivity info for this network, grouped by clients

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/connectionStats{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_connection_stats_by_client_id(network_id, client_id, params=''):
    """Aggregated connectivity info for a given client on this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @client_id: Client ID Hash (eg k74272e)
            ↳ get_clients_by_serial(serial)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/connectionStats{}'.format(
            network_id, client_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_latency_stats_by_network_id(network_id, params=''):
    """Aggregated latency info for this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN
        - fields: Partial selection: If present, this call will return
           only the selected fields of ["rawDistribution", "avg"]. All
           fields will be returned by default. Selected fields must be
           entered as a comma separated string.

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/latencyStats{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_devices_latency_stats_by_network_id(network_id, params=''):
    """Aggregated latency info for this network, grouped by node

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN
        - fields: Partial selection: If present, this call will return
           only the selected fields of ["rawDistribution", "avg"]. All
           fields will be returned by default. Selected fields must be
           entered as a comma separated string.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/devices/latencyStats{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_latency_stats_by_device_serial(network_id, serial, params=''):
    """Aggregated latency info for a given AP on this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @serial: Serial# of a device (eg Q234-ABCD-5678)
            ↳ get_devices_by_network_id(network_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN
        - fields: Partial selection: If present, this call will return
           only the selected fields of ["rawDistribution", "avg"]. All
           fields will be returned by default. Selected fields must be
           entered as a comma separated string.

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/devices/{}/latencyStats{}'.format(
            network_id, serial, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_clients_latency_stats_by_network_id(network_id, params=''):
    """Aggregated latency info for this network, grouped by clients

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN
        - fields: Partial selection: If present, this call will return
           only the selected fields of ["rawDistribution", "avg"]. All
           fields will be returned by default. Selected fields must be
           entered as a comma separated string.

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/latencyStats{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_latency_stats_by_client_id(network_id, client_id, params=''):
    """Aggregated latency info for a given client on this network

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @client_id: Client ID Hash (eg k74272e)
            ↳ get_clients_by_serial(serial)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN
        - fields: Partial selection: If present, this call will return
           only the selected fields of ["rawDistribution", "avg"]. All
           fields will be returned by default. Selected fields must be
           entered as a comma separated string.

    Returns: (dict)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/clients/{}/latencyStats{}'.format(
            network_id, client_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)


def get_failed_connections_by_network_id(network_id, params=''):
    """List of all failed client connection events on this network in a given
       time range

    Args:
        @network_id: (eg N_24329156)
            ↳ get_networks_by_org_id(org_id)
        @params: Dict/JSON of options like
            {"key": val, "array": [{"key": val}, ...], ...}.

    Params: (dict)
        - t0: Start of the requested time range in seconds since epoch
           (Required)
        - t1: End of the requested time range in seconds since epoch
           (Required)
        - ssid: Filter results by SSID
        - vlan: Filter results by VLAN
        - serial: Filter by AP
        - clientId: Filter by client

    Returns: (list)

    """
    # urlencode gives us & when query needs ?
    url_query = urllib.parse.urlencode(params)
    url_query = '?' + url_query.replace('&', '?')
    response = requests.get(
        BASE_URL + '/networks/{}/failedConnections{}'.format(
            network_id, params, url_query),
        headers=HEADERS)
    return graceful_exit(response)
