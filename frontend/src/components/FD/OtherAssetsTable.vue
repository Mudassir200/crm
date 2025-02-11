<template>
    <div class="other_assets">
        <div class="other_assets-header">
            <h6 class="title">Other Assets</h6>
            <Button label="Add Other Assets" outlined icon="pi pi-plus" iconPos="left" size="small"
                @click="createNew"></Button>
        </div>
        <div class="asset_details">
            <DataTable v-model:editingRows="editingRows" :value="all_assets" showGridlines size="small" editMode="row"
                dataKey="name">
                <Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header" :bodyClass="isNumberField(col.field) ? 'text-right' : ''" style="width: 280px">
                    <template #body="{ data, field }">
                        {{
                            isNumberField(field) ? formatCurrency(data[field]) : data[field]
                        }}
                    </template>
                    <template #editor="{ data, field }">
                        <template v-if="isNumberField(field)">
                            <InputNumber v-model="data[field]" mode="currency" currency="USD" locale="en-US" autofocus
                                 :minFractionDigits="0" :maxFractionDigits="2" :invalid="col.required && submitForm && !data[field] && data[field] != 0" />
                        </template>
                        <template v-else-if="isSelectField(field)">
                            <Select name="investor" v-model="investor" :options="fd_investors" optionLabel="label"
                                placeholder="Select Investor" :invalid="col.required && submitForm && !investor" />
                        </template>
                        <template v-else>
                            <InputText v-model="data[field]" autofocus :invalid="col.required && submitForm && !data[field]" />
                        </template>
                    </template>
                </Column>
                <Column header="Actions" bodyClass="min-w-[100px] w-[100px]">
                    <template #body="{ data }">
                        <div v-if="data.name == 'combined'">
                            <span style="display: none;">No Action</span>
                        </div>
                        <div v-else-if="isRowEditing(data)" class="flex flex-wrap justify-center gap-2">
                            <i class="pi pi-check cursor-pointer" @click="onRowEditSave(data)" v-tooltip.top="'Save'" style="font-size: 20px;"></i>
                            <i class="pi pi-times text-red-500 cursor-pointer" @click="onRowEdit" v-tooltip.top="'Cancel'" style="font-size: 20px;"></i>
                            <!-- <Button icon="pi pi-check" aria-label="Save" severity="secondary" raised
                                @click="onRowEditSave(data)" v-tooltip.top="'Save'" />
                            <Button icon="pi pi-times" aria-label="Cancel" severity="danger" raised
                                @click="onRowEdit" v-tooltip.top="'Cancel'" /> -->
                        </div>
                        <div v-else class="flex flex-wrap justify-center gap-2">
                            <i class="pi pi-pencil cursor-pointer" @click="onRowEdit(data)" v-tooltip.top="'Edit'" style="font-size: 20px;"></i>
                            <i class="pi pi-trash text-red-500 cursor-pointer" @click="onRowDelete(data)" v-tooltip.top="'Delete'" style="font-size: 20px;"></i>
                            <!-- <Button icon="pi pi-pencil" aria-label="Edit" severity="secondary" raised
                                @click="onRowEdit(data)" v-tooltip.top="'Edit'" />
                            <Button icon="pi pi-trash" aria-label="Delete" severity="danger" raised
                                @click="onRowDelete(data)" v-tooltip.top="'Delete'" /> -->
                        </div>
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>
</template>
<script>
import { currencyFormat,fetch_api } from '@/utils'
import Button from 'primevue/button';

export default {
    name: "OtherAssetsTable",
    components: {
        Button
    },
    data() {
        return {
            submitForm: false,
            all_assets: [],
            editingRows: [],
            columns: [
                { field: 'title', header: 'Investor', required: true },
                { field: 'cash_savings', header: 'Cash Savings', required: true },
                { field: 'superannuation', header: 'Superannuation', required: false },
                { field: 'shares_equities', header: 'Shares & Equities', required: false },
                { field: 'weekly_savings_capacity', header: 'Weekly Savings Capacity', required: false },
                { field: 'extra_yearly_contributions', header: 'Extra Yearly Contributions', required: false },
            ],
            investor: "",
            fd_investors: [],
        }
    },
    watch: {
        'other_assets': async function (data) {
            this.formateOtherAssets(data)
        },
        'investors': async function (investors) {
            this.fd_investors = [];
            investors.forEach(investor => {
                this.fd_investors.push({
                    "value": investor.buyer,
                    "label": investor.first_name + " " + investor.surname
                })
            });
        }
    },
    methods: {
        formateOtherAssets(data) {
            this.all_assets = []
            data.forEach((element, index) => {
                this.all_assets.push({
                    "title": element.first_name + " " + element.surname,
                    ...element
                })
            });
            if (this.other_assets.length >= 2) {
                this.all_assets.push({
                    "name": "combined",
                    "title": "Combined",
                    "cash_savings": this.combined(this.all_assets, "cash_savings"),
                    "superannuation": this.combined(this.all_assets, "superannuation"),
                    "shares_equities": this.combined(this.all_assets, "shares_equities"),
                    "weekly_savings_capacity": this.combined(this.all_assets, "weekly_savings_capacity"),
                    "extra_yearly_contributions": this.combined(this.all_assets, "extra_yearly_contributions"),
                })                
            }
        },
        isNumberField(field) {
            if (field == 'cash_savings' || field == 'superannuation' || field == 'shares_equities' || field == 'weekly_savings_capacity' || field == "extra_yearly_contributions") {
                return true;
            } else {
                return false
            }
        },
        isSelectField(field) {
            if (field == 'title') {
                return true;
            } else {
                return false
            }
        },
        isRowEditing(row) {
            return this.editingRows.find(item => item.name === row.name);
        },
        onRowEdit(row = false) {
            if (row) {
                this.editingRows = [row]
                if (row?.new != true) {
                    this.fd_investors.find(item => {
                        item.value === row.investor ? this.investor = item : false
                    });
                } else {
                    this.investor = ""
                }
            } else {
                this.editingRows = []
                this.investor = ""
            }
        },
        onRowEditSave(event) {
            if (event.new) this.createOtherAssets(event)
            else this.updateOtherAssets(event)
        },
        createNew() {
            let newData = {
                name: this.generateUniqueId(),
                title: "",
                new: true,
                cash_savings: 0,
                superannuation: 0,
                shares_equities: 0,
                weekly_savings_capacity: 0,
                extra_yearly_contributions: 0,
            }
            this.formateOtherAssets([...this.other_assets, newData])
            this.editingRows = [];
            this.editingRows = [newData];
            this.investor = ""
        },
        confirmDelete(rowData) {
            this.$confirm.require({
                message: `Are you sure you want to delete this FD Other Assets?`,
                header: 'Confirm Deletion',
                icon: 'pi pi-exclamation-triangle',
                accept: () => {
                    this.deleteOtherAssets(rowData);
                },
            });
        },
        onRowDelete(event) {
            if (event.new == true) {
                this.$emit('getOtherAssets');
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
        combined(arr = [], key) {
            return arr.reduce((total, item) => item[key] + total, 0);
        },
        checkValidity(data) {
            let validate = true;
            let required = {
                cash_savings: 0
            };
            if (this.investor == null || this.investor == undefined || this.investor === "") {
                validate = false
            }
            for (let key in required) {
                if (data[key] == null || data[key] == undefined || data[key] === "") {
                    validate = false
                }
            }
            return validate
        },
        async createOtherAssets(data) {
            this.submitForm = true
            if (this.checkValidity(data)) {
                let params = {
                    id: this.$route.params.id,
                    investor: this.investor.value,
                    data: {
                        ...data
                    }
                }
                let url = "/api/method/crm.financial_discovery.api.financial_discovery.create_other_assets"
                let res = await fetch_api(url, "POST", params);
                if (res.message?.name) {
                    this.editingRows = [];
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Other Real Estate Asset created successfully.', life: 5000 });
                    this.submitForm = false
                    this.$emit('getFinancialDiscovery');
                } else {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
                }
            } 
        },
        async updateOtherAssets(data) {
            this.submitForm = true
            if (data?.name && data.name != undefined && data.name != null && this.checkValidity(data)) {
                let params = {
                    id: data.name,
                    investor: this.investor.value,
                    data: {
                        ...data
                    }
                }
                let url = "/api/method/crm.financial_discovery.api.financial_discovery.update_other_assets"
                let res = await fetch_api(url, "POST", params);
                if (res.message?.name) {
                    this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Other Assets updated successfully.', life: 5000 });
                    this.editingRows = []
                    this.submitForm = false
                    this.$emit('getFinancialDiscovery');
                } else {
                    this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
                }
            } 
        },
        async deleteOtherAssets(data) {
            let params = {
                id: data.name,
            }
            let url = "/api/method/crm.financial_discovery.api.financial_discovery.delete_other_assets"
            let res = await fetch_api(url, "POST", params);
            if (res.message) {
                this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Other Assets deleted successfully.', life: 5000 });
                this.$emit('getFinancialDiscovery');
            } else {
                this.$toast.add({ severity: 'error', summary: 'Error', detail: res.message, life: 5000 });
            }
        },
    },
    props: {
        other_assets: Array,
        investors: Array
    },
}
</script>


<style>
.other_assets input {
    width: 100px;
    padding: 6px 8px;
   /* border: 0px; */
    box-shadow: none;
    font-size: 14px;
    border-radius: 0px;
}
.other_assets .p-select {
    /* border: 0px; */
    box-shadow: none;
    width: 100%;
    border-radius: 0px;
}
.other_assets .p-inputnumber {
    height: 35px;
}
.other_assets .p-select .p-select-label {
    padding: 6px 8px;
}
.p-datatable-tbody > tr > td.text-right {
    text-align: right;
}
.p-datatable .p-datatable-tbody > tr > td[data-p-cell-editing="true"] {
    padding: 0!important;
}

.other_assets .other_assets-header {
    display: flex;
    gap: 20px;
    /* justify-content: space-between; */
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
}
/* .other_assets .asset_details {
    display: flex;
    gap: 20px;
    align-items: baseline;
}
.other_assets .asset_details .p-datatable {
    flex-grow: 1;
}
.other_assets .asset_details .extra_detail {
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 10px;
} */

/* Prime dialog css for Add Buyer */
.p-dialog .other_assets_form .fields {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0px 20px;
    margin-bottom: 10px;
}
.p-dialog .other_assets_form .field {
    margin-bottom: 10px;
}
.p-dialog .other_assets_form input,
.p-dialog .other_assets_form .p-datepicker,
.p-dialog .other_assets_form .p-select,
.p-dialog .other_assets_form .p-inputnumber {
    width: 100%;
}
.p-dialog .other_assets_form .btns {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
</style>