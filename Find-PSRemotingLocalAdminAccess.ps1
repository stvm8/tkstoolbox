﻿function Find-PSRemotingLocalAdminAccess {
<#
.EXAMPLE
Find-PSRemotingLocalAdminAccess -ComputerName "Computer1", "Computer2" -Domain "example.com" -StopOnSuccess -Verbose

.LINK
https://github.com/samratashok/nishang
http://www.labofapenetrationtester.com/
#>

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory = $false, Position = 0, ValueFromPipeline = $true)]
        [String[]]
        $ComputerName,

        [Parameter(Mandatory = $false, Position = 1, ValueFromPipeline = $true)]
        [String]
        $ComputerFile,

        [Parameter(Mandatory = $false)]
        [String]
        $Domain,

        [Parameter()]
        [Switch]
        $StopOnSuccess
    )

    $ErrorActionPreference = "SilentlyContinue"

    # Read word list (consider pipeline for performance)
    if ($ComputerFile) {
        $Computers = Get-Content $ComputerFile
    }
    elseif ($ComputerName) {
        $Computers = $ComputerName
    }
    else {
        # Get a list of all the computers in the domain
        $objSearcher = New-Object System.DirectoryServices.DirectorySearcher

        if ($Domain) {
            $objSearcher.SearchRoot = New-Object System.DirectoryServices.DirectoryEntry("LDAP://$Domain")
        }
        else {
            $objSearcher.SearchRoot = New-Object System.DirectoryServices.DirectoryEntry
        }

        $objSearcher.Filter = "(&(sAMAccountType=805306369))"
        $Computers = $objSearcher.FindAll() | ForEach-Object { $_.properties.dnshostname }
    }

    # Clear error listing
    $Error.Clear()

    # Run the test
    Write-Verbose 'Trying to run a command parallely on the provided computers list using PSRemoting.'
    Invoke-Command -ScriptBlock { hostname } -ComputerName $Computers -ErrorAction SilentlyContinue

    # Put the first error into a variable (best practice)
    $ourError = $Error[0]

    # If there is no error, then we were successful; otherwise, check the error message
    if ($ourError -eq $null) {
        "The current user has Local Admin access on: $Computer"
        if ($StopOnSuccess) {
            break
        }
    }
    elseif (-not $ourError.Exception.Message.Contains("Access is denied.")) {
        Write-Warning "Something went wrong. Check the settings, confirm hostname, etc. $($ourError.Exception.Message)"
    }
    else {
        Write-Debug "$($ourError.Exception.Message)"
    }
}