import { createResource } from 'frappe-ui'

export function useFinancialDiscovery() {
  const resources = {
    calculate: createResource({
      url: 'crm.financial_discovery.api.financial_discovery.calculateAllFDFields',
      transform: (data) => data.message
    }),
    
    updateField: createResource({
      url: 'crm.financial_discovery.api.financial_discovery.updateField',
      transform: (data) => data.message
    })
  }

  const updateFieldValue = async (fieldName, value, id) => {
    try {
      const result = await resources.updateField.submit({
        id,
        field: fieldName,
        value
      })
      return result
    } catch (error) {
      throw error
    }
  }

  return {
    resources,
    updateFieldValue
  }
}
