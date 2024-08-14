metadata name = 'Infrastructure for the smallestAzureDataplatform'
metadata description = 'This is the main entry point for the smallestAzureDataplatform'

targetScope = 'subscription'

param location string = 'northeurope'
param rgName string
param dlName string
param fnName string
param fnstgName string
param aspName string
param sqlServerName string

module rg 'br/public:avm/res/resources/resource-group:0.2.4' = { // Resource group to contain all resources
  name: '${deployment().name}-resourceGroup' 
  params: {
    name: rgName
    location: location
  }
}

module dl 'br/public:avm/res/storage/storage-account:0.9.1' = { // Data lake which will store raw data
  name: '${deployment().name}-datalake'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
  ]
  params: {
    name: dlName
    location: location
    enableHierarchicalNamespace: true // Required to enabled data lake gen2 instead of blob storage
    publicNetworkAccess: 'Enabled'
    blobServices: {
      containers: [
        {
          name: 'raw'
        }
      ]
    }
    // roleAssignments: [
    //   {
    //     principalId: fn.outputs.systemAssignedMIPrincipalId
    //     roleDefinitionIdOrName: 'Storage Blob Data Contributor'
    //   }
    // ]
  }
}

module asp 'br/public:avm/res/web/serverfarm:0.2.2' = { // Hosting for the function app
  name: '${deployment().name}-appServicePlan'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
  ]
  params: {
    name: aspName
    location: location
    skuCapacity: 1 
    skuName: 'B1' // Can't use free tier because it doesn't support deployments from a package
    reserved: true // Required for Linux
    kind: 'Linux' // Needed for a python function app
  } 
}

module fnstg 'br/public:avm/res/storage/storage-account:0.9.1' = { // Storage account for the function app backend (where the function app code is stored)
  name: '${deployment().name}-functionStorage'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
  ]
  params: {
    name: fnstgName
    location: location
    publicNetworkAccess: 'Enabled'
  }
}

module fn 'br/public:avm/res/web/site:0.3.9' = { // Function app which will run the python code
  name: '${deployment().name}-function'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
    asp
    fnstg
  ]
  params: {
    name: fnName
    location: location   
    kind: 'functionapp,linux'
    serverFarmResourceId: asp.outputs.resourceId
    siteConfig: {
      pythonVersion: '3.11'
      linuxFxVersion: 'python|3.11'
    }
    appSettingsKeyValuePairs: {
      FUNCTIONS_WORKER_RUNTIME: 'python'
      FUNCTIONS_EXTENSION_VERSION: '~4'
      WEBSITE_RUN_FROM_PACKAGE: '1' // This is required to deploy the function app from a package (github cicd)
      DATALAKE__blobServiceUri: 'https://${dlName}.blob.${environment().suffixes.storage}/' // Required to have a storage account output binding in the function app
    }
    managedIdentities: {
      systemAssigned: true // Creates a managed identity for the function app to access other azure resources
    }
    storageAccountResourceId: fnstg.outputs.resourceId // Backend storage account for the function app
    storageAccountUseIdentityAuthentication: true // Required to be able to access the storage account without access keys
  }
}

module sqlServer 'br/public:avm/res/sql/server:0.4.1' = { // SQL server which will store the processed data
  name: '${deployment().name}-sqlServer'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
  ]
  params: {
    name: sqlServerName
    location: location
    administrators: { // This enabled entra security by only allowing the specified users to access the server, and disables a root user with a password.
      azureADOnlyAuthentication: true
      login: 'DBA'
      principalType: 'User'
      sid: 'afd21219-8856-4a5f-a60a-903c217b6ba2'
    }
  }
}
