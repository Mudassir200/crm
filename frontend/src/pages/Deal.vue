<template>
  <LayoutHeader v-if="deal.data">
    <template #left-header>
      <div class="flex items-center justify-between">
        <router-link class="text-xl flex items-center text-blue-700" :to="{ name: 'Deals',params: { viewType: route.query.viewType },
          query: { view: route.query.view } }">
          <span class="pi pi-angle-left" >
          </span>
          <span class="hover:underline">
            {{ __("Deals") }}
          </span>
        </router-link>
      </div>
    </template>
    <template #center-header>
      <Tabs as="div" v-model="tabIndex" :tabs="tabs">
      </Tabs>
    </template>
    <template #right-header>
      <CustomActions v-if="deal.data._customActions?.length" :actions="deal.data._customActions" />
    </template>
  </LayoutHeader>
  <div v-if="deal.data" class="flex h-full overflow-hidden">
    <Resizer side="left" class="flex flex-col justify-between border-r">
      <div class="flex items-center justify-start gap-5 border-b p-5">
        <Tooltip :text="__('Organization logo')">
          <div class="group relative size-12">
            <Avatar size="3xl" class="size-12" :label="organization.data?.name || __('Untitled')"
              :image="organization.data?.organization_logo" />
          </div>
        </Tooltip>
        <div class="flex flex-col gap-2.5 truncate text-ink-gray-9">
          <Tooltip :text="organization.data?.name || __('Set an organization')">
            <div class="truncate text-2xl font-medium">
              {{ organization.data?.name || __('Untitled') }}
            </div>
          </Tooltip>
          <div v-if="isManager() && deal?.data?.pipeline" class="field flex items-center gap-2 leading-5">
            <Tooltip :text="__('Stage')" :hoverDelay="1">
              <div class="shrink-0 truncate text-base text-ink-gray-8">
                {{ __('Stage:') }}
              </div>
            </Tooltip>
            <div class="flex items-center justify-between w-[65%]">
              <Link class="form-control select-text" 
                :value="deal.data.stage" doctype="CRM Stage"
                :dependsFilter="deal?.data?.pipeline ? { 'pipeline': deal.data.pipeline} : {}"
                @change="(data) => updateField('stage', data)" 
                />
            </div>
          </div>
          <div v-if="isManager()" class="field flex items-center gap-2 leading-5">
            <Tooltip :text="__('Pipeline')" :hoverDelay="1">
              <div class="shrink-0 truncate text-base text-ink-gray-8">
                {{ __('Pipeline:') }}
              </div>
            </Tooltip>
            <div class="w-[65%]">
              <Tooltip :text="__('Edit Pipeline')">
                <Button
                  variant="ghost"
                  class="w-100"
                  @click="showPipelineModal = true"
                >
                  <div class="flex items-center justify-between">
                    <span>{{ deal.data.pipeline }}</span>
                  </div>
                </Button>
              </Tooltip>
            </div>
          </div>
          <div class="flex gap-1.5">
            <Tooltip v-if="callEnabled" :text="__('Make a call')">
              <Button class="h-7 w-7" @click="triggerCall">
                <PhoneIcon class="h-4 w-4" />
              </Button>
            </Tooltip>
            <Tooltip :text="__('Send an email')">
              <Button class="h-7 w-7">
                <Email2Icon class="h-4 w-4" @click="
                  deal.data.email
                    ? openEmailBox()
                    : errorMessage(__('No email set'))
                  " />
              </Button>
            </Tooltip>
            <Tooltip :text="__('Go to website')">
              <Button class="h-7 w-7">
                <LinkIcon class="h-4 w-4" @click="
                  deal.data.website
                    ? openWebsite(deal.data.website)
                    : errorMessage(__('No website set'))
                  " />
              </Button>
            </Tooltip>
            <Tooltip :text="__('Attach a file')">
              <Button class="size-7" @click="showFilesUploader = true">
                <AttachmentIcon class="size-4" />
              </Button>
            </Tooltip>
          </div>
        </div>
      </div>
      <SLASection v-if="deal.data.sla_status" v-model="deal.data" @updateField="updateField" />
      <div v-if="leftSidePanelSections.data" class="flex flex-1 flex-col justify-between overflow-hidden">
        <LeftSidePanelLayout v-model="deal.data" :sections="leftSidePanelSections.data"
          doctype="CRM Deal" @update="updateField" @reload="leftSidePanelSections.reload">
        </LeftSidePanelLayout>
      </div>
    </Resizer>
    <Tabs as="div" v-model="tabIndex" :tabs="tabs">
      <Activities ref="activities" doctype="CRM Deal" :tabs="tabs" v-model:reload="reload" v-model:tabIndex="tabIndex"
        v-model="deal" />
    </Tabs>
    <Resizer side="right" class="flex flex-col justify-between border-l">
      <div v-if="rightSidePanelSections.data" class="flex flex-1 flex-col justify-between overflow-hidden">
        <RightSidePanelLayout :sections="rightSidePanelSections.data" 
          doctype="CRM Deal" @reload="rightSidePanelSections.reload" :objectId="props.dealId" >
        </RightSidePanelLayout>
      </div>
    </Resizer>
  </div>
  <div v-if="isDirty" class="p-4 flex gap-3 bottom-0 right-0" style="box-shadow: rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;">
    <Button variant="solid" @click="updateDealDetails('save')">
      {{ __('Save') }}
    </Button>
    <Button variant="outline" @click="updateDealDetails('discard')">
      {{ __('Discard') }}
    </Button>
  </div>
  <OrganizationModal v-model="showOrganizationModal" v-model:organization="_organization" :options="{
    redirect: false,
    afterInsert: (doc) => updateField('organization', doc.name),
  }" />
  <PipelineModal v-if="deal?.data" v-model="showPipelineModal" :data="deal.data"
    :onSave="(doc) => {
      updateField('pipeline', doc.pipeline, () => {
        deal.reload()
        updateField('stage', doc.stage)
      })
    }" />
  <FilesUploader v-if="deal.data?.name" v-model="showFilesUploader" doctype="CRM Deal" :docname="deal.data.name" @after="() => {
    activities?.all_activities?.reload()
    changeTabTo('attachments')
  }
    " />
</template>
<script setup>
import Resizer from '@/components/Resizer.vue'
import ActivityIcon from '@/components/Icons/ActivityIcon.vue'
import EmailIcon from '@/components/Icons/EmailIcon.vue'
import Email2Icon from '@/components/Icons/Email2Icon.vue'
import CommentIcon from '@/components/Icons/CommentIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import WhatsAppIcon from '@/components/Icons/WhatsAppIcon.vue'
import LinkIcon from '@/components/Icons/LinkIcon.vue'
import AttachmentIcon from '@/components/Icons/AttachmentIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Activities from '@/components/Activities/Activities.vue'
import OrganizationModal from '@/components/Modals/OrganizationModal.vue'
import Link from '@/components/Controls/Link.vue'
import FilesUploader from '@/components/FilesUploader/FilesUploader.vue'
import SLASection from '@/components/SLASection.vue'
import CustomActions from '@/components/CustomActions.vue'
import { usersStore } from '@/stores/users'

import {
  openWebsite,
  createToast,
  setupAssignees,
  setupCustomizations,
  errorMessage,
} from '@/utils'
import { getSettings } from '@/stores/settings'
import { globalStore } from '@/stores/global'
import { whatsappEnabled, callEnabled } from '@/composables/settings'
import {
  createResource,
  createDocumentResource,
  Tooltip,
  Avatar,
  Tabs,
  call,
  usePageMeta,
} from 'frappe-ui'

import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useActiveTabManager } from '@/composables/useActiveTabManager'
import LeftSidePanelLayout from '../components/LeftSidePanelLayout.vue'
import PipelineModal from '../components/Modals/PipelineModal.vue'
import RightSidePanelLayout from '../components/RightSidePanelLayout.vue'

const { brand } = getSettings()
const { $dialog, $socket, makeCall } = globalStore()
const { isManager } = usersStore()
const route = useRoute()
const router = useRouter()

const props = defineProps({
  dealId: {
    type: String,
    required: true,
  },
})

const showPipelineModal = ref(false)

const deal = createResource({
  url: 'crm.fcrm.doctype.crm_deal.api.get_deal',
  params: { name: props.dealId },
  cache: ['deal', props.dealId],
  onSuccess: (data) => {
    if (data.organization) {
      organization.update({
        params: { doctype: 'CRM Organization', name: data.organization },
      })
      organization.fetch()
    }

    setupAssignees(deal)
    setupCustomizations(deal, {
      doc: data,
      $dialog,
      $socket,
      router,
      updateField,
      createToast,
      deleteDoc: deleteDeal,
      resource: {
        deal,
        rightSidePanelSections,
        leftSidePanelSections
      },
      call,
    })
  },
})

const organization = createResource({
  url: 'frappe.client.get',
  onSuccess: (data) => (deal.data._organizationObj = data),
})

onMounted(() => {
  $socket.on('crm_customer_created', () => {
    createToast({
      title: __('Customer created successfully'),
      icon: 'check',
      iconClasses: 'text-ink-green-3',
    })
  })

  if (deal.data) {
    organization.data = deal.data._organizationObj
    return
  }
  deal.fetch()
})

onBeforeUnmount(() => {
  $socket.off('crm_customer_created')
})

const reload = ref(false)
const showOrganizationModal = ref(false)
const showFilesUploader = ref(false)
const _organization = ref({})


usePageMeta(() => {
  return {
    title: organization.data?.name || deal.data?.name,
    icon: brand.favicon,
  }
})

const tabs = computed(() => {
  let tabOptions = [
    {
      name: 'Overview',
      label: __('Overview'),
    },
    {
      name: 'Activity',
      label: __('Activity'),
      icon: ActivityIcon,
    },
    {
      name: 'Emails',
      label: __('Emails'),
      icon: EmailIcon,
    },
    {
      name: 'Comments',
      label: __('Comments'),
      icon: CommentIcon,
    },
    {
      name: 'Calls',
      label: __('Calls'),
      icon: PhoneIcon,
      condition: () => callEnabled.value,
    },
    {
      name: 'Tasks',
      label: __('Tasks'),
      icon: TaskIcon,
    },
    {
      name: 'Notes',
      label: __('Notes'),
      icon: NoteIcon,
    },
    {
      name: 'Attachments',
      label: __('Attachments'),
      icon: AttachmentIcon,
    },
    {
      name: 'WhatsApp',
      label: __('WhatsApp'),
      icon: WhatsAppIcon,
      condition: () => whatsappEnabled.value,
    },
  ]
  return tabOptions.filter((tab) => (tab.condition ? tab.condition() : true))
})

const { tabIndex } = useActiveTabManager(tabs, 'lastDealTab')

const rightSidePanelSections = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_right_sidepanel_sections',
  cache: ['rightSidePanelSections', 'CRM Deal'],
  params: { doctype: 'CRM Deal', type: "Right Side Panel" },
  auto: true,
  transform: (data) => data,
})

const leftSidePanelSections = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_sidepanel_sections',
  cache: ['leftSidePanelSections', 'CRM Deal'],
  params: { doctype: 'CRM Deal', type: "Left Side Panel" },
  auto: true,
  transform: (data) => getParsedSections(data),
})

// Add Condition For Showing Pipeline and Stage field 
function isFieldVisible(_sections,fieldName) {
  let show = false;
  _sections?.data?.forEach((section) => {
    section.columns[0].fields.forEach((field) => {
      if (field.fieldname == fieldName && field.visible) {
        show = true
      }
    })
  })
  return show
}

function getParsedSections(_sections) {
  _sections.forEach((section) => {
    section.columns[0].fields.forEach((field) => {
      if (field.fieldname == 'organization') {
        field.create = (value, close) => {
          _organization.value.organization_name = value
          showOrganizationModal.value = true
          close()
        }
        field.link = (org) =>
          router.push({
            name: 'Organization',
            params: { name: org },
          })
      }
    })
  })
  return _sections
}

const dealContacts = ref({})

function triggerCall() {
  let primaryContact = dealContacts.data?.find((c) => c.is_primary)
  let mobile_no = primaryContact.mobile_no || null

  if (!primaryContact) {
    errorMessage(__('No primary contact set'))
    return
  }

  if (!mobile_no) {
    errorMessage(__('No mobile number set'))
    return
  }

  makeCall(mobile_no)
}

const isDirty = computed(() => {
  return updateDealData.isDirty
})

const updateDealData = createDocumentResource({
    doctype: "CRM Deal",
    name: props.dealId,
    auto: true,
    setValue: {
      onSuccess: () => {
        updateDealData.reload()
        deal.reload()
        rightSidePanelSections.reload()
        reload.value = true
        createToast({
          title: 'Data Updated',
          icon: 'check',
          iconClasses: 'text-ink-green-3',
        })
      },
      onError: (err) => {
        createToast({
          title: 'Error',
          text: err.messages[0],
          icon: 'x',
          iconClasses: 'text-red-600',
        })
      },
    },
  })

function updateDealDetails(action){
  if(action === 'discard'){
    deal.reload()
    updateDealData.reload()
    return
  }
  updateDealData.save.submit()
}


function updateField(name, value, callback) {
  deal.data[name] = value
  updateDealData.doc[name] = value
  updateDealData.isDirty = true
}

async function deleteDeal(name) {
  await call('frappe.client.delete', {
    doctype: 'CRM Deal',
    name,
  })
  router.push({ name: 'Deals' })
}

const activities = ref(null)

function openEmailBox() {
  activities.value.emailBox.show = true
}
</script>
