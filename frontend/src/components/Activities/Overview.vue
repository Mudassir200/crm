<template>
    <div class="my-3 flex flex-col gap-3 items-center justify-between text-lg font-medium sm:mb-4">
        <div class="shadow-md mb-4 hover:shadow-lg transition-shadow duration-300 p-3 w-[100%]"
            v-for="section in resolvedValues" :key="section.name">
            <div v-if="section.visible">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="">{{ section.label }}</h2>
                    <Button v-if="section.editable && isManager() && !isMobileView" variant="subtle"
                        @click="showDataFieldsModal = true">
                        <FeatherIcon name="settings" class="h-4 w-4" />
                    </Button>
                </div>
                <div class="grid w-full gap-4" 
                    :style="`grid-template-columns: repeat(${section.columns.length}, minmax(0, 1fr));`">
                    <div v-for="column in section.columns" :key="column.name" class="flex flex-col gap-4">
                        <div v-for="field in column.fields" :key="field.title" class="flex flex-col gap-1 items-center">
                            <div class="text-base text-ink-gray-8 font-semibold uppercase">{{ field.title }}</div>
                            <div class="text-base text-ink-gray-8 font-normal">{{ field.value }}</div>
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
                    <Button variant="subtle" @click.stop="router.push({ name: 'FDDetails', params: { id: fd.name } })">
                        <FeatherIcon name="arrow-right" class="h-4 w-4" />
                    </Button>
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
                            <div class="font-medium text-gray-800">{{ getFormattedCurrency('annual_income_goal',fd) }}</div>
                        </div>
                        <div>
                            <span class="text-gray-600">Weekly Goal</span>
                            <div class="font-medium text-gray-800">{{ getFormattedCurrency('weekly_income_goal',fd) }}</div>
                        </div>
                    </div>
                    <div class="border-t pt-3">
                        <h4 class="text-sm font-semibold text-gray-700 mb-2">Current Financial Status</h4>
                        <div class="flex justify-between">
                            <div>
                                <span class="text-gray-600">Gross Annual Income</span>
                                <div class="font-medium text-gray-800">{{ getFormattedCurrency('total_gross_annual_income',fd) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Annual Tax</span>
                                <div class="font-medium text-gray-800">{{ getFormattedCurrency('total_tax',fd) }}</div>
                            </div>
                            <div>
                                <span class="text-gray-600">Annual Mortgage Payments</span>
                                <div class="font-medium text-gray-800">{{
                                    getFormattedCurrency('total_annual_mortgage_payments',fd) }}</div>
                            </div>
                            <div>
                                <span class="text-gray-600">Net Annual Income</span>
                                <div class="font-medium text-gray-800">{{ getFormattedCurrency('total_net_annual_income',fd) }}
                                </div>
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
                                    {{ getFormattedCurrency('lump_sum_needed',fd) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Yearly Savings Needed</span>
                                <div class="font-medium"
                                    :class="{ 'text-red-600': fd.yearly_savings_required_starting_today < 0, 'text-gray-800': fd.yearly_savings_required_starting_today >= 0 }">
                                    {{ getFormattedCurrency('yearly_savings_required_starting_today',fd) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Daily Savings Needed</span>
                                <div class="font-medium"
                                    :class="{ 'text-red-600': fd.daily_savings_required_starting_today < 0, 'text-gray-800': fd.daily_savings_required_starting_today >= 0 }">
                                    {{ getFormattedCurrency('daily_savings_required_starting_today',fd) }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="border-t pt-3">
                        <h4 class="text-sm font-semibold text-gray-700 mb-2">Current Net Worth</h4>
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <span class="text-gray-600">Total Assets</span>
                                <div class="font-medium text-gray-800">{{ getFormattedCurrency('total_assets_current',fd) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Total Liabilities</span>
                                <div class="font-medium text-gray-800">{{ getFormattedCurrency('total_liabilities_current',fd) }}
                                </div>
                            </div>
                            <div>
                                <span class="text-gray-600">Net Wealth</span>
                                <div class="font-medium"
                                    :class="{ 'text-red-600': fd.net_wealth_current < 0, 'text-green-600': fd.net_wealth_current > 0 }">
                                    {{ getFormattedCurrency('net_wealth_current',fd) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex flex-col justify-center shadow-md hover:shadow-lg transition-shadow duration-300 p-10 w-[100%]"
            v-else>
            <div class="text-center">
                <Button variant="subtle" tooltip="create"
                    @click.stop="router.push({ 'name': 'CreateFD', query: { dealname: props.docname } })">
                    <div class="flex justify-center gap-1 items-center">
                        <FeatherIcon name="plus" class="h-4 w-4" />
                        {{ __("Create Financial Discovery") }}
                    </div>
                </Button>
            </div>
        </div>
    </div>
    <OverviewFieldsModal v-if="showDataFieldsModal" v-model="showDataFieldsModal" :doctype="doctype" @reload="() => {
        tabs.reload()
        data.reload()
    }" />
</template>

<script setup>
import OverviewFieldsModal from '@/components/Modals/OverviewFieldsModal.vue'
import { usersStore } from '@/stores/users'
import { getMeta } from '@/stores/meta'
import { isMobileView } from '@/composables/settings'
import { createResource, createDocumentResource, call} from 'frappe-ui'
import { useRouter } from 'vue-router';
import { computed, ref, watchEffect } from 'vue';

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

const { getFormattedCurrency } = getMeta(props.doctype)
const { isManager } = usersStore()
const router = useRouter()
const showDataFieldsModal = ref(false)
const resolvedValues = ref([]);

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
    name: props.docname
})

const sections = computed(() => tabs.data?.[0]?.sections || []);

watchEffect(async () => {
    if (!sections.value) return;
    resolvedValues.value = await Promise.all(sections.value.map(async section => ({
        ...section,
        columns: await Promise.all(section.columns.map(async column => ({
            ...column,
            fields: await Promise.all(column.fields.map(async field => ({
                ...field,
                value: await getValue(data.doc, field)
            })))
        })))
    })));
});

async function getValue(doc, field) {
    if (!doc || !field) return "";
    if (field.fieldtype === "Link" && field.field === "stage") {
        const get_value = await call("frappe.desk.search.search_link", {
            doctype: field.options,
            filters: { name: doc[field.field] },
            txt: doc[field.field],
        });
        return get_value?.[0]?.label || get_value?.[0]?.value || doc[field.field];
    }
    return field.fieldtype === "Currency" ? getFormattedCurrency(field.field,doc) : doc[field.field];    
}

</script>
