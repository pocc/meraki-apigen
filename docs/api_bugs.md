# Bugs I've noticed with the v0 API
## General
### Resource already exists
* 409 (Conflict) if resource already exists should be used. For example, 
  if you are trying to create an admin and a user with that email is already 
  an admin in that org. Instead, 200 is used with errortext.

## Per API Call
### POST /networks/[networkId]/devices/[serial]/remove
* This is removing a device, so it should be a DELETE, not a POST. 
  This is what it should look like instead:
  
  `DELETE /networks/[networkId]/devices/[serial]`
  
* This is returning a 204 error code, but the sample resp returns a JSON. 
  Per the docs, code 204 should *should return no content*.

### POST /organizations/[organizationId]/networks
* Passing {"name": "some name"} without a type results in a 500 error. 
  It should return an errors key in the response json explaining that 
  "type" is required.
  
### GET/PUT/DELETE /networks/[networkId]/sm/targetGroups/[targetGroupId]
None of the GET Sample Resps have an ID that is returned that can be used to 
interact with this API endpoint.
