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

        <div class="form hh_info-form mb-10">
          <h6 class="page-title mb-5">Household Information</h6>
          <div class="fields grid lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-y-[15px] gap-x-5">
            <div class="field">
              <label for="household_type text-red">Household Type</label>
              <Select v-model="hh_info.household_type" :options="hhtypes" optionLabel="label"
                placeholder="Select Household Type" :invalid="isSubmitedForm && !hh_info.household_type" />
            </div>
            <div class="field">
              <label for="dependant">{{ "Dependants (<18yr)" }}</label>
                  <Select v-model="hh_info.dependant" :options="dependant_option" optionLabel="label"
                    placeholder="Select Dependant" :invalid="isSubmitedForm && !hh_info.dependant" />
            </div>
            <div class="field">
              <label for="tenure_type">Tenure Type</label>
              <Select v-model="hh_info.tenure_type" :options="tenure_types" optionLabel="label"
                placeholder="Select Tenure Type" :invalid="isSubmitedForm && !hh_info.tenure_type" />
            </div>
            <div class="field">
              <label for="years_lived_in_current_address">Years lived in current address</label>
              <InputNumber :maxFractionDigits="0" v-model="hh_info.years_lived_in_current_address"
              :invalid="isSubmitedForm && !hh_info.years_lived_in_current_address && hh_info.years_lived_in_current_address == null" />
            </div>
          </div>
        </div>

        <!-- <Divider /> -->

        <div class="form buyer_info-form mb-10">
          <h6 class="page-title mb-5">Personal Information</h6>
          <div v-for="(buyer, index) in buyers" :key="index" :class="{ 'mb-4': buyers?.length > 1 }">
            <div class="form-title text-body font-medium mb-2.5 text-[16px]">
              Individual {{ index + 1 }} Information
            </div>
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
                <DatePicker id="date_of_birth" v-model="buyer.date_of_birth" dateFormat="yy-mm-dd" :maxDate="maxDate"
                :invalid="isSubmitedForm && buyer.date_of_birth == ''" />
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
                <Select v-model="buyer.employment_type" :options="employment_types" optionLabel="label"
                  placeholder="Select Employment Type" />
              </div>
              <div class="field">
                <label for="length_of_employment_yrs">Length of Employment (yrs)</label>
                <InputNumber :maxFractionDigits="0" id="length_of_employment_yrs"
                  v-model="buyer.length_of_employment_yrs" autocomplete="off" />
              </div>
              <div class="field">
                <label for="gross_annual_income">Annual Income (incl. Super)</label>
                <InputNumber :minFractionDigits="0" :maxFractionDigits="2" v-model="buyer.gross_annual_income"
                  inputId="gross_annual_income" mode="currency" currency="USD" locale="en-US"
                  :invalid="isSubmitedForm && !buyer.gross_annual_income" />
              </div>
              <div class="field">
                <label for="untaxed_income">Untaxed Income</label>
                <InputNumber :minFractionDigits="0" :maxFractionDigits="2" v-model="buyer.untaxed_income"
                  inputId="untaxed_income" mode="currency" currency="USD" locale="en-US" />
              </div>
            </div>
          </div>
        </div>
        <div class="form buyer_info-form mb-10">
          <h6 class="page-title mb-5">Passive Income Goal</h6>
          <div class="fields grid lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-y-[15px] gap-x-5">
            <div class="field">
              <label for="retirement_age_goal">Retirement Age Goal</label>
              <InputNumber :maxFractionDigits="0" v-model="hh_info.retirement_age_goal"
              :invalid="isSubmitedForm && !hh_info.retirement_age_goal" />
            </div>
            <div class="field">
              <label for="annual_income_goal">Annual Income Goal</label>
              <InputNumber :minFractionDigits="0" :maxFractionDigits="2" v-model="hh_info.annual_income_goal"
                inputId="annual_income_goal" mode="currency" currency="USD" locale="en-US"
                :invalid="isSubmitedForm && !hh_info.annual_income_goal" />
            </div>
            <div class="field">
              <label for="weekly_income_goal">Weekly Income Goal</label>
              <InputNumber :minFractionDigits="0" :maxFractionDigits="2" v-model="hh_info.weekly_income_goal"
                inputId="weekly_income_goal" mode="currency" currency="USD" locale="en-US" disabled />
            </div>
            <div class="field">
              <label for="timeframe">Timeframe</label>
              <InputNumber :maxFractionDigits="2" v-model="timeframe" inputId="timeframe" :invalid="isSubmitedForm && !timeframe" />
            </div>
          </div>
        </div>
        <div class="flex justify-between btn-submit text-center">
          <Button label="Back To List" severity="secondary"  icon="pi pi-arrow-left" iconPos="left"
              @click="$router.push({ name: 'FDList' })" raised />
          <Button label="Update" icon="pi pi-save" iconPos="right" size="large"
            @click="update" raised />
          <Button label="Back To Details" severity="secondary"  icon="pi pi-arrow-right" iconPos="right"
            @click="$router.push({ name: 'FDDetails', params: { id: $route.params.id } })" raised />
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import { currencyFormat,fetch_api } from '@/utils'
import Button from 'primevue/button';
import { useLoadingStore } from "@/stores/loading"; 

export default {
  name: "EditFD",
  components: {
        Button
    },
  data() {
    return {
      maxDate: new Date(),
      isSubmitedForm: false,
      financial_discovery: {},
      dealname:"",
      organization:"",
      hh_info: {
        household_type: { label: "Single", value: "Single" },
        dependant: { label: "No", value: "No" },
        tenure_type: "",
        years_lived_in_current_address: 0,
        retirement_age_goal: 0,
        annual_income_goal: 0,
        weekly_income_goal: 0,
      },
      buyers: [],
      dependant_option: [
        { label: "Yes", value: "Yes" },
        { label: "No", value: "No" },
      ],
      employment_types: [
        { label: "PAYG", value: "PAYG" },
        { label: "Self-Employed", value: "Self-Employed" },
        { label: "Retired", value: "Retired" },
        { label: "Unemployed", value: "Unemployed" },
      ],
      hhtypes: [
        { label: "Single", value: "Single" },
        { label: "Couple", value: "Couple" },
      ],
      tenure_types: [
        { label: "Renting", value: "Renting" },
        { label: "Owned with Mortgage", value: "Owned with Mortgage" },
        { label: "Owned Outright", value: "Owned Outright" },
      ],
    };
  },
  watch: {
    "hh_info.household_type": function (newType) {
      if (newType.value === "Couple" && this.buyers.length === 1) {
        this.buyers.push({
          first_name: "",
          surname: "",
          date_of_birth: "",
          age: "",
          occupation: "",
          length_of_employment_yrs: "",
          employment_type: "",
          gross_annual_income: 0,
          untaxed_income: 0,
        });
      } else if (newType.value !== "Couple" && this.buyers.length > 1) {
        this.buyers.splice(1);
      }
    },
    buyers: {
      deep: true,
      handler(newBuyers) {
        newBuyers.forEach((buyer, index) => {
          if (buyer.date_of_birth) {
            buyer.age = this.calculateAge(buyer.date_of_birth);
          }
        });
      },
    },
    "hh_info.annual_income_goal": function (data) {
      if (data != undefined && data != null && data > 0) {
        this.hh_info.weekly_income_goal = Math.round(data / 52);
      }
    },
  },
  computed: {
    timeframe() {
      if (this.hh_info.retirement_age_goal == "") {
        return "";
      } else if (this.buyers[0].date_of_birth == "") {
        return 0;
      } else {
        const birthdate = new Date(this.buyers[0].date_of_birth);
        const today = new Date();
        const birthDateMillis = new Date(this.buyers[0].date_of_birth).getTime();
        const todayMillis = today.getTime();
        const differenceMillis = todayMillis - birthDateMillis;
        const differenceDays = differenceMillis / (1000 * 60 * 60 * 24 * 365);
        let timeframe = this.hh_info.retirement_age_goal - differenceDays;
        return timeframe < 0 ? 0 : timeframe;
      }
    },
  },
  methods: {
    checkValidity() {
      let validate = true;
      let required = {
        household_type: "",
        dependant: 0,
        tenure_type: "",
        years_lived_in_current_address: 0,
        retirement_age_goal: 0,
        annual_income_goal: 0,
      };
      let requiredBuyer = {
        first_name: "",
        surname: "",
        date_of_birth: "",
        gross_annual_income: 0,
      };

      if (
        this.timeframe == null ||
        this.timeframe == undefined ||
        this.timeframe === ""
      ) {
        validate = false;
      }

      for (let key in required) {
        if (
          this.hh_info[key] == null ||
          this.hh_info[key] == undefined ||
          this.hh_info[key] === ""
        ) {
          validate = false;
        }
        if (key == "annual_income_goal" && this.hh_info[key] <= 0) {
          validate = false;
        }
        if (key == "retirement_age_goal" && this.hh_info[key] <= 0) {
          validate = false;
        }
      }

      for (let key in requiredBuyer) {
        if (
          this.buyers[0][key] == null ||
          this.buyers[0][key] == undefined ||
          this.buyers[0][key] === "" ||
          !this.buyers[0][key]
        ) {
          validate = false;
        }
        if (this.hh_info.household_type?.value == "Couple") {
          if (
            this.buyers[1][key] == null ||
            this.buyers[1][key] == undefined ||
            this.buyers[1][key] === "" ||
            !this.buyers[1][key]
          ) {
            validate = false;
          }
        }
      }
      return validate;
    },
    async update() {
      this.isSubmitedForm = true;
      if (this.checkValidity()) {
        let url = "/api/method/crm.financial_discovery.api.financial_discovery.update_financial_discovery"
        let res = await fetch_api(url, "POST", {
          id: this.$route.params.id,
          data: {
            ...this.hh_info,
            timeframe: this.timeframe,
            dependant: this.hh_info.dependant?.value,
            household_type: this.hh_info.household_type?.value,
            tenure_type: this.hh_info.tenure_type?.value,
          },
          buyers: this.buyers.map(item => {
            return {
              ...item,
              employment_type: item.employment_type?.value
            }
          }),
        })
        if (res.message?.name) {
          this.$router.push({ name: "FDDetails", params: { id: res.message?.name } })
          this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Financial Discovery updated successfully.', life: 5000 });
        } else {
          this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
        }
      }
    },
    async get_fdDetails() {
      const loadingStore = useLoadingStore();
      loadingStore.setLoading(true);

      let params = {
        id: this.$route.params.id,
      };
      let url = "/api/method/crm.financial_discovery.api.financial_discovery.get_financial_discovery";
      let res = await fetch_api(url, "POST", params);
      if (res?.message?.financial_discovery) {
        this.financial_discovery = res.message.financial_discovery;
        this.hh_info.household_type = {
          label: this.financial_discovery.household_type,
          value: this.financial_discovery.household_type,
        };
        this.hh_info.dependant = {
          label: this.financial_discovery.dependant,
          value: this.financial_discovery.dependant,
        };
        this.hh_info.tenure_type = {
          label: this.financial_discovery.tenure_type,
          value: this.financial_discovery.tenure_type,
        };
        this.hh_info.years_lived_in_current_address = this.financial_discovery.years_lived_in_current_address;
        this.hh_info.retirement_age_goal = this.financial_discovery.retirement_age_goal;
        this.hh_info.annual_income_goal = this.financial_discovery.annual_income_goal;
        this.buyers = this.financial_discovery.buyers.map((item) => {
          item.employment_type = {
            label: item.employment_type,
            value: item.employment_type,
          };
          return item;
        });
        this.dealname = res.message.financial_discovery?.crm_deal || '';
        this.organization = res.message.financial_discovery?.crm_organization || '';
      }else {
        this.$toast.add({ severity: 'error', summary: 'Error', detail: "Financial Discovery Not Found", life: 5000 });
        this.$router.push({ name: "CreateFD" })
      }
      loadingStore.setLoading(false);
    },
    calculateAge(date_of_birth) {
      const birthDate = new Date(date_of_birth);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      return age;
    },
  },
  async mounted() {
    await this.get_fdDetails();
  },
};
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
</style>
