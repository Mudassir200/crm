<template>
    <div class="my-3 flex items-center justify-between text-lg font-medium sm:mb-4">
        <div class="box-shadow-1 p-3 w-[100%]" v-for="section in sections" :key="section.title">
            <div v-if="section.visible">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="">{{ section.title }}</h2>
                    <Button v-if="section.editable" variant="ghost">
                        <FeatherIcon name="settings" class="h-4 w-4" />
                    </Button>
                </div>
                <div class="flex flex-col flex-1 gap-4">
                    <div v-for="row in section.items" :key="row[0].title" class="flex w-[100%] justify-evenly gap-4">
                        <div v-for="item in row" :key="item.title">
                            <div class="flex flex-col gap-1 items-center justify-between">
                                <div class="text-base text-ink-gray-8 font-semibold uppercase">{{ item.title }}</div>
                                <div class="text-base text-ink-gray-8 font-normal">{{ item.value }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

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

const sections = ref([{
    title: "Data Highlights",
    type: "highlight",
    editable: true,
    visible: true,
    items: [
        [
            {
                "title": "Create Date",
                "value": "28/11/2024 10:54 AM GMT+5:30",
            },
            {
                "title": "Deal Stage",
                "value": "Ready 0-3 months",
            },
            {
                "title": "Last Activity Date",
                "value": "28/11/2024 10:55 AM GMT+5:30",
            },
        ],
        [
            {
                "title": "Status",
                "value": "Qualification",
            },
            {
                "title": "Deal Owner",
                "value": "Administrator",
            },
            {
                "title": "Deal Type",
                "value": "New Business",
            }
        ]
    ]
}])

</script>

<style scoped>
.box-shadow-1 {
    box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
}
</style>