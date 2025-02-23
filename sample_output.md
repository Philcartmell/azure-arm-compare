# Summary

## Ignored Properties

The following properties were ignored during comparisons:
- dependsOn[0]
- dependsOn[1]
- name

## Compared Resources

| Resource Type | Name | Total Properties | Correct | Incorrect |
| --- | --- | --- | --- | --- |
| Microsoft.Storage/storageAccounts/blobServices | [storage001/default](#microsoftstoragestorageaccountsblobservices-storage001default) | 14 | 12 | 0 |
| Microsoft.Storage/storageAccounts/fileServices | [storage001/default](#microsoftstoragestorageaccountsfileservices-storage001default) | 8 | 6 | 0 |
| Microsoft.Storage/storageAccounts/queueServices | [storage001/default](#microsoftstoragestorageaccountsqueueservices-storage001default) | 5 | 2 | 1 |
| Microsoft.Storage/storageAccounts/tableServices | [storage001/default](#microsoftstoragestorageaccountstableservices-storage001default) | 5 | 2 | 1 |
| Microsoft.Storage/storageAccounts/blobServices/containers | [storage001/default/images](#microsoftstoragestorageaccountsblobservicescontainers-storage001defaultimages) | 9 | 5 | 1 |
| Microsoft.Storage/storageAccounts | [storage001](#microsoftstoragestorageaccounts-storage001) | 25 | 19 | 5 |

---

<a id="microsoftstoragestorageaccountsblobservices-storage001default"></a>
### Comparison for Resource: Microsoft.Storage/storageAccounts/blobServices / storage001/default

| Property Path | Left Value | Right Value | Fail |
| --- | --- | --- | --- |
| apiVersion | 2023-05-01 | 2023-05-01 |  |
| dependsOn[0] | [resourceId('Microsoft.Storage/storageAccounts', 'storage001')] | [resourceId('Microsoft.Storage/storageAccounts', 'storage002')] | Ignored |
| name | storage001/default | storage002/default | Ignored |
| properties.changeFeed.enabled | False | False |  |
| properties.containerDeleteRetentionPolicy.days | 7 | 7 |  |
| properties.containerDeleteRetentionPolicy.enabled | True | True |  |
| properties.deleteRetentionPolicy.allowPermanentDelete | False | False |  |
| properties.deleteRetentionPolicy.days | 7 | 7 |  |
| properties.deleteRetentionPolicy.enabled | True | True |  |
| properties.isVersioningEnabled | False | False |  |
| properties.restorePolicy.enabled | False | False |  |
| sku.name | Standard_RAGRS | Standard_RAGRS |  |
| sku.tier | Standard | Standard |  |
| type | Microsoft.Storage/storageAccounts/blobServices | Microsoft.Storage/storageAccounts/blobServices |  |


<a id="microsoftstoragestorageaccountsfileservices-storage001default"></a>
### Comparison for Resource: Microsoft.Storage/storageAccounts/fileServices / storage001/default

| Property Path | Left Value | Right Value | Fail |
| --- | --- | --- | --- |
| apiVersion | 2023-05-01 | 2023-05-01 |  |
| dependsOn[0] | [resourceId('Microsoft.Storage/storageAccounts', 'storage001')] | [resourceId('Microsoft.Storage/storageAccounts', 'storage002')] | Ignored |
| name | storage001/default | storage002/default | Ignored |
| properties.shareDeleteRetentionPolicy.days | 7 | 7 |  |
| properties.shareDeleteRetentionPolicy.enabled | True | True |  |
| sku.name | Standard_RAGRS | Standard_RAGRS |  |
| sku.tier | Standard | Standard |  |
| type | Microsoft.Storage/storageAccounts/fileServices | Microsoft.Storage/storageAccounts/fileServices |  |


<a id="microsoftstoragestorageaccountsqueueservices-storage001default"></a>
### Comparison for Resource: Microsoft.Storage/storageAccounts/queueServices / storage001/default

| Property Path | Left Value | Right Value | Fail |
| --- | --- | --- | --- |
| apiVersion | 2023-05-01 | 2023-05-01 |  |
| dependsOn[0] | [resourceId('Microsoft.Storage/storageAccounts', 'storage001')] | [resourceId('Microsoft.Storage/storageAccounts', 'storage002')] | Ignored |
| name | storage001/default | storage002/default | Ignored |
| properties.cors.corsRules[0] |  | zzz | ✗ |
| type | Microsoft.Storage/storageAccounts/queueServices | Microsoft.Storage/storageAccounts/queueServices |  |


<a id="microsoftstoragestorageaccountstableservices-storage001default"></a>
### Comparison for Resource: Microsoft.Storage/storageAccounts/tableServices / storage001/default

| Property Path | Left Value | Right Value | Fail |
| --- | --- | --- | --- |
| apiVersion | 2023-05-01 | 2023-05-01 |  |
| dependsOn[0] | [resourceId('Microsoft.Storage/storageAccounts', 'storage001')] | [resourceId('Microsoft.Storage/storageAccounts', 'storage002')] | Ignored |
| name | storage001/default | storage002/default | Ignored |
| properties.cors.corsRules[0] | abc |  | ✗ |
| type | Microsoft.Storage/storageAccounts/tableServices | Microsoft.Storage/storageAccounts/tableServices |  |


<a id="microsoftstoragestorageaccountsblobservicescontainers-storage001defaultimages"></a>
### Comparison for Resource: Microsoft.Storage/storageAccounts/blobServices/containers / storage001/default/images

| Property Path | Left Value | Right Value | Fail |
| --- | --- | --- | --- |
| apiVersion | 2023-05-01 | 2023-05-01 |  |
| dependsOn[0] | [resourceId('Microsoft.Storage/storageAccounts/blobServices', 'storage001', 'default')] | [resourceId('Microsoft.Storage/storageAccounts/blobServices', 'storage002', 'default')] | Ignored |
| dependsOn[1] | [resourceId('Microsoft.Storage/storageAccounts', 'storage001')] | [resourceId('Microsoft.Storage/storageAccounts', 'storage002')] | Ignored |
| name | storage001/default/images | storage002/default/images | Ignored |
| properties.defaultEncryptionScope | $account-encryption-key | $account-encryption-key |  |
| properties.denyEncryptionScopeOverride | True | False | ✗ |
| properties.immutableStorageWithVersioning.enabled | False | False |  |
| properties.publicAccess | None | None |  |
| type | Microsoft.Storage/storageAccounts/blobServices/containers | Microsoft.Storage/storageAccounts/blobServices/containers |  |


<a id="microsoftstoragestorageaccounts-storage001"></a>
### Comparison for Resource: Microsoft.Storage/storageAccounts / storage001

| Property Path | Left Value | Right Value | Fail |
| --- | --- | --- | --- |
| apiVersion | 2023-05-01 | 2023-05-01 |  |
| kind | StorageV2 | StorageV2 |  |
| location | uksouth | uksouth |  |
| name | storage001 | storage002 | Ignored |
| properties.accessTier | Hot | Hot |  |
| properties.allowBlobPublicAccess | True | True |  |
| properties.allowCrossTenantReplication | False | True | ✗ |
| properties.allowSharedKeyAccess | False | True | ✗ |
| properties.allowedCopyScope | AAD | AAD |  |
| properties.defaultToOAuthAuthentication | True | False | ✗ |
| properties.dnsEndpointType | Standard | Standard |  |
| properties.encryption.keySource | Microsoft.Storage | Microsoft.Storage |  |
| properties.encryption.requireInfrastructureEncryption | False | False |  |
| properties.encryption.services.blob.enabled | True | True |  |
| properties.encryption.services.blob.keyType | Account | Account |  |
| properties.encryption.services.file.enabled | True | True |  |
| properties.encryption.services.file.keyType | Account | Account |  |
| properties.minimumTlsVersion | TLS1_2 | TLS1_2 |  |
| properties.networkAcls.bypass | AzureServices | AzureServices |  |
| properties.networkAcls.defaultAction | Deny | Allow | ✗ |
| properties.publicNetworkAccess | Enabled | Enabled |  |
| properties.supportsHttpsTrafficOnly | True | True |  |
| sku.name | Standard_RAGRS | Standard_LRS | ✗ |
| sku.tier | Standard | Standard |  |
| type | Microsoft.Storage/storageAccounts | Microsoft.Storage/storageAccounts |  |

