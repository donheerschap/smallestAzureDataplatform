using 'main.bicep'

// Resource names using CAF naming conventions <resourcetype>-<appname>-<workloadname>-<environment>-<region>-<instance>
param rgName =  'rg-don-sad-d-eun-01'
param dlName =  'dldonsaddeun01' // Storage account is not allowed to have special characters as -.
param aspName = 'asp-don-sad-d-eun-01'
param fnstgName = 'fnstgdonsaddeun01'
param fnName = 'fn-don-sad-d-eun-01'
param sqlServerName = 'sql-don-sad-d-eun-01'

