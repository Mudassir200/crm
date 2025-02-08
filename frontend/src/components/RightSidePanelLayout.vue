<template>
  <div class="sections flex flex-col overflow-y-auto">
    <template v-for="(section, i) in _sections" :key="section.name">
      <div v-if="section.visible" class="section flex flex-col">
        <div v-if="i !== firstVisibleIndex()" class="w-full section-border h-px border-t" />
        <div class="p-1 sm:p-3">
          <Section labelClass="font-semibold" headerClass="h-8" :label="getSectionLabel(section)" :hideLabel="!section.label"
            :opened="section.opened">
            <template v-if="!preview" #actions>
              <div class="flex items-center">
                <div v-if="section.istable">
                  <Link value="" :doctype="section.source_doctype" @change="(e) => addAssociation(e, section)">
                  <template #target="{ togglePopover }">
                    <Button class="h-7 px-3" variant="ghost" icon="plus" @click="togglePopover()" />
                  </template>
                  </Link>
                </div>
                <Button v-if="section.showEditButton" variant="ghost" class="w-7 mr-2"
                  @click="showSidePanelModal = true">
                  <EditIcon class="h-4 w-4" />
                </Button>
              </div>
            </template>
            <slot v-bind="{ section }">
              <div :class="section.label.toLowerCase() + '-area'">
                <div v-if="section.data?.loading && section.data?.data?.length == 0"
                  class="flex min-h-20 flex-1 items-center justify-center gap-3 text-base text-ink-gray-4">
                  <LoadingIndicator class="h-4 w-4" />
                  <span>{{ __('Loading...') }}</span>
                </div>
                <div v-else-if="section.data?.data?.length" v-for="(object, i) in section.data.data" :key="object.name"
                  class="w-[100%] pl-1" :class="[i == 0 ? 'pt-1' : 'pt-0']">
                  <Section :opened="false">
                    <template #header="{ opened, toggle }">
                      <div class="flex flex-col cursor-pointer gap-2 text-base leading-5 text-ink-gray-7">
                        <template v-for="(field, i) in section.fields ?? []" :key="field?.name">
                          <div class="flex items-center gap-2"
                            v-if="object[field.fieldname] !== null && object[field.fieldname] !== '' && object[field.fieldname] !== undefined">
                            <div class="flex w-full cursor-pointer items-center justify-between gap-2"
                              v-if="field.fieldname == section.title_field">
                              <div class="truncate font-bold text-[#0091ae]"
                                @click="showAccordion(object, section.fields) ? toggle() : null">
                                {{ object[field.fieldname] }}
                              </div>
                              <div class="flex items-center">
                                <Dropdown v-if="section.istable" :options="otherOptions(object, section)">
                                  <Button icon="more-horizontal" class="text-ink-gray-5" variant="ghost" />
                                </Dropdown>
                                <Button variant="ghost" v-if="section?.route" @click="
                                  router.push({
                                    name: section.route,
                                    params: { name: object[field.fieldname] },
                                  })
                                  ">
                                  <ArrowUpRightIcon class="h-4 w-4" />
                                </Button>
                              </div>
                            </div>
                            <div v-else class="truncate">
                              {{ object[field.fieldname] }}
                            </div>
                          </div>
                        </template>
                      </div>
                    </template>
                    <template #footer>
                      <div v-if="i != section.data.data.length - 1"
                        class="mb-1 mt-2 border-t border-1 border-gray-300" />
                    </template>
                  </Section>
                </div>
                <div v-else class="flex ml-1 mt-2 items-center text-base text-ink-gray-5">
                  {{ __(section?.empty_message || "No Data Available") }}
                </div>
              </div>
            </slot>
          </Section>
        </div>
        <div class="w-full section-border h-px border-t" />
      </div>
    </template>
  </div>
  <SidePanelModal v-if="showSidePanelModal" v-model="showSidePanelModal" type="Right Side Panel" :doctype="doctype"
    @reload="() => emit('reload')" />
</template>

<script setup>
import Section from '@/components/Section.vue'
import ArrowUpRightIcon from '@/components/Icons/ArrowUpRightIcon.vue'
import EditIcon from '@/components/Icons/EditIcon.vue'
import Link from '@/components/Controls/Link.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { createToast } from '@/utils'
import SidePanelModal from '@/components/Modals/SidePanelModal.vue'
import { createResource, Dropdown, call } from 'frappe-ui'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const props = defineProps({
  objectId: {
    type: String,
    required: true,
  },
  sections: {
    type: Object,
  },
  doctype: {
    type: String,
    default: 'CRM Lead',
  },
  preview: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update', 'reload'])

const showSidePanelModal = ref(false)

const _sections = ref([])

watch([() => props.sections, () => props.doctype, () => props.objectId], () => {
  if (!props.sections?.length) {
    _sections.value = []
    return
  }

  _sections.value = props.sections.map((section) => {
    if (section.data !== false) return section
    let params = {
      dt: props.doctype,
      name: props.objectId,
      field: section.reference_field,
      source_doctype: section.source_doctype,
      istable: section.istable,
      target_field: section?.target_field,
      selected_fields: ["name", section.title_field, ...section?.selected_fields]
    }

    return {
      ...section,
      data: createResource({
        url: 'crm.api.utils.get_association_list',
        params: params,
        cache: [props.doctype, section.target_doctype, props.objectId],
        auto: true
      })
    }
  })
}, { immediate: true })


async function addAssociation(value, section) {
  if (!value) return
  if (section.data.data?.find((c) => c[section.target_field] === value)) {
    createToast({
      title: __('Association already exist!'),
      icon: 'x',
      iconClasses: 'text-ink-red-3',
    })
    return
  }
  let d = await call('crm.api.utils.add_association', {
    dt: props.doctype,
    name: props.objectId,
    field: section.reference_field,
    target_field: section.target_field,
    value: value
  })
  if (d) {
    section.data.reload()
    createToast({
      title: __(`${section.source_doctype} added`),
      icon: 'check',
      iconClasses: 'text-ink-green-3',
    })
  }
}

async function removeAssociation(value, section) {
  if (!value) return
  let d = await call('crm.api.utils.remove_association', {
    dt: props.doctype,
    name: props.objectId,
    field: section.reference_field,
    target_field: section.target_field,
    value: value
  })
  if (d) {
    section.data.reload()
    createToast({
      title: __(`${section.source_doctype} removed`),
      icon: 'check',
      iconClasses: 'text-ink-green-3',
    })
  }
}

function getSectionLabel(section) {
  if (section.istable) return `${section.label} (${section?.data?.data?.length})` 
  return section.label
}

function showAccordion(object, fields) {
  return fields.some((field) => !field.in_preview && field.in_list_view && object[field.fieldname])
}

function otherOptions(object, section) {
  let options = [
    {
      label: __('Remove'),
      icon: 'trash-2',
      onClick: () => removeAssociation(object.name, section),
    },
  ]

  return options
}

function firstVisibleIndex() {
  return _sections.value.findIndex((section) => section.visible)
}
</script>

<style scoped>
.form-control {
  margin: 2px;
}

:deep(.form-control input:not([type='checkbox'])),
:deep(.form-control select),
:deep(.form-control textarea),
:deep(.form-control button),
.dropdown-button {
  border-color: transparent;
  background: transparent;
}

:deep(.form-control button) {
  gap: 0;
}

:deep(.form-control [type='checkbox']) {
  margin-left: 9px;
  cursor: pointer;
}

:deep(.form-control button > div) {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.form-control button svg) {
  color: white;
  width: 0;
}

.sections .section .column {
  max-height: 300px;
}

.sections .section:last-of-type .column {
  max-height: none;
}
</style>
