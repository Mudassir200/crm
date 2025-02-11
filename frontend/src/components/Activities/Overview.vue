<template>
    <div class="my-3 flex items-center justify-between text-lg font-medium sm:mb-4">
        <div class="box-shadow-1 p-3 w-[100%]" v-for="section in sections" :key="section.title">
            <div v-if="section.visible">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="">{{ section.title }}</h2>
                    <Button v-if="section.editable" variant="ghost">
                        <FeatherIcon name="settings" class="h-4 w-4" />
                    </Button>
                </div>
                <div class="flex flex-col flex-1 gap-4">
                    <div v-for="row in section.items" :key="row[0].title" class="flex w-[100%] justify-evenly gap-4">
                        <div v-for="item in row" :key="item.title">
                            <div class="flex flex-col gap-1 items-center justify-between">
                                <div class="text-base text-ink-gray-8 font-semibold uppercase">{{ item.title }}</div>
                                <div class="text-base text-ink-gray-8 font-normal">{{ item.value }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="my-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">{{ __("Financial Discovery") }}</h2>
        <div class="grid grid-cols-1 gap-6 mb-5">
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
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Button from "primevue/button"

import {
    createResource,
    createDocumentResource,
    Tooltip,
    Avatar,
    Tabs,
    call,
    usePageMeta,
} from 'frappe-ui'

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

const financial_discovery = createResource({
    url: 'crm.api.utils.get_financial_discovery',
    cache: ['financial_discovery', props.doctype, props.docname],
    params: { doctype: props.doctype, name: props.docname },
    auto: true,
    transform: (data) => data,
})

const sections = ref([{
    title: "Data Highlights",
    type: "highlight",
    editable: true,
    visible: true,
    items: [
        [
            {
                "title": "Create Date",
                "value": "28/11/2024 10:54 AM GMT+5:30",
            },
            {
                "title": "Deal Stage",
                "value": "Ready 3-6 Months",
            },
            {
                "title": "Last Activity Date",
                "value": "28/11/2024 10:55 AM GMT+5:30",
            },
        ],
        [
            {
                "title": "Status",
                "value": "Qualification",
            },
            {
                "title": "Deal Owner",
                "value": "Administrator",
            },
            {
                "title": "Deal Type",
                "value": "New Business",
            }
        ]
    ]
}])

const formatNumber = (value) => {
    return new Intl.NumberFormat('en-US').format(Math.round(value))
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