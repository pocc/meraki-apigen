# Any combination of positional (max 2) and piped (n) variables will be summed if variable count > 2
function Add {
[cmdletbinding()]
param(
    # Positional variables
    [parameter(Position=0)]
    [int[]]
    $addend,
    [parameter(Position=1)]
    [int]
    $addend2,

    # Piped variables
    [parameter(ValueFromPipelineByPropertyName, ValueFromPipeline)]
    [int[]]$InputList
)
    Begin {    $sum = 0
}
    Process {
    if ($addend1) {$InputList += $addend1}
    if ($addend2) {$InputList += $addend2}
    if ($InputList.length -lt 2) {
        Write-Error "Not enough numbers as piped input or params"
    }

    foreach ($int in $InputList) {
        $sum += $int
    }
    }
    End {
    # Write-Information -InformationAction Continue "Sum is $sum"
    return $sum
}

}

function testAdd() {
    # 1 + 2 + 3 = 6
    $result = 1,2,3 | Add
    if ($result -ne 6) {
        Write-Information -InformationAction Continue "1,2,3 | Add does not equal 6!"
    }

    # String is not valid pipeline input
    $result = $(1, 2, 'aoeu' | Add) 2>&1
    $expectedError = "The input object cannot be bound to any parameters for the command*"
    if (-Not ($result -like $expectedError)) {
        Write-Information -InformationAction Continue "Error! String should not be valid pipeline input!"
    }

    # 1 + 2 = 3
    $result = Add 1 2
    if ($result -ne 3) {
        Write-Information -InformationAction Continue "Error! Add 1 2 does not produce 3"
    }
    
    # String is not valid param input
    $expectedError = "Add : Cannot process argument transformation on parameter 'addend2'. Cannot convert value*"
    try {
        $result = Add 1 'aoeu' 2>&1
        Write-Information -InformationAction Continue "Error! Input cannot be string!"
    }
    catch {}

    # Only 2 valid inputs
    try {
        $result = Add 1 2 3
        Write-Information -InformationAction Continue "Error! Too many inputs (3) does not cause error!"
    }
    catch {}

    # 1 input should error
    $expectedError = "Add : ERROR! Pipeline vals or 2 inputs are required, 1 provided.*"
    try {
        $result = Add 1 -ErrorAction "SilentlyContinue"
        Write-Information -InformationAction Continue "Error! Too few inputs (1) does not cause break!"
    }
    catch {}
}

# To test, uncomment the following line:
# testAdd