using 'main.bicep'

// Resource names using CAF naming conventions <resourcetype>-<appname>-<workloadname>-<environment>-<region>-<instance>
param rgName =  'rg-don-sad-d-euw-01'
param dlName =  'dldonsaddeuw01' // Storage account is not allowed to have special characters as -.
param aspName = 'asp-don-sad-d-euw-01'
param fnstgName = 'fnstgdonsaddeuw01'
param fnName = 'fn-don-sad-d-euw-01'

