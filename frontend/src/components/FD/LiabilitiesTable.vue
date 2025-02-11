<template>
  <div class="liabilities">
    <div class="liability_table">
      <div class="table-header">
        <h6 class="title">Liabilities</h6>
        <Button label="Add Liabilities" outlined icon="pi pi-plus" iconPos="left" size="small"
          @click="createNewLiability"></Button>
      </div>
      <DataTable scrollable v-model:editingRows="editingLiabilityRows" :value="re_liabilities" showGridlines
        size="small" editMode="row" dataKey="name">
        <Column v-for="col of liabilityColumns" :key="col.field" :field="col.field" :header="col.header"
          :bodyClass="isNumberField(col.field) ? 'text-right' : ''" style="width: 200px">
          <template #body="{ data, field }">
            {{
              isNumberField(field)
                ? formatCurrency(data[field])
                : field == "rate"
                  ? data[field] + "%"
                  : data[field]
            }}
          </template>
          <template #editor="{ data, field }">
            <template v-if="isNumberField(field)">
              <InputNumber v-model="data[field]" mode="currency" currency="USD" locale="en-US" autofocus
                :minFractionDigits="0" :maxFractionDigits="2" :invalid="col.required && submitForm && !data[field] && data[field] != 0" />
            </template>
            <template v-else-if="field == 'rate'">
              <InputNumber v-model="data[field]" inputId="rate" suffix="%" :min="0" :max="100" autofocus
                :maxFractionDigits="2" :invalid="col.required && submitForm && !data[field]" />
            </template>
            <template v-else-if="field == 'liability_name'">
              <Select v-model="liability_name" :options="liabilityTypes" optionLabel="label"
                placeholder="Select Liability" :invalid="submitForm && !liability_name" />
            </template>
            <template v-else>
              <InputText v-model="data[field]" autofocus :invalid="col.required && submitForm && !data[field]" />
            </template>
          </template>
        </Column>
        <Column frozen alignFrozen="right" bodyClass="min-w-[100px] w-[100px]" header="Actions">
          <template #body="{ data }">
            <div v-if="isLiabilityRowEditing(data)" class="flex flex-wrap justify-center gap-2">
              <i class="pi pi-check cursor-pointer" @click="onLiabilityRowEditSave(data)" v-tooltip.top="'Save'"
                style="font-size: 20px"></i>
              <i class="pi pi-times text-red-500 cursor-pointer" @click="editingLiabilityRows = []"
                v-tooltip.top="'Cancel'" style="font-size: 20px"></i>
            </div>
            <div v-else class="flex flex-wrap justify-center gap-2">
              <i class="pi pi-pencil cursor-pointer" @click="editLiabilityRow(data)" v-tooltip.top="'Edit'"
                style="font-size: 20px"></i>
              <i class="pi pi-trash text-red-500 cursor-pointer" @click="onLiabilityRowDelete(data)"
                v-tooltip.top="'Delete'" style="font-size: 20px"></i>
            </div>
          </template>
        </Column>
      </DataTable>
    </div>
    <div class="monthly_expenses">
      <div class="table-header">
        <h6 class="title">Monthly Expenses</h6>
        <Button label="Add Monthly Expenses" outlined icon="pi pi-plus" iconPos="left" size="small"
          @click="createNewExpense"></Button>
      </div>
      <DataTable v-model:editingRows="editingExpenseRows" :value="re_monthly_expenses" showGridlines size="small"
        editMode="row" dataKey="name">
        <Column v-for="col of expenseColumns" :key="col.field" :field="col.field" :header="col.header"
          style="width: 170px">
          <template #body="{ data, field }">
            {{
              isNumberField(field) ? formatCurrency(data[field])
                : field == "expense_name" ? data[field]
                  : data[field]
            }}
          </template>
          <template #editor="{ data, field }">
            <template v-if="isNumberField(field)">
              <InputNumber v-model="data[field]" mode="currency" currency="USD" locale="en-US" autofocus
                :minFractionDigits="0" :maxFractionDigits="2" :invalid="col.required && submitFormExpense && !data[field] && data[field] == null" />
            </template>
            <template v-else-if="field == 'expense_name'">
              <Select v-model="expense_name" :options="expensesTypes" optionLabel="label" placeholder="Select Expense"
                :invalid="submitFormExpense && !expense_name" />
            </template>
            <template v-else>
              <InputText v-model="data[field]" autofocus :invalid="col.required && submitFormExpense && !data[field]" />
            </template>
          </template>
        </Column>
        <Column bodyClass="min-w-[100px] w-[100px]" header="Actions">
          <template #body="{ data }">
            <div v-if="isExpenseRowEditing(data)" class="flex flex-wrap justify-center gap-2">
              <i class="pi pi-check cursor-pointer" @click="onExpenseRowEditSave(data)" v-tooltip.top="'Save'"
                style="font-size: 20px"></i>
              <i class="pi pi-times text-red-500 cursor-pointer" @click="editingExpenseRows = []"
                v-tooltip.top="'Cancel'" style="font-size: 20px"></i>
            </div>
            <div v-else class="flex flex-wrap justify-center gap-2">
              <i class="pi pi-pencil cursor-pointer" @click="editExpenseRow(data)" v-tooltip.top="'Edit'"
                style="font-size: 20px"></i>
              <i class="pi pi-trash text-red-500 cursor-pointer" @click="onExpenseRowDelete(data)"
                v-tooltip.top="'Delete'" style="font-size: 20px"></i>
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
  name: "LiebilitiesTable",
  components: { Button },
  data() {
    return {
      submitForm: false,
      submitFormExpense: false,
      editingLiabilityRows: [],
      editingExpenseRows: [],
      liability_name: "",
      expense_name: "",
      liabilityColumns: [
        { field: "liability_name", header: "Liability Name", required: true },
        { field: "limit", header: "Limit", required: false },
        { field: "owning", header: "Owning", required: true },
        { field: "lender", header: "Lender", required: true },
        { field: "rate", header: "Rate", required: false },
        {
          field: "monthly_repayment",
          header: "Monthly Repayment",
          required: false,
        },
      ],
      liabilityTypes: [
        { label: "Credit Card", value: "Credit Card" },
        { label: "Vehicle Loan", value: "Vehicle Loan" },
        { label: "Personal Loan", value: "Personal Loan" },
        { label: "Other Loan", value: "Other Loan" },
        { label: "HECS", value: "HECS" },
      ],
      expensesTypes: [
        { label: "Rent", value: "Rent" },
        { label: "Est. Living Expenses", value: "Est. Living Expenses" },
        {
          label: "Private Healthcare Insurance",
          value: "Private Healthcare Insurance",
        },
        {
          label: "Child Care/Private School",
          value: "Child Care/Private School",
        },
        { label: "Child Support", value: "Child Support" },
      ],
      expenseColumns: [
        { field: "expense_name", header: "Expense Name", required: true },
        { field: "amount", header: "Amount", required: true },
      ],
      re_liabilities: [],
      re_monthly_expenses: [],
    };
  },
  watch: {
    liabilities: function (data) {
      this.re_liabilities = data;
    },
    monthly_expenses: function (data) {
      this.re_monthly_expenses = data;
    },
  },
  methods: {
    isNumberField(field) {
      if (
        field == "limit" ||
        field == "owning" ||
        field == "monthly_repayment" ||
        field == "amount"
      ) {
        return true;
      } else {
        return false;
      }
    },
    isLiabilityRowEditing(row) {
      return this.editingLiabilityRows.find((item) => item.name === row.name);
    },
    editLiabilityRow(row) {
      this.editingLiabilityRows = [row];
      if (row?.new != true) {
        this.liabilityTypes.find((item) => {
          item.value === row.liability_name ? (this.liability_name = item) : false;
        });
      } else {
        this.liability_name = "";
      }
    },
    editExpenseRow(row) {
      this.editingExpenseRows = [row];
      if (row?.new != true) {
        this.expensesTypes.find((item) => {
          item.value === row.expense_name ? (this.expense_name = item) : false;
        });
      } else {
        this.expense_name = "";
      }
    },
    isExpenseRowEditing(row) {
      return this.editingExpenseRows.find((item) => item.name === row.name);
    },
    onLiabilityRowEditSave(event) {
      if (event.new) this.createLiabilities(event);
      else this.updateLiabilities(event);
    },
    onExpenseRowEditSave(event) {
      if (event.new) this.createExpense(event);
      else this.updateExpense(event);
    },
    confirmLiabilityDelete(rowData) {
      this.$confirm.require({
        message: `Are you sure you want to delete this FD Liability ${rowData.liability_name}?`,
        header: "Confirm Deletion",
        icon: "pi pi-exclamation-triangle",
        accept: () => {
          this.deleteLiabilities(rowData);
        },
      });
    },
    confirmExpenseDelete(rowData) {
      this.$confirm.require({
        message: `Are you sure you want to delete this FD Expense ${rowData.expense_name}?`,
        header: "Confirm Deletion",
        icon: "pi pi-exclamation-triangle",
        accept: () => {
          this.deleteExpense(rowData);
        },
      });
    },
    onLiabilityRowDelete(event) {
      if (event.new == true) {
        this.$emit("getLiabilities");
      } else {
        this.confirmLiabilityDelete(event);
      }
    },
    onExpenseRowDelete(event) {
      if (event.new == true) {
        this.$emit("getMonthlyExpenses");
      } else {
        this.confirmExpenseDelete(event);
      }
    },
    createNewLiability() {
      let newData = {
        name: this.generateUniqueId(),
        new: true,
        liability: "",
        limit: 0,
        owning: 0,
        lender: "",
        rate: 0,
        monthly_repayment: 0,
      };
      this.liability_name = "";
      this.re_liabilities = [...this.liabilities, newData];
      this.editingLiabilityRows = [];
      this.editingLiabilityRows = [newData];
    },
    createNewExpense() {
      let newData = {
        name: this.generateUniqueId(),
        new: true,
        expense_name: "",
        amount: 0,
      };
      this.expense_name = "";
      this.re_monthly_expenses = [...this.monthly_expenses, newData];
      this.editingExpenseRows = [];
      this.editingExpenseRows = [newData];
    },
    generateUniqueId() {
      return "id-" + Date.now() + "-" + Math.floor(Math.random() * 10000);
    },
    formatCurrency(value) {
      return currencyFormat(value);
    },
    checkLiabilitiesValidity(data) {
      let validate = true;
      let required = {
        owning: 0,
        lender: "",
      };
      for (let key in required) {
        if (data[key] == null || data[key] == undefined || data[key] === "") {
          validate = false;
        }
      }
      if (
        this.liability_name == null ||
        this.liability_name == undefined ||
        this.liability_name == ""
      ) {
        validate = false;
      }

      return validate;
    },
    checkExpenseValidity(data) {
      let validate = true;
      let required = {
        amount: 0,
      };
      for (let key in required) {
        if (data[key] == null || data[key] == undefined || data[key] === "") {
          validate = false;
        }
      }
      if (
        this.expense_name == null ||
        this.expense_name == undefined ||
        this.expense_name == ""
      ) {
        validate = false;
      }

      return validate;
    },
    async createLiabilities(data) {
      this.submitForm = true;
      if (this.checkLiabilitiesValidity(data)) {
        let params = {
          id: this.$route.params.id,
          data: {
            ...data,
            liability_name: this.liability_name?.value,
          },
        };
        let url =
          "/api/method/crm.financial_discovery.api.financial_discovery.create_liabilities";
        let res = await fetch_api(url, "POST", params);
        if (res.message?.name) {
          this.$toast.add({
            severity: "success",
            summary: "Success",
            detail: "Liability created successfully.",
            life: 5000,
          });
          this.editingLiabilityRows = [];
          this.submitForm = false;
          this.$emit("getFinancialDiscovery");
        } else {
          this.$toast.add({
            severity: "error",
            summary: "Error",
            detail: res.message,
            life: 5000,
          });
        }
      }
    },
    async updateLiabilities(data) {
      this.submitForm = true;
      if (
        data?.name &&
        data.name != undefined &&
        data.name != null &&
        this.checkLiabilitiesValidity(data)
      ) {
        let params = {
          id: data.name,
          data: {
            ...data,
            liability_name: this.liability_name?.value,
          },
        };
        let url =
          "/api/method/crm.financial_discovery.api.financial_discovery.edit_liabilities";
        let res = await fetch_api(url, "POST", params);
        if (res.message?.name) {
          this.$toast.add({
            severity: "success",
            summary: "Success",
            detail: "Liability updated successfully.",
            life: 5000,
          });
          this.editingLiabilityRows = [];
          this.submitForm = false;
          this.$emit("getFinancialDiscovery");
        } else {
          this.$toast.add({
            severity: "error",
            summary: "Error",
            detail: res.message,
            life: 5000,
          });
        }
      }
    },
    async deleteLiabilities(data) {
      let params = {
        id: data.name,
      };
      let url =
        "/api/method/crm.financial_discovery.api.financial_discovery.delete_liabilities";
      let res = await fetch_api(url, "POST", params);
      if (res.message) {
        this.$toast.add({
          severity: "success",
          summary: "Success",
          detail: "Liability deleted successfully.",
          life: 5000,
        });
        this.$emit("getFinancialDiscovery");
      } else {
        this.$toast.add({
          severity: "error",
          summary: "Error",
          detail: res.message,
          life: 5000,
        });
      }
    },
    async createExpense(data) {
      this.submitFormExpense = true;
      if (this.checkExpenseValidity(data)) {
        let params = {
          id: this.$route.params.id,
          data: {
            ...data,
            expense_name: this.expense_name?.value,
          },
        };
        let url =
          "/api/method/crm.financial_discovery.api.financial_discovery.create_monthly_expense";
        let res = await fetch_api(url, "POST", params);
        if (res.message?.name) {
          this.$toast.add({
            severity: "success",
            summary: "Success",
            detail: "Monthly Expense created successfully.",
            life: 5000,
          });
          this.editingExpenseRows = [];
          this.submitFormExpense = false;
          this.$emit("getFinancialDiscovery");
        } else {
          this.$toast.add({
            severity: "error",
            summary: "Error",
            detail: res.message,
            life: 5000,
          });
        }
      }
    },
    async updateExpense(data) {
      this.submitFormExpense = true;
      if (
        data?.name &&
        data.name != undefined &&
        data.name != null &&
        this.checkExpenseValidity(data)
      ) {
        let params = {
          id: data.name,
          data: {
            ...data,
            expense_name: this.expense_name?.value,
          },
        };
        let url =
          "/api/method/crm.financial_discovery.api.financial_discovery.update_monthly_expense";
        let res = await fetch_api(url, "POST", params);
        if (res.message?.name) {
          this.$toast.add({
            severity: "success",
            summary: "Success",
            detail: "FD Expense updated successfully.",
            life: 5000,
          });
          this.editingExpenseRows = [];
          this.submitFormExpense = false;
          this.$emit("getFinancialDiscovery");
        } else {
          this.$toast.add({
            severity: "error",
            summary: "Error",
            detail: res.message,
            life: 5000,
          });
        }
      }
    },
    async deleteExpense(data) {
      let params = {
        id: data.name,
      };
      let url =
        "/api/method/crm.financial_discovery.api.financial_discovery.delete_monthly_expense";
      let res = await fetch_api(url, "POST", params);
      if (res.message) {
        this.$toast.add({
          severity: "success",
          summary: "Success",
          detail: "FD Expense deleted successfully.",
          life: 5000,
        });
        this.$emit("getFinancialDiscovery");
      } else {
        this.$toast.add({
          severity: "error",
          summary: "Error",
          detail: res.message,
          life: 5000,
        });
      }
    },
  },
  props: {
    liabilities: Array,
    monthly_expenses: Array,
  },
};
</script>

<style>
.liabilities input {
  width: 100%;
  padding: 6px 8px;
  /* border: 0px; */
  box-shadow: none;
  font-size: 14px;
  border-radius: 0px;
}

.liabilities .p-select {
  /* border: 0px; */
  box-shadow: none;
  width: 100%;
  border-radius: 0px;
}

.liabilities .p-inputnumber {
  height: 35px;
}

.liabilities .p-select .p-select-label {
  padding: 6px 8px;
}

.p-datatable-tbody>tr>td.text-right {
  text-align: right;
}

.p-datatable .p-datatable-tbody>tr>td[data-p-cell-editing="true"] {
  padding: 0 !important;
}

.liabilities {
    display: flex;
    gap: 20px;
}
.liabilities .liability_table {
    width: 75%;
}
.liabilities .monthly_expenses {
    width: 25%;
}
.liabilities .table-header {
    display: flex;
    gap: 20px;
    /* justify-content: space-between; */
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 10px;
}

/* Prime dialog css for Add Buyer */
.p-dialog .liabilities_form .fields {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0px 20px;
    margin-bottom: 10px;
}
.p-dialog .liabilities_form .field {
    margin-bottom: 10px;
}
.p-dialog .liabilities_form input,
.p-dialog .liabilities_form .p-datepicker,
.p-dialog .liabilities_form .p-select,
.p-dialog .liabilities_form .p-inputnumber {
    width: 100%;
}
.p-dialog .liabilities_form .btns {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

/* Media query */
@media(max-width: 1600px){
    .liabilities .liability_table {
        width: 65%;
    }
    .liabilities .monthly_expenses {
        width: 35%;
    }
}
@media(max-width: 1280px){
    .liabilities .liability_table {
        width: 55%;
    }
    .liabilities .monthly_expenses {
        width: 45%;
    }
}
@media(max-width: 1024px){
    .liabilities{
        flex-direction: column;
        gap: 60px;
    }
    .liabilities .liability_table {
        width: 100%;
    }
    .liabilities .monthly_expenses {
        width: 100%;
    }
}
</style>
