<template>
    <div class="home-page px-5">
        <section class="max-w-[1024px] w-full mx-auto">
            
            <div class="hh-info_form-container py-10">
                <div v-if="dealname || organization" class="form hh_info-form mb-10">
                    <h6 v-if="dealname" class="page-title mb-2">
                        <strong>{{ __('Deal :')}}</strong>
                        <span class="ml-2">{{ dealname }}</span>
                    </h6>
                    <h6 v-if="organization" class="page-title mb-2">
                        <strong>{{ __('Buyer :')}}</strong>
                        <span class="ml-2">{{ organization }}</span>
                    </h6>
                </div>
                <div  class="form hh_info-form mb-10">
                </div>
                <div class="form hh_info-form mb-10">
                    <h6 class="page-title mb-5">Household Information</h6>
                    <div
                        class="fields grid lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-y-[15px] gap-x-5">
                        <div class="field">
                            <label for="household_type text-red">Household Type</label>
                            <Select v-model="hh_info.household_type" :options="hhtypes" optionLabel="label"
                                placeholder="Select Household Type"
                                :invalid="isSubmitedForm && !hh_info.household_type" />
                        </div>
                        <div class="field">
                            <label for="dependant">{{ "Dependants (<18yr)" }}</label>
                                    <Select v-model="hh_info.dependant" :options="dependant_option" optionLabel="label"
                                        placeholder="Select Dependant"
                                        :invalid="isSubmitedForm && !hh_info.dependant" />
                        </div>
                        <div class="field">
                            <label for="tenure_type">Tenure Type</label>
                            <Select v-model="hh_info.tenure_type" :options="tenure_types" optionLabel="label"
                                placeholder="Select Tenure Type" :invalid="isSubmitedForm && !hh_info.tenure_type" />
                        </div>
                        <div class="field">
                            <label for="years_lived_in_current_address">Years lived in current address</label>
                            <InputNumber :maxFractionDigits="0" v-model="hh_info.years_lived_in_current_address"
                                :invalid="isSubmitedForm && (!hh_info.years_lived_in_current_address && hh_info.years_lived_in_current_address == null)" />
                        </div>
                    </div>
                </div>

                <!-- <Divider /> -->

                <div class="form buyer_info-form mb-10">
                    <h6 class="page-title mb-5">Personal Information</h6>
                    <div v-for="(buyer, index) in buyers" :key="index" :class="{ 'mb-4': buyers?.length > 1 }">
                        <div class="form-title text-body font-medium mb-2.5 text-[16px]">Individual {{ index + 1 }}
                            Information</div>
                        <div
                            class="fields grid xl:grid-cols-5 lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-y-[15px] gap-x-5">
                            <div class="field">
                                <label for="firstname">First Name</label>
                                <InputText id="firstname" v-model="buyer.first_name" autocomplete="off"
                                    :invalid="isSubmitedForm && !buyer.first_name" />
                            </div>
                            <div class="field">
                                <label for="surname">Surname</label>
                                <InputText id="surname" v-model="buyer.surname" autocomplete="off"
                                    :invalid="isSubmitedForm && !buyer.surname" />
                            </div>
                            <div class="field">
                                <label for="date_of_birth">Date of Birth</label>
                                <DatePicker id="date_of_birth" v-model="buyer.date_of_birth" dateFormat="dd/mm/yy"
                                    :maxDate="maxDate"
                                    :invalid="isSubmitedForm && (buyer.date_of_birth == '' || buyer.date_of_birth == null)" />
                            </div>
                            <div class="field">
                                <label for="age">Age</label>
                                <InputText id="age" v-model="buyer.age" disabled autocomplete="off" />
                            </div>
                            <div class="field">
                                <label for="occupation">Occupation</label>
                                <InputText id="occupation" v-model="buyer.occupation" autocomplete="off" />
                            </div>
                            <div class="field">
                                <label for="employment_type">Employment Type</label>
                                <Select v-model="buyer.employment_type" :options="Occupations" optionLabel="label"
                                    placeholder="Select Employment Type" />
                            </div>
                            <div class="field">
                                <label for="length_of_employment_yrs">Length of Employment (yrs)</label>
                                <InputNumber :maxFractionDigits="0" id="length_of_employment_yrs"
                                    v-model="buyer.length_of_employment_yrs" autocomplete="off" />
                            </div>
                            <div class="field">
                                <label for="gross_annual_income">Annual Income (incl. Super)</label>
                                <InputNumber :minFractionDigits="0" :maxFractionDigits="2"
                                    v-model="buyer.gross_annual_income" inputId="gross_annual_income" mode="currency"
                                    currency="USD" locale="en-US"
                                    :invalid="isSubmitedForm && !buyer.gross_annual_income" />
                            </div>
                            <div class="field">
                                <label for="untaxed_income">Untaxed Income</label>
                                <InputNumber :minFractionDigits="0" :maxFractionDigits="2"
                                    v-model="buyer.untaxed_income" inputId="untaxed_income" mode="currency"
                                    currency="USD" locale="en-US" />
                            </div>
                        </div>
                    </div>
                </div>

                <div class="form buyer_info-form mb-10">
                    <h6 class="page-title mb-5">Passive Income Goal</h6>
                    <div
                        class="fields grid lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-y-[15px] gap-x-5">
                        <div class="field">
                            <label for="retirement_age_goal">Retirement Age Goal</label>
                            <InputNumber :maxFractionDigits="0" v-model="hh_info.retirement_age_goal"
                                :invalid="isSubmitedForm && !hh_info.retirement_age_goal" />
                        </div>
                        <div class="field">
                            <label for="annual_income_goal">Annual Income Goal</label>
                            <InputNumber :minFractionDigits="0" :maxFractionDigits="2"
                                v-model="hh_info.annual_income_goal" inputId="annual_income_goal" mode="currency"
                                currency="USD" locale="en-US"
                                :invalid="isSubmitedForm && !hh_info.annual_income_goal" />
                        </div>
                        <div class="field">
                            <label for="weekly_income_goal">Weekly Income Goal</label>
                            <InputNumber :minFractionDigits="0" :maxFractionDigits="2"
                                v-model="hh_info.weekly_income_goal" inputId="weekly_income_goal" mode="currency"
                                currency="USD" locale="en-US" disabled />
                        </div>
                        <div class="field">
                            <label for="timeframe">Timeframe</label>
                            <InputNumber :maxFractionDigits="2" v-model="timeframe" inputId="timeframe"
                                :invalid="isSubmitedForm && !timeframe" />
                        </div>
                    </div>
                </div>
                <div class="flex justify-between btn-submit text-center">
                    <Button label="Back To List" severity="secondary"  icon="pi pi-arrow-left" iconPos="left"
                        @click="$router.push({ name: 'FDList' })" raised />
                    <Button label="Continue" class="w-[200px] h-[46px]" icon="pi pi-arrow-right" iconPos="right"
                        size="large" :loading="loading" @click="submit" />
                </div>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref, reactive, watch, computed, onMounted, toRaw } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from 'primevue/button'
import { createResource } from 'frappe-ui'
import { createToast } from '@/utils'
import { useLoadingStore } from "@/stores/loading"; 

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const maxDate = ref(new Date())
const isSubmitedForm = ref(false)
const loadingStore = useLoadingStore();

const hh_info = reactive({
    household_type: { label: "Single", value: "Single" },
    dependant: { label: 'No', value: "No" },
    tenure_type: "",
    years_lived_in_current_address: 0,
    retirement_age_goal: 0,
    annual_income_goal: 0,
    weekly_income_goal: 0
})

const buyers = reactive([{
    contact: '',
    first_name: "",
    surname: '',
    date_of_birth: '',
    age: '',
    employment_type: "",
    length_of_employment_yrs: '',
    occupation: '',
    gross_annual_income: 0,
    untaxed_income: 0,
}])

const dependant_option = [
    { label: 'Yes', value: "Yes" },
    { label: 'No', value: "No" },
]

const Occupations = [
    { label: 'PAYG', value: 'PAYG' },
    { label: 'Self-Employed', value: 'Self-Employed' },
    { label: 'Retired', value: 'Retired' },
    { label: 'Unemployed', value: 'Unemployed' },
]

const hhtypes = [
    { label: "Single", value: "Single" },
    { label: "Couple", value: "Couple" },
]

const tenure_types = [
    { label: "Renting", value: "Renting" },
    { label: "Owned with Mortgage", value: "Owned with Mortgage" },
    { label: "Owned Outright", value: "Owned Outright" },
]

// Watchers
watch(() => hh_info.household_type, (newType) => {
    if (newType.value === "Couple" && buyers.length === 1) {
        buyers.push({
            contact: '',
            first_name: '',
            surname: '',
            date_of_birth: '',
            age: '',
            occupation: '',
            length_of_employment_yrs: '',
            employment_type: '',
            gross_annual_income: 0,
            untaxed_income: 0,
        })
    } else if (newType.value !== "Couple" && buyers.length > 1) {
        buyers.splice(1)
    }
})

watch(buyers, (newBuyers) => {
    newBuyers.forEach((buyer) => {
        if (buyer.date_of_birth) {
            buyer.age = calculateAge(buyer.date_of_birth)
        }
    })
}, { deep: true })

watch(() => hh_info.annual_income_goal, (data) => {
    if (data != undefined && data != null && data > 0) {
        hh_info.weekly_income_goal = Math.round(data / 52)
    }
})

// Computed
const timeframe = computed(() => {
    if (hh_info.retirement_age_goal == "") {
        return ""
    } else if (buyers[0].date_of_birth == "") {
        return 0
    } else {
        const today = new Date()
        const birthDateMillis = new Date(buyers[0].date_of_birth).getTime()
        const todayMillis = today.getTime()
        const differenceMillis = todayMillis - birthDateMillis
        const differenceDays = differenceMillis / (1000 * 60 * 60 * 24 * 365)
        let timeframe = hh_info.retirement_age_goal - differenceDays
        return timeframe < 0 ? 0 : timeframe
    }
})

// Methods
const calculateAge = (date_of_birth) => {
    const birthDate = date_of_birth
    const today = new Date()
    return today.getFullYear() - birthDate.getFullYear()
}

const checkValidity = () => {
    let validate = true
    let required = {
        household_type: "",
        dependant: 0,
        tenure_type: "",
        years_lived_in_current_address: 0,
        retirement_age_goal: 0,
        annual_income_goal: 0,
    }
    let requiredBuyer = {
        first_name: '',
        surname: '',
        date_of_birth: '',
        gross_annual_income: 0
    }

    if (timeframe.value == null || timeframe.value == undefined || timeframe.value === "") {
        validate = false
    }

    for (let key in required) {
        if (hh_info[key] == null || hh_info[key] == undefined || hh_info[key] === "") {
            validate = false
        }
        if (key == "annual_income_goal" && hh_info[key] <= 0) {
            validate = false
        }
        if (key == "retirement_age_goal" && hh_info[key] <= 0) {
            validate = false
        }
    }

    for (let key in requiredBuyer) {
        if (buyers[0][key] == null || buyers[0][key] == undefined || buyers[0][key] === "" || !buyers[0][key]) {
            validate = false
        }
        if (hh_info.household_type?.value == "Couple") {
            if (buyers[1][key] == null || buyers[1][key] == undefined || buyers[1][key] === "" || !buyers[1][key]) {
                validate = false
            }
        }
    }

    return validate
}
const dealname = computed(() => route?.query?.dealname || '')
const organization = computed(() => route?.query?.organization || '')

const organizationBuyers = createResource({
    url: 'crm.api.utils.get_organizaion_contacts',
    cache: ['get_organizaion_contacts'],
    params: { name: dealname.value },
})

async function get_buyer_details() {
    
    
    let org_buyers = []

    if (dealname.value) {
        org_buyers = await organizationBuyers.fetch();
        
    }else if(organization.value){
        organizationBuyers.update({
            params: { name: organization.value,org:true },
        })
        org_buyers = await organizationBuyers.fetch();
    }else{
        createToast({
            title: __('No buyer details found.'),
            icon: 'x',
            iconClasses: 'text-red-700',
        })
    }
    if (org_buyers.length > 0) {
        buyers.length = 0 // Clear the existing buyers array before adding new ones
        org_buyers.map(buyer => {
            buyers.push({
                contact: buyer.name,
                first_name: buyer.first_name,
                surname: buyer.last_name,
                date_of_birth: new Date(buyer.date_of_birth), 
                age: '',
                employment_type: '',
                length_of_employment_yrs: '',
                occupation: '',
                gross_annual_income: 0,
                untaxed_income: 0,
            })
        })
        if (org_buyers.length == 2) {
            hh_info.household_type = { label: "Couple", value: "Couple" }
        }
    }
    loadingStore.setLoading(false);
}

const submit = async () => {
    isSubmitedForm.value = true
    loading.value = true
    if (checkValidity()) {
        createResource({
            url: 'crm.financial_discovery.api.financial_discovery.create_financial_discovery',
            params: {
                data: {
                    ...toRaw(hh_info),
                    timeframe: timeframe.value,
                    dependant: hh_info.dependant?.value,
                    household_type: hh_info.household_type?.value,
                    tenure_type: hh_info.tenure_type?.value,
                    dealname: dealname.value,
                    organization: organization.value,
                },
                buyers: buyers.map(item => ({
                    ...item,
                    employment_type: item.employment_type?.value
                })),
            },
            auto: true,
            onSuccess: (res) => {
                createToast({
                    title: __('Financial Discovery created successfully.'),
                    icon: 'check',
                    iconClasses: 'text-ink-green-3',
                })
                router.push({ name: "FDDetails", params: { id: res?.name } })
            },
            onError: (err) => {
                createToast({
                    title: __('Error updating deal'),
                    text: __(err.messages?.[0]),
                    icon: 'x',
                    iconClasses: 'text-ink-red-4',
                })
            },
        })
    }
    loading.value = false
}

onMounted(get_buyer_details)
</script>

<style scoped>
:deep(.p-inputnumber-input) {
    width: 100%;
}

.home-page .hh-info_form-container .form .field input,
.home-page .hh-info_form-container .form .field .p-select,
.home-page .hh-info_form-container .form .field .p-inputnumber,
.home-page .hh-info_form-container .form .field .p-datepicker {
    width: 100%;
}

label {
    font-size: 14px;
}
</style>