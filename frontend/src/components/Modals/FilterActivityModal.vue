<template>
    <Dialog v-model="show" :options="{ size: 'md' }">
        <template #body>
            <div class="bg-surface-modal px-4 pb-6 pt-5 sm:px-6">
                <div class="mb-5 flex items-center justify-between">
                    <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
                        {{ __('Activity Filter') }}
                    </h3>
                    <div class="flex items-center gap-1">
                        <Button variant="ghost" class="w-7" @click="show = false">
                            <FeatherIcon name="x" class="h-4 w-4" />
                        </Button>
                    </div>
                </div>
                <div class="flex flex-col gap-4 mb-3">
                    <div class="flex items-center gap-2">
                        <Checkbox v-model="allSelect" :binary="true" inputId="all" />
                        <label for="all">{{ __('Select All') }}</label>
                    </div>
                    <div v-for="option in filterOptions" :key="option.key" class="flex items-center gap-2">
                        <Checkbox v-model="selectedOptions" :inputId="option.key" name="option" :value="option.key" />
                        <label :for="option.key">{{ option.name }}</label>
                    </div>
                </div>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import Checkbox from "primevue/checkbox"

const props = defineProps({
    types: {
        type: Array,
        default: () => [
            {name: "Activity", key: "activity"},
            {name: "Emails", key: "emails"},
            {name: "Calls", key: "calls"},
            {name: "Comments", key: "comments"},
            {name: "Attachments", key: "attachments"},
        ],
    },
    selectedFilter: {
        type: Array,
        default: () => [],
    }
})

const emit = defineEmits(['after'])
const filterOptions = ref([])
const selectedOptions = ref([])
const allSelect = ref(false)
const show = defineModel()

onMounted(() => {
    filterOptions.value = [...props.types]
    selectedOptions.value = [...props.selectedFilter]
})

watch(selectedOptions, (newVal) => {
    allSelect.value = newVal.length === filterOptions.value.length
    emit('after', [...selectedOptions.value])
}, { deep: true })

watch(allSelect, (checked) => {
    selectedOptions.value = checked ? 
                    filterOptions.value.map(option => option.key) : 
                    filterOptions.value.length == selectedOptions.value.length ? [] : 
                    selectedOptions.value
})
</script>
