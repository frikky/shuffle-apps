docker run -it mcr.microsoft.com/powershell:ubuntu-18.04


### https://docs.microsoft.com/en-us/powershell/module/exchange/connect-exchangeonline?view=exchange-ps
Install-Module -Name ExchangeOnlineManagement -Force

Connect-ExchangeOnline -Device

* Go to https://microsoft.com/devicelogin and type in the code they give

Get-QuarantineMessage
Get-QuarantineMessageHeader
Delete-QuarantineMessage
Export-QuarantineMessage
Preview-QuarantineMessage
Release-QuarantineMessage

############### Otherwise:
Install-Module -Name ExchangeOnlineManagement -Force
Connect-ExchangeOnline -InlineCredential

$userCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList "frikky@shufflertest2.onmicrosoft.com", $(ConvertTo-SecureString -String "MyPassword" -AsPlainText -Force)

$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri https://outlook.office365.com/powershell-liveid/ -Authentication Basic -AllowRedirection -Credential $(New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList "frikky@shufflertest2.onmicrosoft.com", $(ConvertTo-SecureString -String "MyPassword" -AsPlainText -Force))

Import-PSSession $Session -AllowClobber


############### USAGE
$msg = Get-QuarantineMessage -StartReceivedDate 06/13/2016 -EndReceivedDate 01/01/2025
$msg[0].MessageID
$msg[0].Identity

Get-QuarantineMessage -MessageID "<5c695d7e-6642-4681-a4b0-9e7a86613cb7@contoso.com>"
Get-QuarantineMessage -Identity $msg.identity

Get-QuarantineMessageHeader $msg.identity
$exported = Export-QuarantineMessage -Identity $msg.identity
$exported.eml



############## EXTRA PSWSMan
Install-Module -Name PSWSMan -Force
Install-WSMan
