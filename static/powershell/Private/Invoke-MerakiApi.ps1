# Funtion that interacts with the Meraki API
function Invoke-ApiCall ([string]$httpMethod, [string]$endpointUrl, [string]$params) {
    # Gather/Format API call inputs for Send Request and then call
    # Using Invoke-WebRequest over Invoke-RestMethod because the former has more
    # metadata like StatusCodes.
    [string] $apiKey = "{}"
    [hashtable] $headers = @{ 'X-Cisco-Meraki-API-Key' = $apiKey }
    Print("`nCalling $($httpMethod) on $($endpointUrl) with [$($params)] params.")
    $url = "https://api.meraki.com/api/v0$($endpointUrl)"
    $RespErr = ''

    try {
        if ($params) {
            $result = Invoke-WebRequest -Uri $url -Headers $headers -Body $params `
                            -method $httpMethod -ContentType 'Application/Json' -ErrorVariable RespErr
        }
        else
        {
            $result = Invoke-WebRequest -Uri $url -Headers $headers `
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
        Print("Status code: $($statusCode); Data: $($data)")
        return $data
    }
}