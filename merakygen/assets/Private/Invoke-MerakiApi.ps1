function Invoke-ApiCall ([string]$httpMethod, [string]$endpointUrl, [string]$params) {
    # Gather/Format API call inputs for Send Request and then call
    # Using Invoke-WebRequest over Invoke-RestMethod because the former has more
    # metadata like StatusCodes.
    [string] $apiKey = "{}"
    [hashtable] $headers = @{ 'X-Cisco-Meraki-API-Key' = $this.apiKey }
    $this.utils.print("`nCalling $($httpMethod) on $($endpointUrl) with [$($params)] params.")
    $url = "https://api.meraki.com/api/v0$($endpointUrl)"
    $RespErr = ''

    try {
        if ($params) {
            $result = Invoke-WebRequest -Uri $url -Headers $this.headers -Body $params `
                            -method $httpMethod -ContentType 'Application/Json' -ErrorVariable RespErr
        }
        else
        {
            $result = Invoke-WebRequest -Uri $url -Headers $this.headers `
                            -method $httpMethod -ContentType 'Application/Json' -ErrorVariable RespErr
        }
        # Keeping for troubleshooting purposes
        $statusCode = $result.StatusCode

        # Get data and remove trailing whitespace
        $data = $result.Content -replace "[\s]*$",""
        return $data
    }
    catch {
        $data = $RespErr
        $statusCode = $_.Exception.Response.StatusCode.Value__
        $this.utils.print("Status code: $($statusCode); Data: $($data)")
        return $data
    }
}