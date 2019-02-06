# Utility functions.

<# NOTE: Powershell is notorious, especially prior to 5.0, for having unreliable console writing behavior.
# i.e. write-host $text, out-host $text, write-output $text, or just putting "$text" on a line.
# Most of these will add the text to the return value of the function.
#>
function Print([String]$text) {
    # Print function substitution added for readability and reliability.
    Write-Information -InformationAction Continue $text
}

function JsonToHashtable([String]$json) {
    # Convert Json to Hashtable (courtesy https://stackoverflow.com/questions/40495248)
    $hashtable = @{}
    (ConvertFrom-Json $json).psobject.properties | Foreach-Object { $hashtable[$_.Name] = $_.Value }
    return $hashtable
}

function ParseParams([Hashtable]$params) {
    # Convert JSON to string in form of ?key=value&key=value&key=value...
    $url = ''
    Foreach ($key in $params.keys) {
        $url += "&$key=$( $params[$key] )"
    }
    return '?' + $url[1..$url.Length]
}