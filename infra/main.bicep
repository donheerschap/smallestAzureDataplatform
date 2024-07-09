metadata name = 'Infrastructure for the smallestAzureDataplatform'
metadata description = 'This is the main entry point for the smallestAzureDataplatform'

targetScope = 'subscription'

param location string = 'westeurope'
param rgName string

module rg 'br/public:avm/res/resources/resource-group:0.2.4' = {
  name: '${deployment().name}-resourceGroup' 
  params: {
    // Required parameters
    name: rgName
    // Non-required parameters
    location: location
  }
}
