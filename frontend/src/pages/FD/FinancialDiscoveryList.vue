<template>
    <div class="fd_list p-5">
    <DataTable :value="financial_discoveries" showGridlines size="small">
        <template #header>
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-[18px] font-semibold">Financial Discovery</span>
                <Button type="button" label="Create Financial Discovery" icon="pi pi-plus" as="router-link" size="small" :to="{ name: 'CreateFD' }" />
             </div>
        </template>
        <template #empty>Data not available.</template>

        <Column field="fd_name" header="Buyer Name"></Column>
        <Column field="household_type" header="Household Type"></Column>
        <Column field="dependant" header="Dependant"></Column>
        <Column field="tenure_type" header="Tenure Type"></Column>
        <Column field="annual_income_goal" header="Annual Income Goal">
            <template #body="{ data }">
                {{ formatCurrency(data['annual_income_goal']) }}
            </template>
        </Column>
        <Column field="weekly_income_goal" header="Weekly Income Goal">
            <template #body="{ data }">
                {{ formatCurrency(data['weekly_income_goal']) }}
            </template>
        </Column>
        <Column field="retirement_age_goal" header="Retirement Age Goal">
            <template #body="{ data }">
                {{ data['retirement_age_goal'] + " years" }}
            </template>
        </Column>
        <Column field="years_lived_in_current_address" header="Years Lived"></Column>
        <Column field="timeframe" header="Timeframe">
            <template #body="{ data }">
                {{ data['timeframe'].toFixed(2) + " years" }}
            </template>
        </Column>
        <Column field="modified" header="Last Modified" bodyClass="whitespace-nowrap">
            <template #body="{ data }">
                {{ formatDate(new Date(data['modified'])) }}
            </template>
        </Column>

        <Column header="Action" bodyClass="w-[150px]">
            <template #body="{ data }">
                <div class="flex gap-2.5"> 
                <Button icon="pi pi-eye" as="router-link" raised severity="secondary" size="small" 
                    :to="{ name: 'FDDetails', params: { id: data.name } }" />
                <Button icon="pi pi-pencil" as="router-link" raised severity="contrast" size="small" 
                    :to="{ name: 'EditFD', params: { id: data.name } }" />
                </div>
            </template>
        </Column>
    </DataTable>
</div>
</template>

<script>

import { currencyFormat,fetch_api } from '@/utils'
import Button from 'primevue/button';
import moment from 'moment';

export default {
    name: 'FinancialDiscoveryList',
    components: {
        Button
    },
    data() {
        return {
            financial_discoveries: []
        }
    },
    methods: {
        formatCurrency(value) {
            return currencyFormat(value)
        },
        formatDate(value) {
            return moment(value).format('DD/MM/YYYY hh:mm:ss a')
        },
        async getFinancialDiscoveryList() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.get_financial_discoveries"
            let res = await fetch_api(url, "POST", {});
            if (res?.message) {
                this.financial_discoveries = res.message;
            }
        }
    },
    mounted() {
        this.getFinancialDiscoveryList();
    }
}

</script>