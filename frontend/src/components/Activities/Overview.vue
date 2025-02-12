<template>
    <div class="my-3 flex items-center justify-between text-lg font-medium sm:mb-4">
        <div class="box-shadow-1 p-3 w-[100%]" v-for="section in resolvedValues" :key="section.name">
            <div v-if="section.visible">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="">{{ section.label }}</h2>
                    <Button v-if="isManager() && !isMobileView" variant="ghost" @click="showDataFieldsModal = true">
                        <FeatherIcon name="settings" class="h-4 w-4" />
                    </Button>
                </div>
                <div class="flex flex-col flex-1 gap-4">
                    <div v-for="column in section.columns" :key="column.name" class="flex w-[100%] justify-evenly gap-4">
                        <div v-for="field in column.fields" :key="field.title">
                            <div class="flex flex-col gap-1 items-center justify-between">
                                <div class="text-base text-ink-gray-8 font-semibold uppercase">{{ field.title }}</div>
                                <div class="text-base text-ink-gray-8 font-normal">{{ field.value }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="my-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">{{ __("Financial Discovery") }}</h2>
        <div class="grid grid-cols-1 gap-6 mb-5" v-if="financial_discovery?.data?.length > 0">
            <div v-for="fd in financial_discovery.data" :key="fd.name"
                class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold cursor-pointer hover:text-blue-600">
                        <span class="text-gray-800">{{ fd.fd_name }} </span>
                        <span class="text-gray-600"> ( {{ fd.household_type }} - {{ fd.tenure_type }} )</span>
                    </h3>
                    <Button icon="pi pi-arrow-right" @click="gotoFD(fd.name)"></Button>
                </div>
                <div class="space-y-3">
                    <div class="grid grid-cols-3 gap-4 mb-4">
                        <div>
                            <span class="text-gray-600">Retirement Goal</span>
                            <div class="font-medium text-gray-800">
                                Age {{ fd.retirement_age_goal }} ( in {{ fd.timeframe.toFixed(2) }} years )
                            </div>
                        </div>
                        <div>
                            <span class="text-gray-600">Annual Goal</span>
                            <div class="font-medium text-gray-800">${{ formatNumber(fd.annual_income_goal) }}</div>
                        </div>
                        <div>
                            <span class="text-gray-600">Weekly Goal</span>
                            <div class="font-medium text-gray-800">${{ formatNumber(fd.weekly_income_goal) }}</div>
                        </div>
                    </div>
                    <div class="border-t pt-3">
                        <h4 class="text-sm font-semibold text-gray-700 mb-2">Current Financial Status</h4>
                        <div class="flex justify-between">
                            <div>
                                <span class="text-gray-600">Gross Annual Income</span>
                                <div class="font-medium text-gray-800">${{ formatNumber(fd.total_gross_annual_income) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Annual Tax</span>
                                <div class="font-medium text-gray-800">${{ formatNumber(fd.total_tax) }}</div>
                            </div>
                            <div>
                                <span class="text-gray-600">Annual Mortgage Payments</span>
                                <div class="font-medium text-gray-800">${{ formatNumber(fd.total_annual_mortgage_payments) }}</div>
                            </div>
                            <div>
                                <span class="text-gray-600">Net Annual Income</span>
                                <div class="font-medium text-gray-800">${{ formatNumber(fd.total_net_annual_income) }}</div>
                            </div>
                        </div>
                    </div>
                    <div class="border-t pt-3">
                        <h4 class="text-sm font-semibold text-gray-700 mb-2">Retirement Planning</h4>
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <span class="text-gray-600">Lump Sum Needed</span>
                                <div class="font-medium"
                                    :class="{ 'text-red-600': fd.lump_sum_needed < 0, 'text-gray-800': fd.lump_sum_needed >= 0 }">
                                    ${{ formatNumber(fd.lump_sum_needed) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Yearly Savings Needed</span>
                                <div class="font-medium"
                                    :class="{ 'text-red-600': fd.yearly_savings_required_starting_today < 0, 'text-gray-800': fd.yearly_savings_required_starting_today >= 0 }">
                                    ${{ formatNumber(fd.yearly_savings_required_starting_today) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Daily Savings Needed</span>
                                <div class="font-medium"
                                    :class="{ 'text-red-600': fd.daily_savings_required_starting_today < 0, 'text-gray-800': fd.daily_savings_required_starting_today >= 0 }">
                                    ${{ formatNumber(fd.daily_savings_required_starting_today) }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="border-t pt-3">
                        <h4 class="text-sm font-semibold text-gray-700 mb-2">Current Net Worth</h4>
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <span class="text-gray-600">Total Assets</span>
                                <div class="font-medium text-gray-800">${{ formatNumber(fd.total_assets_current) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Total Liabilities</span>
                                <div class="font-medium text-gray-800">${{ formatNumber(fd.total_liabilities_current) }}
                                </div>
                            </div>
                            <div >
                                <span class="text-gray-600">Net Wealth</span>
                                <div class="font-medium"
                                    :class="{ 'text-red-600': fd.net_wealth_current < 0, 'text-green-600': fd.net_wealth_current > 0 }">
                                    ${{ formatNumber(fd.net_wealth_current) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex flex-col justify-center box-shadow-1 p-10 w-[100%]" v-else>
            <div class="text-center">
                <Button as="router-link" icon="pi pi-plus" :to="{'name':'CreateFD',query: { dealname: props.docname }}" label="Create" />
            </div>
        </div>
    </div>
    <OverviewFieldsModal
        v-if="showDataFieldsModal"
        v-model="showDataFieldsModal"
        :doctype="doctype"
        @reload="
        () => {
            tabs.reload()
            data.reload()
        }
        "
    />
</template>

<script setup>
import Button from "primevue/button"
import { computed, ref, watchEffect } from 'vue';
import { useRouter } from 'vue-router';
import { usersStore } from '@/stores/users'
import { isMobileView } from '@/composables/settings'
import OverviewFieldsModal from '@/components/Modals/OverviewFieldsModal.vue'
import {
    createResource,
    createDocumentResource,
    call,
} from 'frappe-ui'

const { isManager } = usersStore()
const router = useRouter()
const props = defineProps({
    doctype: {
        type: String,
        required: true,
    },
    docname: {
        type: String,
        required: true,
    },
})

const showDataFieldsModal = ref(false)
const financial_discovery = createResource({
    url: 'crm.api.utils.get_financial_discovery',
    cache: ['financial_discovery', props.doctype, props.docname],
    params: { doctype: props.doctype, name: props.docname },
    auto: true,
    transform: (data) => data,
})

const tabs = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_overview_layout',
  cache: ['overview_sections', 'CRM Deal'],
  params: { doctype: 'CRM Deal', type: "Overview" },
  auto: true,
})

const data = createDocumentResource({
  doctype: props.doctype,
  name: props.docname,
  setValue: {
    onSuccess: () => {
      data.reload()
      createToast({
        title: 'Data Updated',
        icon: 'check',
        iconClasses: 'text-ink-green-3',
      })
    },
    onError: (err) => {
      createToast({
        title: 'Error',
        text: err.messages[0],
        icon: 'x',
        iconClasses: 'text-red-600',
      })
    },
  },
})

const sections = computed((section)=>{
    return tabs.data?.length ? tabs.data[0]?.sections || [] : []
});

const formatNumber = (value) => {
    return new Intl.NumberFormat('en-US').format(Math.round(value))
}

const resolvedValues = ref([]);
watchEffect(async () => {
    if (!sections.value) return;

    const updatedSections = await Promise.all(
        sections.value.map(async (section) => {
            return {
                ...section,
                columns: await Promise.all(
                    section.columns.map(async (column) => {
                        return {
                            ...column,
                            fields: await Promise.all(
                                column.fields.map(async (field) => {
                                    const value = await getValue(data.doc, field);
                                    return {
                                        ...field,
                                        value,
                                    };
                                })
                            ),
                        };
                    })
                ),
            };
        })
    );

    resolvedValues.value = updatedSections;
});

async function getValue(doc,field){
    if (!doc || !field) return "";

    if(field.fieldtype === 'Link'){
        if (['stage'].includes(field.field)){
            const get_value = await call('frappe.desk.search.search_link',{
                doctype: field.options,
                filters: {
                    name: doc[field.field]
                },
                txt:doc[field.field]
            })
            return get_value.length ? get_value[0]?.label || get_value[0]?.value : doc[field.field]
        }else{
            return doc[field.field]
        }
    } else if(field.fieldtype === 'Currency'){
        return `$${formatNumber(doc[field.field])}`
    } else {
        return doc[field.field]
    }
}

function gotoFD(name){
    router.push({
        name: 'FDDetails',
        params: { id: name }
    })
}

</script>

<style scoped>
.box-shadow-1 {
    box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}
</style>