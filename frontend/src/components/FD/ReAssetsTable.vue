<template>
    <div class="re_assets">
        <div class="re_assets-header">
            <h6 class="title">Real Estate Assets</h6>
            <Button label="Add Real Estate Assets" outlined icon="pi pi-plus" iconPos="left" size="small"
                @click="createNew"></Button>
        </div>
        <DataTable scrollable v-model:editingRows="editingRows" :value="re_estate_assets" showGridlines size="small"
            editMode="row" dataKey="name">
            <Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header"
                :bodyClass="fieldType(col.field) == 'currency' ? 'text-right' : ''" style="width: 120px; max-width: 120px;">
                <template #body="{ data, field }">
                    {{
                        fieldType(field) == "currency" ? formatCurrency(data[field]) :
                            fieldType(field) == "rate" ? data[field] + "%" : data[field]
                    }}
                </template>
                <template #editor="{ data, field }">
                    <template v-if="field == 'weekly_rent_income'">
                        <InputNumber :minFractionDigits="0" :maxFractionDigits="2" v-if="weekly_rent_income_show"
                            v-model="data[field]" mode="currency" currency="USD" locale="en-US" autofocus
                            :invalid="col.required && submitForm && (data[field] == null || data[field] < 0)" />
                        <div v-else>-</div>
                    </template>
                    <template v-else-if="fieldType(field) == 'currency'">
                        <InputNumber :minFractionDigits="0" :maxFractionDigits="2"
                            v-model="data[field]" mode="currency" currency="USD" locale="en-US" autofocus
                            :invalid="col.required && submitForm && (data[field] == null || data[field] < 0)" />
                    </template>
                    <template v-else-if="fieldType(field) == 'select'">
                        <Select v-if="field == 'type'" v-model="select.type" :options="assets_types" optionLabel="label"
                            placeholder="Select Real Estate Type" :invalid="col.required && submitForm && !select.type" />
                        <Select v-else-if="field == 'ownership_type'" v-model="select.ownership_type"
                            :options="ownership_types" optionLabel="label" placeholder="Select Ownership Type"
                            :invalid="col.required && submitForm && !select.ownership_type" />
                        <Select v-else-if="field == 'ownership_structure'" v-model="select.ownership_structure"
                            :options="ownership_structures" optionLabel="label" placeholder="Select Ownership Structure"
                            :invalid="col.required && submitForm && !select.ownership_structure" />
                        <Select v-else-if="field == 'p_io'" v-model="select.p_io" :options="p_i_or_io"
                            optionLabel="label" placeholder="Select P&I OR IO" />
                        <Select v-else-if="field == 'fixed_or_var'" v-model="select.fixed_or_var"
                            :options="fixed_or_var" optionLabel="label" placeholder="Select Fixed or Var" />
                    </template>
                    <template v-else-if="fieldType(field) == 'mask'">
                        <InputMask v-model="data[field]" mask="9999" placeholder="1990"
                        :invalid="col.required && submitForm && (!data[field] || data[field] > maxYear)" />
                    </template>
                    <template v-else-if="fieldType(field) == 'rate'">
                        <InputNumber :maxFractionDigits="2" v-model="data[field]" inputId="interest_rate" suffix="%"
                            :min="0" :max="100" :invalid="col.required && submitForm && (!data[field] && data[field] == null)" />
                    </template>
                    <template v-else>
                        <InputText v-model="data[field]" autofocus :invalid="col.required && submitForm && !data[field]" />
                    </template>
                </template>
            </Column>
            <Column frozen alignFrozen="right" header="Actions" bodyClass="min-w-[100px] w-[100px]">
                <template #body="{ data }">
                    <div v-if="data.name == 'combined'">
                        <Button style="display: none;" />
                    </div>
                    <div v-else-if="isRowEditing(data)" class="flex flex-wrap justify-center gap-2">
                        <i class="pi pi-check cursor-pointer" @click="onRowEditSave(data)" v-tooltip.top="'Save'"
                            style="font-size: 20px;"></i>
                        <i class="pi pi-times text-red-500 cursor-pointer" @click="onRowEdit" v-tooltip.top="'Cancel'"
                            style="font-size: 20px;"></i>
                        <!-- <Button icon="pi pi-check" aria-label="Save" severity="secondary" raised
                            @click="onRowEditSave(data)" v-tooltip.top="'Save'" />
                        <Button icon="pi pi-times" aria-label="Cancel" severity="danger" raised @click="onRowEdit"
                            v-tooltip.top="'Cancel'" /> -->
                    </div>
                    <div v-else class="flex flex-wrap justify-center gap-3">
                        <i class="pi pi-pencil cursor-pointer" @click="onRowEdit(data)" v-tooltip.top="'Edit'"
                            style="font-size: 20px;"></i>
                        <i class="pi pi-trash text-red-500 cursor-pointer" @click="onRowDelete(data)"
                            v-tooltip.top="'Delete'" style="font-size: 20px;"></i>
                        <!-- <Button icon="pi pi-pencil" aria-label="Edit" severity="secondary" text
                            @click="onRowEdit(data)" v-tooltip.top="'Edit'" />
                        <Button icon="pi pi-trash" aria-label="Delete" severity="danger" raised
                            @click="onRowDelete(data)" v-tooltip.top="'Delete'" /> -->
                    </div>
                </template>
            </Column>
        </DataTable>
    </div>
</template>
<script>
import { currencyFormat,fetch_api } from '@/utils'
import Button from 'primevue/button';

export default {
    name: "ReAssetsTable",
    components: {
        Button
    },
    data() {
        return {
            submitForm: false,
            re_estate_assets: [],
            editingRows: [],
            columns: [
                { field: 'type', header: 'Real Estate Assets', required: true },
                { field: 'location', header: 'Location', required: true },
                { field: 'current_value', header: 'Current Value', required: true },
                { field: 'purchase_price', header: 'Purchase Price', required: true },
                { field: 'year_aquired', header: 'Year Aquired', required: true },
                { field: 'ownership_type', header: 'Ownership Type', required: true },
                { field: 'ownership_structure', header: 'Ownership Structure', required: true },
                { field: 'weekly_rent_income', header: 'Weekly Rent Income', required: true },
                { field: 'loan_amount', header: 'Loan Amount', required: true },
                { field: 'lender', header: 'Lender', required: false },
                { field: 'interest_rate', header: 'Interest Rate', required: true },
                { field: 'p_io', header: 'P&IO or IO', required: false },
                { field: 'fixed_or_var', header: 'Fixed or Var', required: false },
                { field: 'monthly_repayment', header: 'Monthly Repayment', required: true },
            ],
            weekly_rent_income_show: true,
            maxYear: new Date().getFullYear(),
            select: {
                type: "",
                ownership_type: "",
                ownership_structure: "",
                p_io: "",
                fixed_or_var: "",
            },
            assets_types: [
                { label: "PPOR", value: "PPOR" },
                { label: "Investment", value: "Investment" },
                { label: "SMSF", value: "SMSF" }
            ],
            ownership_types: [
                { label: "Personal", value: "Personal" },
                { label: "Trust", value: "Trust" },
                { label: "SMSF", value: "SMSF" },
                { label: "Company", value: "Company" },
            ],
            ownership_structures: [
                { label: "Individual 1", value: "Individual 1" },
                { label: "Individual 2", value: "Individual 2" },
                { label: "Joint", value: "Joint" },
            ],
            p_i_or_io: [
                { label: "P&I", value: "P&I" },
                { label: "IO", value: "IO" },
            ],
            fixed_or_var: [
                { label: "Fixed", value: "Fixed" },
                { label: "Variable", value: "Variable" },
            ],
        }
    },
    watch: {
        'real_estate_assets': async function (data) {
            this.re_estate_assets = data
        },
        'select.type': async function (data) {
            console.log(data);
            if (data?.value == "PPOR") this.weekly_rent_income_show = false
            else this.weekly_rent_income_show = true
        },
    },
    methods: {
        fieldType(field) {
            if (["type", "ownership_type", "ownership_structure", "p_io", "fixed_or_var"].includes(field)) return "select"
            else if (["current_value", "purchase_price", "weekly_rent_income", "monthly_repayment", "loan_amount"].includes(field)) return "currency"
            else if (["location", "lender"].includes(field)) return "text"
            else if (["year_aquired"].includes(field)) return "mask"
            else if (["interest_rate"].includes(field)) return "rate"
            else false
        },
        isRowEditing(row) {
            return this.editingRows.find(item => item.name === row.name);
        },
        onRowEdit(row = false) {
            if (row) {
                this.editingRows = [row]
                if (row?.new != true) {
                    this.assets_types.find(item => {
                        item.value === row.type ? this.select.type = item : false
                    });
                    this.ownership_types.find(item => {
                        item.value === row.ownership_type ? this.select.ownership_type = item : false
                    });
                    this.ownership_structures.find(item => {
                        item.value === row.ownership_structure ? this.select.ownership_structure = item : false
                    });
                    this.p_i_or_io.find(item => {
                        item.value === row.p_io ? this.select.p_io = item : false
                    });
                    this.fixed_or_var.find(item => {
                        item.value === row.fixed_or_var ? this.select.fixed_or_var = item : false
                    });
                } else {
                    for (let key in this.select) {
                        this.select[key] = ""
                    }
                }
            } else {
                this.editingRows = []
                for (let key in this.select) {
                    this.select[key] = ""
                }
            }
        },
        onRowEditSave(event) {
            if (event.new) this.createRealEstateAsset(event)
            else this.updateRealEstateAsset(event)
        },
        createNew() {
            let newData = {
                name: this.generateUniqueId(),
                new: true,
                type: "",
                location: "",
                current_value: 0,
                purchase_price: 0,
                year_aquired: "",
                ownership_type: "",
                ownership_structure: "",
                weekly_rent_income: 0,
                loan_amount: 0,
                lender: "",
                interest_rate: 0,
                p_io: "",
                fixed_or_var: "",
                monthly_repayment: 0
            }
            this.re_estate_assets = [...this.real_estate_assets, newData]
            this.editingRows = [];
            this.editingRows = [newData];
            for (let key in this.select) {
                this.select[key] = ""
            }
        },
        confirmDelete(rowData) {
            this.$confirm.require({
                message: `Are you sure you want to delete this FD Real Estate Assets?`,
                header: 'Confirm Deletion',
                icon: 'pi pi-exclamation-triangle',
                accept: () => {
                    this.deleteRealEstateAsset(rowData);
                },
            });
        },
        onRowDelete(event) {
            if (event.new == true) {
                this.$emit('getRealEstateAssets');
            } else {
                this.confirmDelete(event)
            }
        },
        generateUniqueId() {
            return 'id-' + Date.now() + '-' + Math.floor(Math.random() * 10000);
        },
        formatCurrency(value) {
            return currencyFormat(value)
        },
        checkValidity(data) {
            let validate = true;
            let selectRequired = {
                type: "",
                ownership_type: "",
                ownership_structure: "",
            };
            let required = {
                location: "",
                current_value: 0,
                purchase_price: 0,
                year_aquired: "",
                loan_amount: 0,
                interest_rate: 0,
                monthly_repayment: 0
            };
            for (let key in selectRequired) {
                if (this.select[key] == null || this.select[key] == undefined || this.select[key] === "") {
                    console.log(this.select[key]);
                    validate = false
                }
            }
            for (let key in required) {
                if (data[key] == null || data[key] == undefined || data[key] === "") {
                    validate = false
                }
                if (key == "year_aquired" && data[key] > this.maxYear) validate = false
                if (key == "monthly_repayment" && data[key] < 0) validate = false
                if (key == "current_value" && data[key] < 0) validate = false
                if (key == "purchase_price" && data[key] < 0) validate = false
                if (key == "loan_amount" && data[key] < 0) validate = false
            }
            if (this.select.type?.value != "PPOR") {
                if (data['weekly_rent_income'] == null || data['weekly_rent_income'] == undefined || data['weekly_rent_income'] < 0) {
                    validate = false
                }
            }else{
                data['weekly_rent_income'] = 0
            }
            return validate
        },
        async createRealEstateAsset(data) {
            this.submitForm = true
            if (this.checkValidity(data)) {
                let params = {
                    id: this.$route.params.id,
                    data: {
                        ...data,
                        weekly_rent_income: this.select.type.value == "PPOR" ? 0 : data.weekly_rent_income,
                        type: this.select.type?.value,
                        ownership_type: this.select.ownership_type?.value,
                        ownership_structure: this.select.ownership_structure?.value,
                        p_io: this.select.p_io !== "" ? this.select.p_io.value : "",
                        fixed_or_var: this.select.fixed_or_var !== "" ? this.select.fixed_or_var.value : "",
                    }
                }
                let url = "/api/method/crm.financial_discovery.api.financial_discovery.create_real_estate_assets"
                let res = await fetch_api(url, "POST", params);

                if (res.message?.name) {
                    this.editingRows = [];
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Real Estate Asset created successfully.', life: 5000 });
                    this.$emit('getFinancialDiscovery');
                    this.submitForm = false
                } else {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
                }
            }
        },
        async updateRealEstateAsset(data) {
            this.submitForm = true
            if (data?.name && data.name != undefined && data.name != null && this.checkValidity(data)) {
                let params = {
                    id: data.name,
                    data: {
                        ...data,
                        weekly_rent_income: this.select.type.value == "PPOR" ? 0 : data.weekly_rent_income,
                        type: this.select.type?.value,
                        ownership_type: this.select.ownership_type?.value,
                        ownership_structure: this.select.ownership_structure?.value,
                        p_io: this.select.p_io !== "" ? this.select.p_io.value : "",
                        fixed_or_var: this.select.fixed_or_var !== "" ? this.select.fixed_or_var.value : "",
                    }
                }
                let url = "/api/method/crm.financial_discovery.api.financial_discovery.update_real_estate_assets"
                let res = await fetch_api(url, "POST", params);
                if (res.message?.name) {
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Real Estate Assets updated successfully.', life: 5000 });
                    this.editingRows = []
                    this.submitForm = false
                    this.$emit('getFinancialDiscovery');
                } else {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
                }
            }
        },
        async deleteRealEstateAsset(data) {
            let params = {
                id: data.name,
            }
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.delete_real_estate_assets"
            let res = await fetch_api(url, "POST", params);
            if (res.message) {
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Real Estate Assets deleted successfully.', life: 5000 });
                this.$emit('getFinancialDiscovery');
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
    },
    props: {
        real_estate_assets: Array,
    },
    mounted() {
        this.addEditingClass
    }
}
</script>

<style>
.re_assets input {
    width: 100%;
    padding: 6px 8px;
    /* border: 0px; */
    box-shadow: none;
    font-size: 14px;
    border-radius: 0px;
}

.re_assets .p-select {
    /* border: 0px; */
    box-shadow: none;
    width: 100%;
    border-radius: 0px;
}

.re_assets .p-inputnumber {
    height: 35px;
}

.re_assets .p-select .p-select-label {
    padding: 6px 8px;
}

.p-datatable-tbody>tr>td.text-right {
    text-align: right;
}

.p-datatable .p-datatable-tbody>tr>td[data-p-cell-editing="true"] {
    padding: 0 !important;
}
.re_assets .re_assets-header {
    display: flex;
    gap: 20px;
    /* justify-content: space-between; */
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
}

/* Prime dialog css for Add Buyer */
.p-dialog .re_assets_form .fields {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0px 20px;
    margin-bottom: 10px;
}
.p-dialog .re_assets_form .field {
    margin-bottom: 10px;
}
.p-dialog .re_assets_form input,
.p-dialog .re_assets_form .p-datepicker,
.p-dialog .re_assets_form .p-select,
.p-dialog .re_assets_form .p-inputnumber {
    width: 100%;
}
.p-dialog .re_assets_form .btns {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
</style>