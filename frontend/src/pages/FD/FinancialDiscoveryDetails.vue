<template>
    <main class="assets-page px-5 relative">
        <div v-if="loading" class="loading absolute inset-0 bg-white z-10">
            <div class="loader flex h-screen items-center">
              <ProgressSpinner />
            </div>
        </div>
        <section class="top-content sticky top-0 z-10 bg-white py-5 mb-5" :class="{'shadow-md' : isScrolled}">
            <div class="    ">
                <TopContent :financial_discovery="financial_discovery" @getFinancialDiscovery="getData" />
            </div>
        </section>
        <section class="re_assets-table py-[30px]">
            <div class="container">
                <ReAssetsTable :real_estate_assets="real_estate_assets" @getFinancialDiscovery="getData" @getRealEstateAssets="getRealEstateAssets" />
            </div>
        </section>
        <section class="other_assets-table py-[30px]">
            <div class="container">
                <OtherAssetsTable @getOtherAssets="getOtherAssets" @getFinancialDiscovery="getData" :other_assets="other_assets" :investors="investors" />
            </div>
        </section>
        <section class="liabilities-table py-[30px]">
            <div class="container">
                <LiabilitiesTable 
                    :liabilities="liabilities" 
                    :monthly_expenses="monthly_expenses" 
                    @getFinancialDiscovery="getData"
                    @getMonthlyExpenses="getMonthlyExpenses"
                    @getLiabilities="getLiabilities" />
            </div>
        </section>
        <section v-if="financial_discovery" class="finance_discovery-section py-[30px]">
            <div class="container">
                <FinanceDiscovery @getFinancialDiscovery="getData" />
            </div>
        </section>
        <ConfirmDialog />
    </main>
</template>
<script>
import TopContent from '@/components/FD/TopContent.vue'
import ReAssetsTable from '@/components/FD/ReAssetsTable.vue'
import OtherAssetsTable from '@/components/FD/OtherAssetsTable.vue'
import LiabilitiesTable from '@/components/FD/LiabilitiesTable.vue'
import FinanceDiscovery from '@/components/FD/FinanceDiscovery.vue'
import {fetch_api} from '@/utils'

export default {
    name: 'FDDetails',
    components: {
        TopContent,
        ReAssetsTable,
        OtherAssetsTable,
        LiabilitiesTable,
        FinanceDiscovery
    },
    data() {
        return {
            loading: false,
            financial_discovery: false,
            annualGrowth:7,
            owner_financial_discovery:"",
            real_estate_assets: [],
            monthly_expenses: [],
            liabilities: [],
            other_assets: [],
            tax_rates: [],
            investors: [],
            isScrolled: false
        }
    }, 
    methods: {
        async getData() {
            this.loading = true
            let params = {
                id: this.$route.params.id
            }
            this.financial_discovery = false
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.get_financial_discovery"
            let res = await fetch_api(url, "POST", params);
            if (res?.message?.financial_discovery) {
                this.financial_discovery = res.message.financial_discovery;
                this.real_estate_assets = res.message.real_estate_assets;
                this.monthly_expenses = res.message.monthly_expenses;
                this.liabilities = res.message.liabilities;
                this.other_assets = res.message.other_assets;
                this.tax_rates = res.message.tax_rates;
                this.investors = res.message.financial_discovery.buyers
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: "Financial Discovery Not Found", life: 5000 });
                this.$router.push({ name: "CreateFD" })
            }
            this.loading = false
        },
        async getRealEstateAssets() {
            let params = { id: this.$route.params.id }
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.get_real_estate_assets"
            let res = await fetch_api(url, "POST", params);
            if (res?.message) {
                this.real_estate_assets = res.message;
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: "Financial Discovery Not Found", life: 5000 });
                this.$router.push({ name: "CreateFD" })
            }
        },
        async getMonthlyExpenses() {
            let params = { id: this.$route.params.id }
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.get_monthly_expenses"
            let res = await fetch_api(url, "POST", params);
            if (res?.message) {
                this.monthly_expenses = res.message;
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: "Financial Discovery Not Found", life: 5000 });
                this.$router.push({ name: "CreateFD" })
            }
        },
        async getLiabilities() {
            let params = { id: this.$route.params.id }
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.get_liabilities"
            let res = await fetch_api(url, "POST", params);
            if (res?.message) {
                this.liabilities = res.message;
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: "Financial Discovery Not Found", life: 5000 });
                this.$router.push({ name: "CreateFD" })
            }
        },
        async getOtherAssets() {
            let params = { id: this.$route.params.id }
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.get_other_assets"
            let res = await fetch_api(url, "POST", params);
            if (res?.message) {
                this.other_assets = res.message;
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: "Financial Discovery Not Found", life: 5000 });
                this.$router.push({ name: "CreateFD" })
            }
        },
        calculateAge(date_of_birth) {
            const birthDate = date_of_birth;
            const today = new Date();
            let age = today.getFullYear() - birthDate.getFullYear();
            return age;
        },
        handleScroll() {
            const scrollPosition = window.scrollY || document.documentElement.scrollTop;
            this.isScrolled = scrollPosition > 50;
        }
    },
    beforeUnmount() {
        window.removeEventListener('scroll', this.handleScroll);
    },
    async mounted() {
        await this.getData()
        window.addEventListener('scroll', this.handleScroll);
    }
}
</script>

<style>

</style>