# Toy ruby script to demonstrate GET POST PUT DELETE admins using net/http
require 'net/http'
require 'uri'
require 'json'

json_file = File.read('../_vars.json')
json_vars = JSON.parse(json_file)
$api_key = json_vars["API_KEY"]
$org_id = json_vars["ORG_ID"]
$new_admin = json_vars["NEW_ADMIN"]

$base_url = 'https://api.meraki.com/api/v0'


# From Ruby docs. One redirect is expected: a second is not.
def api_call(http_method, site, options, limit = 2)
  raise ArgumentError, 'too many HTTP redirects' if limit.zero?

  uri = URI.parse(site)
  puts site
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true

  case http_method
  when 'GET' then
    request = Net::HTTP::Get.new(uri.request_uri)
  when 'POST' then
    request = Net::HTTP::Post.new(uri.request_uri)
    request.body = options.to_json
  when 'PUT' then
    request = Net::HTTP::Put.new(uri.request_uri)
    request.body = options.to_json
  when 'DELETE' then
    request = Net::HTTP::Delete.new(uri.request_uri)
  else
    raise ArgumentError, 'Invalid HTTP method'
  end
  request['Content-Type'] = 'application/json'
  request['X-Cisco-Meraki-Api-Key'] = $api_key
  request['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
  response = http.request(request)

  case response
  when Net::HTTPSuccess then
    return response.body
  when Net::HTTPRedirection then
    return api_call(http_method, response['location'], options, limit - 1)
  else
    return response.value
  end
end

def orgs
  query = '/organizations'
  fetch('GET', "#{$base_url}#{query}", [])
end

def admins
  query = "/organizations/#{$org_id}/admins"
  api_call('GET', "#{$base_url}#{query}", [])
end

def create_admin
  query = "/organizations/#{$org_id}/admins"
  options = $new_admin
  api_call('POST', "#{$base_url}#{query}", options)
end

def update_admin(id)
  query = "/organizations/#{org_id}/admins/#{id}"
  options = { "tags": [{ "tag": 'east', "access": 'read-only' }] }
  api_call('PUT', "#{$base_url}#{query}", options)
end

def delete_admin(id)
  query = "/organizations/#{$org_id}/admins/#{$id}"
  api_call('DELETE', "#{$base_url}#{query}", [])
end
