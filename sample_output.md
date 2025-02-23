# Summary

## Ignored Properties

The following properties were ignored during comparisons:
- name

## Compared Resources

| Resource Type | Name | Total Properties | Correct | Incorrect |
| --- | --- | --- | --- | --- |
| Microsoft.Storage/storageAccounts | [storage001](#microsoftstoragestorageaccounts-storage001) | 25 | 19 | 5 |

## Unmatched Resources in Left Template

| Resource Type | Name |
| --- | --- |
| Microsoft.Storage/storageAccounts/blobServices | storage001/default |
| Microsoft.Storage/storageAccounts/fileServices | storage001/default |
| Microsoft.Storage/storageAccounts/queueServices | storage001/default |
| Microsoft.Storage/storageAccounts/tableServices | storage001/default |
| Microsoft.Storage/storageAccounts/blobServices/containers | storage001/default/images |
| Microsoft.Storage/storageAccounts/blobServices/containers | storage001/default/tf-state |
| Microsoft.Storage/storageAccounts/blobServices/containers | storage001/default/vpnlogs |

## Unmatched Resources in Right Template

| Resource Type | Name |
| --- | --- |
| Microsoft.Storage/storageAccounts/blobServices | storage002/default |
| Microsoft.Storage/storageAccounts/fileServices | storage002/default |
| Microsoft.Storage/storageAccounts/queueServices | storage002/default |
| Microsoft.Storage/storageAccounts/tableServices | storage002/default |
| Microsoft.Storage/storageAccounts/blobServices/containers | storage002/default/images |
| Microsoft.Storage/storageAccounts/blobServices/containers | storage002/default/tf-state |
| Microsoft.Storage/storageAccounts/blobServices/containers | storage002/default/vpnlogs |

---

<a id="microsoftstoragestorageaccounts-storage001"></a>
### Comparison for Resource: Microsoft.Storage/storageAccounts / storage001

| Property Path | Left Value (Line No.) | Right Value (Line No.) | Fail |
| --- | --- | --- | --- |
| apiVersion | 2023-05-01 (9) | 2023-05-01 (9) |  |
| kind | StorageV2 (150) | StorageV2 (16) |  |
| location | uksouth (145) | uksouth (11) |  |
| name | storage001 (10) | storage002 (10) | Ignored |
| properties.accessTier | Hot (181) | Hot (47) |  |
| properties.allowBlobPublicAccess | True (158) | True (24) |  |
| properties.allowCrossTenantReplication | False (156) | True (22) | ✗ |
| properties.allowSharedKeyAccess | False (159) | True (25) | ✗ |
| properties.allowedCopyScope | AAD (153) | AAD (19) |  |
| properties.defaultToOAuthAuthentication | True (154) | False (20) | ✗ |
| properties.dnsEndpointType | Standard (152) | Standard (18) |  |
| properties.encryption.keySource | Microsoft.Storage (179) | Microsoft.Storage (45) |  |
| properties.encryption.requireInfrastructureEncryption | False (168) | False (34) |  |
| properties.encryption.services.blob.enabled | True (20) | True (38) |  |
| properties.encryption.services.blob.keyType | Account (171) | Account (37) |  |
| properties.encryption.services.file.enabled | True (20) | True (38) |  |
| properties.encryption.services.file.keyType | Account (171) | Account (37) |  |
| properties.minimumTlsVersion | TLS1_2 (157) | TLS1_2 (23) |  |
| properties.networkAcls.bypass | AzureServices (161) | AzureServices (27) |  |
| properties.networkAcls.defaultAction | Deny (164) | Allow (30) | ✗ |
| properties.publicNetworkAccess | Enabled (155) | Enabled (21) |  |
| properties.supportsHttpsTrafficOnly | True (166) | True (32) |  |
| sku.name | Standard_RAGRS (10) | Standard_LRS (10) | ✗ |
| sku.tier | Standard (16) | Standard (14) |  |
| type | Microsoft.Storage/storageAccounts (8) | Microsoft.Storage/storageAccounts (8) |  |

