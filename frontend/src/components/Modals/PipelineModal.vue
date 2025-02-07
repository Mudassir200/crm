<template>
  <Dialog v-model="show" :options="{ size: 'md' }">
    <template #body>
      <div class="bg-surface-modal px-4 pb-6 pt-5 sm:px-6">
        <div class="mb-5 flex items-center justify-between">
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ __('Edit Pipeline') }}
            </h3>
        </div>
        <div class="flex flex-col gap-2">
          <div class="field flex items-center gap-1.5 leading-5">
            <div class="shrink-0 truncate text-base text-ink-gray-8">
              {{ __('Pipeline') }}
            </div>
          </div>
          <div class="flex items-center justify-between w-[100%]">
            <Link class="w-full form-control select-text" :value="_form.pipeline" doctype="CRM Pipeline"
              @change="(data) => updateField('pipeline', data)" />
          </div>
          <div v-if="data?.pipeline" class="field flex items-center gap-2 leading-5">
            <div class="shrink-0 truncate text-base text-ink-gray-8">
              {{ __('Stage') }}
            </div>
          </div>
          <div class="flex items-center justify-between w-[100%]">
            <Link class="w-full form-control select-text" :value="_form.stage" doctype="CRM Stage"
              :dependsFilter="_form.pipeline ? { 'pipeline': _form.pipeline } : {}"
              @change="(data) => updateField('stage', data)" />
          </div>
        </div>
      </div>
      <div class="flex flex-row-reverse gap-2 px-4 pb-7 pt-4 sm:px-6">
        <div class="space-y-2">
          <Button class="max-w-[200px]" :disabled="_form.pipeline === '' || _form.stage === ''" variant="solid"
            :label="__('Save')" :loading="loading" @click="updatePipeline" />
        </div>
        <div class="space-y-2">
          <Button class="max-w-[200px]" variant="solid" :label="__('Cancel')" @click="show = false" />
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import Link from '@/components/Controls/Link.vue'


const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
  onSave: {
    type: Function,
    default: () => { },
  },
})

const show = defineModel()
const loading = ref(false)

let _form = ref({
  pipeline: '',
  stage: '',
})

watch(() => props.data, (newData) => {
  if (newData) {
    _form.value.pipeline = newData?.pipeline || ''
    _form.value.stage = newData?.stage || ''
  }
}, { immediate: true })

async function updatePipeline() {
  if (_form.value.pipeline == '' || _form.value.stage == '') return
  props.onSave && props.onSave(_form.value);
  show.value = false;
}

function updateField(name, value) {
  _form.value[name] = value;
  if (name === 'pipeline' && props.data.pipeline !== value) _form.value.stage = '';
}
</script>