metadata name = 'Infrastructure for the smallestAzureDataplatform'
metadata description = 'This is the main entry point for the smallestAzureDataplatform'

targetScope = 'subscription'

param location string = 'westeurope'
param rgName string
param dlName string
param fnName string
param fnstgName string
param aspName string
param sqlServerName string

module rg 'br/public:avm/res/resources/resource-group:0.2.4' = {
  name: '${deployment().name}-resourceGroup' 
  params: {
    name: rgName
    location: location
  }
}

module dl 'br/public:avm/res/storage/storage-account:0.9.1' = {
  name: '${deployment().name}-datalake'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
  ]
  params: {
    name: dlName
    location: location
    enableHierarchicalNamespace: true
  }
}

module asp 'br/public:avm/res/web/serverfarm:0.2.2' = {
  name: '${deployment().name}-appServicePlan'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
  ]
  params: {
    name: aspName
    location: location
    skuCapacity: 1 
    skuName: 'B1' 
  } 
}

module fnstg 'br/public:avm/res/storage/storage-account:0.9.1' = {
  name: '${deployment().name}-functionStorage'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
  ]
  params: {
    name: fnstgName
    location: location
  }
}

module fn 'br/public:avm/res/web/site:0.3.9' = {
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
      pythonVersion: '3.9'
    }
    appSettingsKeyValuePairs: {
      FUNCTIONS_WORKER_RUNTIME: 'python'
      FUNCTIONS_EXTENSION_VERSION: '~4'
    }
    managedIdentities: {
      systemAssigned: true
    }
    storageAccountResourceId: fnstg.outputs.resourceId
    storageAccountUseIdentityAuthentication: true
  }
}

module sqlServer 'br/public:avm/res/sql/server:0.4.1' = {
  name: '${deployment().name}-sqlServer'
  scope: resourceGroup(rgName)
  dependsOn: [
    rg
  ]
  params: {
    name: sqlServerName
    location: location
    administrators: {
      azureADOnlyAuthentication: true
      login: 'DBA'
      principalType: 'User'
      sid: 'afd21219-8856-4a5f-a60a-903c217b6ba2'
    }
  }
}
