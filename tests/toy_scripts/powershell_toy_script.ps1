# -*- coding: utf-8 -*-
# Copyright 2019 Ross Jacobs All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

<# Toy script to test basic API calls in Powershell.
#
# Following PascalCase for function names and camelCase for variables.
#
# https://overpoweredshell.com/Introduction-to-PowerShell-Classes/
# Without classes, methods have varying and unpredictable behavior for text
# output to the console. Powershell classes have much better
# error checking (avoid functions if possible).
#>

Remove-Variable * -ErrorAction SilentlyContinue
$error.Clear()

# Main function
$TestRunner = [TestBasic]::new()
$TestRunner.RunTests()


class ApiCall
{
    [string] $apiKey
    [hashtable] $headers
    [TestUtils] hidden $utils

    # Default constructor: Use a predetermined file.
    ApiCall() {
        $this.utils = [TestUtils]::new()
        $jsonFile = '../_apikey'
        $this.apiKey = Get-Content -Raw -Path $jsonFile
        $this.headers = @{ 'X-Cisco-Meraki-API-Key' = $this.apiKey }
    }

    # Optional method params don't exist so overload functions instead.
    [string] SendRequest([string]$httpMethod, [string]$endpointUrl) {
        $emptyParams = ''
        return $this.SendRequest($httpMethod, $endpointUrl, $emptyParams)}
    [string] SendRequest([string]$httpMethod, [string]$endpointUrl, [string]$params) {
        # Gather/Format API call inputs for Send Request and then call
        # Using Invoke-WebRequest over Invoke-RestMethod because the former has more
        # metadata like StatusCodes.
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
}


class TestBasic
# Test GET orgs, GET POST PUT DELETE admins
# All of these functions return error text (string) if they fail but otherwise return $Null.
{
    [ApiCall] $api
    [TestUtils] hidden $utils
    [HashTable] $testData


    TestBasic() {
        $this.utils = [TestUtils]::new()
        $this.api = [ApiCall]::new()
    }

    [void] GetTestData() {
        # Get the API key from a JSON file
        $rawJson = Get-Content -Raw -Path '../_vars.json'
        $this.testData = $this.utils.JsonToHashtable($rawJson)
    }

    # Methods
    [string] TestGetOrgs([string]$expectedResultStr) {
        # Test expected org JSON against one from API
        [string]$fetchedOrgsStr = $this.api.SendRequest("get", "/organizations")

        [string]$result = ''
        if (Compare-Object $expectedResultStr $fetchedOrgsStr -PassThru){
            $result = "`n`nExpected: $expectedResultStr`n`nActual: $fetchedOrgsStr" }
        return $result
    }

    [string] TestGetAdmins ([string]$orgId, [string]$expectedResultStr) {
        # Test expected admins JSON against one from API
        [string]$fetchedAdminsStr = $this.api.SendRequest("get", "/organizations/$orgId/admins")
        # lastActive for Admins can change, so remove the value so comparison to expected is valid.
        [string]$fetchedAdminsStr = $fetchedAdminsStr -replace '"lastActive": ?[\d]*,','"lastActive":"",'

        [string]$result = ''
        if (Compare-Object $expectedResultStr $fetchedAdminsStr -PassThru){
            $result = "`n`nExpected: $expectedResultStr`n`nActual: $fetchedAdminsStr" }
        return $result
    }

    [string] TestAddDeleteAdmin([string]$orgId, [string]$defaultAdmins,
                                   [string]$newAdminPayload, [string]$expectedNewAdmins) {
        # Create an admin with $newAdmin JSON. Compare new admins data with $expectedNewAdmins JSON.
        [string]$result = ''
        [string]$newAdminJson = $this.api.SendRequest("post", "/organizations/$orgId/admins", $newAdminPayload)
        $newAdminJson -match "`"id`":`"([\d]*)`""
        [string]$newAdminId = $matches[1]  # matches is the variable regex matches are put. [0] is inital string.
        [string]$fetchedNewAdminsJson = $this.api.SendRequest("get", "/organizations/$orgId/admins")
        # lastActive for Admins can change, so remove the value so comparison to expected is valid.
        [string]$fetchedNewAdmins = $fetchedNewAdminsJson -replace '"lastActive": ?[\d]*,','"lastActive":"",'
        # id will be different for new admins so change default value of 'readme' to actual
        [string]$expectedNewAdmins = $expectedNewAdmins -replace '"id":"replaceme"', "`"id`":`"$newAdminId`""
        if (Compare-Object $expectedNewAdmins $fetchedNewAdmins -PassThru){
            $result += "Create Admins `n`nExpected: $expectedNewAdmins`n`nActual: $fetchedNewAdmins" }


        # Delete admin and verify that all admins JSON matches initial JSON. Delete resp should be empty.
        [hashtable]$newAdmin = $this.utils.JsonToHashtable($newAdminJson)
        [string]$newAdminId = $newAdmin.id
        [string]$deleteResp = $this.api.SendRequest("delete", "/organizations/$orgId/admins/$newAdminId")
        if ($deleteResp)
            {$result += "Delete response (unexpected): $deleteResp"}
        [string]$fetchedAdminsJson = $this.api.SendRequest("get", "/organizations/$orgId/admins")
        # lastActive for Admins can change, so remove the value so comparison to expected is valid.
        [string]$fetchedAdmins = $fetchedAdminsJson -replace '"lastActive": ?[\d]*,','"lastActive":"",'
        if (Compare-Object $defaultAdmins  $fetchedAdmins -PassThru) {
            $result += "Delete Admins `n`nExpected: $defaultAdmins`n`nActual: $fetchedAdmins" }
        return $result
    }

    [string] TestUpdateAdmin([string]$orgId, [string]$updatedAdmin, [string]$updatedBack, [string]$adminId) {
        # Update an admin and then update them back. Verify end admins match initial values with no tags.
        [string]$putOptions = '{ "tags": [{ "tag": "east", "access": "read-only" }] }'
        [string]$putBackOptions = '{ "tags": [] }'
        [string]$endpointUrl = "/organizations/$orgId/admins/$adminId"

        $actualUpdatedAdmin = $this.api.SendRequest("put", $endpointUrl, $putOptions)
        $testUpdate = Compare-Object $updatedAdmin $actualUpdatedAdmin -PassThru

        $updatedBackAdminsJson = $this.api.SendRequest("put", $endpointUrl, $putBackOptions)
        $testUpdateBack = Compare-Object $updatedBack $updatedBackAdminsJson -PassThru

        [string]$result = ''
        if ($testUpdate -Or $testUpdateBack){
            $result = "Test failed.`nTest Update: $testUpdate`nTest Update Back: $testUpdateBack" }
        return $result
    }

    # Optional method params don't exist so overload functions instead.
    [void] CompareHashTables($expected, $actual) {
        $emptyParams = ''
        $this.CompareHashTables($expected, $actual, $emptyParams)}
    [void] CompareHashTables($expected, $actual, $history = '') {
        # Recursively compare hash tables.
        $allKeys = $expected.keys + $actual.keys | Select-Object -uniq
        foreach ($key in $allKeys) {
            if (($actual.keys -contains $key) -and ($expected.keys -contains $key)) {
                $history_param = $history + " : hash['$($key)']"
                $this.CompareNonHashTables($expected[$key], $actual[$key], $history_param) }
            elseif ($expected.keys -notcontains $key) {
                $this.utils.print( "$($history) : hash['$($key)'] in Actual but not Expected!") }
            elseif ($actual.keys -notcontains $key) {
                $this.utils.print( "$($history) : hash['$($key)'] in Expected but not Actual!") } } }

    [void] CompareNonHashTables ($expected, $actual, $history = '') {
        # Helper function for Compare-Hashes.
        if ($expected.GetType().Name -eq "HashTable") {
            $this.CompareHashTables($expected, $actual, $history) }
        elseif (($expected.GetType().Name -eq "Object[]") -and ($actual.GetType().Name -eq "Object[]")) {
            $maxLength = $($expected.length, $actual.length | Measure-Object -Max).Maximum
            for ($i = 0; $i -lt $maxLength; $i++) {
                if ($null -eq $expected[$i]) {
                    $this.utils.print( "$($history) : list['$($actual[$i])'] in Actual but not Expected!") }
                elseif ($null -eq $actual[$i]) {
                    $this.utils.print( "$($history) : list['$($expected[$i])'] in Expected but not Actual!") }
                else {
                    $history_param = $history + " : list[$($i)]"
                    $this.CompareNonHashTables($expected[$i], $actual[$i], $history_param) } } }
        else {
            # If type is string
            $different = Compare-Object $expected $actual
            if ($different) {
                $this.utils.print("$($history) : <->")
                $this.utils.print("   -> Expected '$($expected)'")
                $this.utils.print("   -> Actually '$($actual)'") } } }


    # Main function
    [void] RunTests() {
        # If there is output from Compare-Object, that test has failed.
        # Compare-Object in all of these tests will compare 2 Powershell-JSON objects
        $this.GetTestData()
        $orgId = $this.testData.ORG_ID
        # -Compress removes whitespace in JSON string.
        [int]$maxDepthLevel = 100
        $orgList = ConvertTo-Json -Compress -Depth $maxDepthLevel $this.testData.ORG_DATA
        $adminList = ConvertTo-json -Compress -Depth $maxDepthLevel $this.testData.ADMIN_DATA
        $adminUpdated = ConvertTo-json -Compress -Depth $maxDepthLevel $this.testData.ADMIN_UPDATED
        $adminUpdatedBack = ConvertTo-json -Compress -Depth $maxDepthLevel $this.testData.ADMIN_UPDATED_BACK
        $adminId = $this.testData.ADMIN_ID
        $newAdminData = ConvertTo-Json -Compress -Depth $maxDepthLevel $this.testData.NEW_ADMIN
        $newAdminList = ConvertTo-Json -Compress -Depth $maxDepthLevel $this.testData.NEW_ADMIN_DATA

        try {
            $this.utils.print("`n=======`nStarting TestGetOrgs...")
            $results = $this.TestGetOrgs($orgList)
            if ($results) {
                $this.utils.print("`nTestGetOrgs failed with $results")
            }
            else {
                $this.utils.print("`nTestGetOrgs succeeded!")
            }
        } catch {
            $this.utils.print("`nTestGetOrgs errored with $($_.Exception.Message)")
        }
        try {
            $this.utils.print("`n========`nStarting TestGetAdmins...")
            $results = $this.TestGetAdmins($orgId, $adminList)
            if ($results) {
                $this.utils.print("`nTestGetAdmins failed with $results")
            }
            else {
                $this.utils.print("`nTestGetAdmins succeeded!")
            }
        }
        catch {
            $this.utils.print("`nTestGetAdmins errored with $($_.Exception.Message)")
        }
        try {
            $this.utils.print("`n========`nStarting TestAddDeleteAdmins...")
            $results = $this.TestAddDeleteAdmin($orgId, $adminList, $newAdminData, $newAdminList)
            if ($results) {
                $this.utils.print("`nTestAddDeleteAdmin failed with $results")
            }
            else {
                $this.utils.print("`nTestAddDeleteAdmin succeeded!")
            }
        }
        catch {
            $this.utils.print("`nTestAddDeleteAdmin errored with $($_.Exception.Message)")
        }
        try {
            $this.utils.print("`n========`nStarting TestUpdateAdmins...")
            $results = $this.TestUpdateAdmin($orgId, $adminUpdated, $adminUpdatedBack, $adminId)
            if ($results)
            {
                $this.utils.print("`nTestUpdateAdmins failed with $results")
            }
            else
            {
                $this.utils.print("`nTestUpdateAdmins succeeded!")
            }
        }
        catch {
            $this.utils.print("`nTestUpdateAdmins errored with $($_.Exception.Message)")
        }
    }
}


class TestUtils {
    # class scoped utils
    [void] print($text) {
        Write-Information -InformationAction Continue $text
    }
    
    [hashtable] JsonToHashtable([string]$json) {
        # Convert Json to Hashtable (courtesy https://stackoverflow.com/questions/40495248)
        $hashtable = @{}
        (ConvertFrom-Json $json).psobject.properties | Foreach { $hashtable[$_.Name] = $_.Value }
        return $hashtable
    }
}