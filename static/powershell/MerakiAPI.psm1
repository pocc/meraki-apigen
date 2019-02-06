# Entrypoint for module Merakygen
$Cwd = (Get-Location).ToString()
$FunctionList = Get-ChildItem -Recurse "$Cwd/Classes","$Cwd/Functions"
# Added for readability and to get a consistent print function.
function print([string]$text) { return Write-Information -InformationAction Continue $text }

foreach ($File in $FunctionList) {
    try {
        . $File.FullName
        print("Imported file: $($File.FullName)")
    }
    catch {
        print("FAILED to import file: $($File.FullName)")
    }
}
