# Bugs I've noticed with the API
## POST /networks/[networkId]/devices/[serial]/remove
* This is removing a device, so it should be a DELETE, not a POST. This is what it should look like instead:
  
  `DELETE /networks/[networkId]/devices/[serial]`
* This is returning a 204 error code, but the sample resp returns a JSON. Per the docs, code 204 should *should return no content*.

## POST /organizations/[organizationId]/networks
* Passing {"name": "some name"} without a type results in a 500 error. It should return an errors key in the response json explaining that "type" is required.