<template>
    <div class="contents-comp flex justify-between items-center flex-wrap gap-5">
        <div class="buyers-content flex gap-5 items-center flex-wrap" @click="editBuyer(financial_discovery.name)">
            <div class="hh-info cursor-pointer" v-tooltip.top="'Please Click For Edit'">
                <!-- <div :class="{'flex gap-2 items-center' : financial_discovery.household_type == 'Single'}"> -->
                    <div class="flex gap-2 items-center">
                        <div class="text-[22px] font-semibold">{{ owner_financial_discovery }}</div>
                        <p v-if="financial_discovery.household_type == 'Single'">{{ single_buyer?.occupation != "" && single_buyer?.employment_type != "" ?
                            `${single_buyer.occupation} - ${single_buyer.employment_type}` :
                            single_buyer?.occupation != "" ? single_buyer?.occupation : single_buyer?.employment_type != "" ?
                                single_buyer?.employment_type : ""}}</p>
                    </div>
                    <div class="flex gap-2 items-center">
                        <div v-if="financial_discovery.household_type == 'Single'" class="font-medium">{{ single_buyer?.age }} years old | {{ formatCurrency(single_buyer.gross_annual_income)}}</div>
                        <p v-if="financial_discovery.household_type == 'Single'">{{ financial_discovery.household_type }} - {{ financial_discovery.tenure_type }}</p>
                    </div>
                <!-- </div> -->
                <p v-if="financial_discovery.household_type == 'Couple'">{{ financial_discovery.household_type }} - {{ financial_discovery.tenure_type }}</p>
            </div>
            <div v-if="financial_discovery.buyers && financial_discovery.household_type == 'Couple'" class="buyers flex gap-5 items-center flex-wrap">
                <div v-tooltip.top="'Please Click For Edit'" class="buyer-detail border-l border-[#596263]/50 pl-5" v-for="(buyer, index) in financial_discovery.buyers" :key="index" @click="editBuyer(financial_discovery.name)">
                    <div class="flex gap-[15px] mb-2">
                        <span v-if="buyer.first_name || buyer.surname" class="text-[18px] font-semibold">{{ buyer.first_name }} {{ buyer.surname }}</span>
                        <p>{{ buyer?.occupation != "" && buyer?.employment_type != "" ?
                            `${buyer.occupation} - ${buyer.employment_type}` :
                            buyer?.occupation != "" ? buyer?.occupation : buyer?.employment_type != "" ?
                                buyer?.employment_type : ""}}</p>
                    </div>
                    <div class="font-medium">{{ buyer?.age }} years old | {{ formatCurrency(buyer.gross_annual_income)}}</div>
                </div>
            </div>
        </div>
        <div v-tooltip.top="'Please Click For Edit'" class="other-content cursor-pointer" @click="editBuyer(financial_discovery.name)">
            <div class="goals-details flex lg:gap-10 gap-5 flex-wrap items-center">
                <div v-if="financial_discovery?.timeframe" class="detail">
                    <p class="text-[15px] mb-3">Timeframe</p>
                    <div class="text-[18px] font-medium">{{ financial_discovery?.timeframe ? financial_discovery.timeframe.toFixed(2) : '0' }} years</div>
                </div>
                <div v-if="financial_discovery.annual_income_goal" class="detail">
                    <p class="text-[15px] mb-3">Annual Income Goal</p>
                    <div class="text-[18px] font-medium">{{ formatCurrency(financial_discovery.annual_income_goal) }}</div>
                </div>
                <div v-if="financial_discovery.retirement_age_goal" class="detail">
                    <p class="text-[15px] mb-3">Retirement Goal</p>
                    <div class="text-[18px] font-medium">{{ financial_discovery.retirement_age_goal }} years</div>
                </div>
            </div>
        </div>
        <Dialog v-model:visible="buyerForm" modal header="Edit Buyer Details" contentClass="addbuyer-form"
            style="max-width: 500px; width: 100%;">
            <div class="fields">
                <div class="field">
                    <label for="firstname">First Name</label>
                    <InputText id="firstname" v-model="buyer.first_name" autocomplete="off" :invalid="isSubmitedForm && !buyer.first_name" />
                </div>
                <div class="field">
                    <label for="surname">Surname</label>
                    <InputText id="surname" v-model="buyer.surname" autocomplete="off" :invalid="isSubmitedForm && !buyer.surname" />
                </div>
                <div class="field">
                    <label for="date_of_birth">Date of Birth</label>
                    <DatePicker id="date_of_birth" v-model="buyer.date_of_birth" dateFormat="dd/mm/yy" :invalid="isSubmitedForm && buyer.date_of_birth == ''" />
                </div>
                <div class="field">
                    <label for="age">Age</label>
                    <InputText id="age" v-model="getAge" disabled autocomplete="off" />
                </div>
                <div class="field">
                    <label for="occupation">Occupation</label>
                    <InputText id="age" v-model="buyer.occupation" autocomplete="off" />
                </div>
                <div class="field">
                    <label for="employment_type">Employment Type</label>
                    <Select v-model="buyer.employment_type" :options="Occupations" optionLabel="label"
                        placeholder="Select Occupation" />
                </div>
                <div class="field">
                    <label for="length_of_employment_yrs">Length of Employment (yrs)</label>
                    <InputText id="length_of_employment_yrs" v-model="buyer.length_of_employment_yrs"
                        autocomplete="off" />
                </div>
                <div class="field">
                    <label for="gross_annual_income">Annual Income (incl. Super)</label>
                    <InputNumber v-model="buyer.gross_annual_income" inputId="gross_annual_income" mode="currency"
                        currency="USD" locale="en-US" :invalid="isSubmitedForm && !buyer.gross_annual_income || buyer.gross_annual_income == null" />
                </div>
                <div class="field">
                    <label for="untaxed_income">Untaxed Income</label>
                    <InputNumber v-model="buyer.untaxed_income" inputId="untaxed_income" mode="currency" currency="USD"
                        locale="en-US" />
                </div>
            </div>
            <div class="btns">
                <Button type="button" label="Cancel" severity="secondary" @click="buyerForm = false"></Button>
                <Button type="button" label="Update" @click="submit"></Button>
            </div>
        </Dialog>
    </div>
</template>
<script>
import { currencyFormat,fetch_api } from '@/utils'
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

export default {
    name: 'TopContent',
    components:{
        Dialog,
        Button,
    },
    data() {
        return {
            annualGrowth: 0,
            annualGrowthExist: false,
            owner_financial_discovery: "",
            buyerForm: false,
            isSubmitedForm: false,
            buyer: {
                name: '',
                first_name: '',
                surname: '',
                date_of_birth: '',
                age: '',
                occupation: '',
                length_of_employment_yrs: '',
                employment_type: '',
                gross_annual_income: 0,
                untaxed_income: 0,
            },
            Occupations: [
                { label: 'PAYG', value: 'PAYG' },
                { label: 'Self-Employed', value: 'Self-Employed' },
                { label: 'Retired', value: 'Retired' },
                { label: 'Unemployed', value: 'Unemployed' },
            ],
        }
    },
    watch: {
        'financial_discovery': function (data) {
            if (data) {
                let name = ""
                data?.buyers.forEach(element => {
                    if (name != "") name += ` and ${element.first_name} ${element.surname}`
                    else name += element.first_name + " " + element.surname
                });
                this.owner_financial_discovery = name;
                this.annualGrowth = data.assumed_annual_growth;      
                this.annualGrowthExist = false
            }
        },
        'annualGrowth': function (data) {
            if (data > 0 && data <= 100 && this.annualGrowthExist) {
                this.updateFDAnnualRate()
            }
            this.annualGrowthExist = true
        }
    },
    props: {
        financial_discovery: {
            type: [Object, Boolean],
            default: false
        }
    },
    computed: {
        single_buyer() {
            if(this.financial_discovery.household_type == 'Single'){
                return this.financial_discovery.buyers[0]
            }else{
                return false
            }
        },
        getAge() {
            if (this.buyer.date_of_birth) {
                const today = new Date();
                let birth_year = this.buyer.date_of_birth.getFullYear()
                const birthMonth = this.buyer.date_of_birth.getMonth();
                const birthDay = this.buyer.date_of_birth.getDate();

                let age = today.getFullYear() - birth_year;
                if (today.getMonth() < birthMonth || (today.getMonth() === birthMonth && today.getDate() < birthDay)) {
                    age--;
                }
                return age;
            }
            return 0
        }
    },
    methods: {
        formatCurrency(value) {
            return currencyFormat(value)
        },
        editBuyer(data) {
            // let employment_type = false
            // this.Occupations.forEach(item => {
            //     if (item.value === data.employment_type) employment_type = item
            // })
            // this.buyer = {
            //     ...data,
            //     date_of_birth: new Date(data.date_of_birth),
            //     employment_type: employment_type,
            //     name: data.buyer
            // }
            this.$router.push({name: "EditFD", params:{id: data}})
            // this.buyerForm = true
        },
        checkValidity() {
            let validate = true;
            let required = {
                name: '',
                first_name: '',
                surname: '',
                date_of_birth: '',
                gross_annual_income: 0
            }

            for (let key in required) {
                if (this.buyer[key] == null || this.buyer[key] == undefined || this.buyer[key] === "") {
                    validate = false
                }
                if (key == "gross_annual_income" && this.buyer[key] <= 0) {
                    validate = false
                }
            }

            return validate
        },
        async submit() {
            this.isSubmitedForm = true;
            if (this.checkValidity()) {
                let url = "/api/method/crm.financial_discovery.api.financial_discovery.updateBuyers"
                let res = await fetch_api(url, "POST", {
                    fdId: this.$route.params.id,
                    id: this.buyer.name,
                    data: {
                        ...this.buyer,
                        employment_type: this.buyer.employment_type?.value
                    },
                })
                if (res.message?.name) {
                    this.$emit('getFinancialDiscovery');
                    this.buyerForm = false
                    this.isSubmitedForm = false;
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Buyer update successfully.', life: 5000 });
                } else {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
                }
            }
        },
        async updateFDAnnualRate() {
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.updateAnnualGrowth"
            let res = await fetch_api(url, "POST", {
                id: this.$route.params.id,
                rate: this.annualGrowth
            })

            if (res.message?.name) {
                this.$emit('getFinancialDiscovery');
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Annual Growth update successfully.', life: 5000 });
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
    },
}
</script>

<style scoped>
.p-dialog .addbuyer-form .desc {
    margin-bottom: 15px;
}
.p-dialog .addbuyer-form .fields {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0px 20px;
    margin-bottom: 10px;
}
.p-dialog .addbuyer-form .field {
    margin-bottom: 10px;
}
.p-dialog .addbuyer-form input,
.p-dialog .addbuyer-form .p-datepicker,
.p-dialog .addbuyer-form .p-select,
.p-dialog .addbuyer-form .p-inputnumber {
    width: 100%;
}
.p-dialog .addbuyer-form .btns {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.buyer-detail{
    cursor: pointer;
}
</style>