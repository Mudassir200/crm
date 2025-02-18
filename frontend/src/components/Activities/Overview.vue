<template>
    <div class="mb-2">
        <div class="my-3 flex flex-col gap-3 items-center justify-between text-lg font-medium sm:mb-4">
            <div class="shadow-md mb-4 hover:shadow-lg transition-shadow duration-300 p-4 w-[100%]"
                v-for="section in resolvedOverviewValues" :key="section.name">
                <div v-if="section.visible">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="">{{ section.label }}</h2>
                        <Button v-if="section.editable && isManager() && !isMobileView" variant="subtle"
                            @click="showOverviewDataFieldsModal = true">
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
        <div class="my-3 shadow-md hover:shadow-lg transition-shadow duration-300">
            <div class="p-4">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold text-gray-800">{{ __("Financial Discovery") }}</h2>
                    <Button v-if="isManager() && !isMobileView" variant="subtle" @click="showFDDataFieldsModal = true">
                        <FeatherIcon name="settings" class="h-4 w-4" />
                    </Button>
                </div>
                <div class="grid grid-cols-1 gap-6 mb-1" v-if="financial_discovery?.data?.length > 0">
                    <div v-for="fd in financial_discovery.data" :key="fd.name"
                        class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold cursor-pointer hover:text-blue-600">
                                <span class="text-gray-800">{{ fd.fd_name }} </span>
                                <span class="text-gray-600"> ( {{ fd.household_type }} - {{ fd.tenure_type }} )</span>
                            </h3>
                            <Button variant="subtle"
                                @click.stop="router.push({ name: 'FDDetails', params: { id: fd.name } })">
                                <FeatherIcon name="arrow-right" class="h-4 w-4" />
                            </Button>
                        </div>
                        <div class="w-[100%]" :class="!section?.hideBorder ? 'border-b py-2' : ''"
                            v-for="section in fdSections" :key="section.name">
                            <div v-if="section.visible">
                                <div v-if="!section?.hideLabel" class="flex justify-between items-center mb-4">
                                    <h2 class="">{{ section.label }}</h2>
                                </div>
                                <div class="grid w-full gap-4"
                                    :style="`grid-template-columns: repeat(${section.columns.length}, minmax(0, 1fr));`">
                                    <div v-for="column in section.columns" :key="column.name" class="flex flex-col gap-4">
                                        <div v-for="field in column.fields" :key="field.title" class="flex flex-col gap-1">
                                            <div class="text-gray-600">{{ field.title }}</div>
                                            <div class="font-medium text-gray-800" v-if="field.options == 'Currency'">{{
                                                getFormattedCurrency(field.field,fd) }}</div>
                                            <div class="font-medium text-gray-800" v-else>{{ fd[field.field] }}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex flex-col justify-center p-10 w-[100%]" v-else>
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
        </div>
    </div>
    <OverviewFieldsModal v-if="showOverviewDataFieldsModal" v-model="showOverviewDataFieldsModal" :doctype="doctype"
        :fieldsDoctype="doctype" @reload="() => {
            tabs.reload()
            data.reload()
        }" />
    <OverviewFieldsModal v-if="showFDDataFieldsModal" v-model="showFDDataFieldsModal" :doctype="doctype"
        type="Financial Discovery" fieldsDoctype="FD Financial Discovery" @reload="() => {
            fdTabs.reload()
            financial_discovery.reload()
        }" />
</template>

<script setup>
import OverviewFieldsModal from '@/components/Modals/OverviewFieldsModal.vue'
import { usersStore } from '@/stores/users'
import { getMeta } from '@/stores/meta'
import { isMobileView } from '@/composables/settings'
import { createResource, createDocumentResource, call } from 'frappe-ui'
import { useRouter } from 'vue-router';
import { computed, ref, watchEffect,h } from 'vue';

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
const showOverviewDataFieldsModal = ref(false)
const showFDDataFieldsModal = ref(false)
const resolvedOverviewValues = ref([]);

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

const fdTabs = createResource({
    url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_overview_layout',
    cache: ['financial_discovery_sections', 'CRM Deal'],
    params: { doctype: 'CRM Deal', type: "Financial Discovery" },
    auto: true,
})


const data = createDocumentResource({
    doctype: props.doctype,
    name: props.docname
})

const sections = computed(() => tabs.data?.[0]?.sections || []);
const fdSections = computed(() => fdTabs.data?.[0]?.sections || []);

watchEffect(async () => {
    if (!sections.value) return;
    resolvedOverviewValues.value = await Promise.all(sections.value.map(async section => ({
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
    return field.fieldtype === "Currency" ? getFormattedCurrency(field.field, doc) : doc[field.field];
}

</script>
