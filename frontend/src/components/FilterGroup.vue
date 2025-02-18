<template>
  <NestedPopover>
    <template #target>
      <div class="flex items-center">
        <Button :label="__('Filter')" :class="filters?.size ? 'rounded-r-none' : ''">
          <template #prefix>
            <FilterIcon class="h-4" />
          </template>
          <template v-if="filters?.size" #suffix>
            <div
              class="flex h-5 w-5 items-center justify-center rounded-[5px] bg-surface-white pt-px text-xs font-medium text-ink-gray-8 shadow-sm">
              {{ filters.size }}
            </div>
          </template>
        </Button>
        <Tooltip v-if="filters?.size" :text="__('Clear all Filter')">
          <div>
            <Button class="rounded-l-none border-l" icon="x" @click.stop="clearfilter(false)" />
          </div>
        </Tooltip>
      </div>
    </template>
    <template #body="{ close }">
      <div
        class="my-2 min-w-40 rounded-lg bg-surface-modal shadow-2xl ring-1 ring-black ring-opacity-5 focus:outline-none">
        <div class="min-w-72 p-2 ">
          <div v-if="filters?.size" v-for="(group, g) in filters" :key="g" :id="'group-list' + g" class="mb-4 sm:mb-3">
            <div class="text-md px-2 pb-2">
              {{ __(`Group ${g + 1}`) }}
            </div>
            <div class="flex flex-col text-sm text-ink-gray-5">
              <div v-for="(field, i) in group" :key="i" :id="'filter-list' + i" class="mb-4 sm:mb-3">
                <div v-if="isMobileView" class="flex flex-col gap-2">
                  <div class="-mb-2 flex w-full items-center justify-between">
                    <div class="text-base text-ink-gray-5">
                      {{ i == 0 ? __('Where') : __('And') }}
                    </div>
                    <Button class="flex" variant="ghost" icon="x" @click="removeFilter(i)" />
                  </div>
                  <div id="fieldname" class="w-full">
                    <Autocomplete :value="field.fieldname" :options="filterableFields.data"
                      @change="(e) => updateFilter(e, g, i)" :placeholder="__('First Name')" />
                  </div>
                  <div id="operator">
                    <FormControl type="select" v-model="field.operator" @change="(e) => updateOperator(e, field, g, i)"
                      :options="getOperators(field.field.fieldtype, field.field.fieldname)" :placeholder="__('Equals')" />
                  </div>
                  <div id="value" class="w-full">
                    <component :is="getValueControl(field)" v-model="field.value" @change.stop="(v) => updateValue(v, field)"
                      :placeholder="__('John Doe')" />
                  </div>
                </div>
                <div v-else class="flex items-center justify-between gap-2">
                  <div class="flex items-center gap-2">
                    <div class="w-13 pl-2 text-end text-base text-ink-gray-5">
                      {{ i == 0 ? __('Where') : __('And') }}
                    </div>
                    <div id="fieldname" class="!min-w-[140px]">
                      <Autocomplete :value="field.fieldname" :options="filterableFields.data"
                        @change="(e) => updateFilter(e, g, i)" :placeholder="__('First Name')" />
                    </div>
                    <div id="operator">
                      <FormControl type="select" v-model="field.operator" @change="(e) => updateOperator(e, field, g, i)" :options="getOperators(field.field.fieldtype, field.field.fieldname)" :placeholder="__('Equals')" />
                    </div>
                    <div id="value" class="!min-w-[140px]">
                      <component :is="getValueControl(field)" v-model="field.value" @change="(v) => updateValue(v, field)"
                        :placeholder="__('John Doe')" />
                    </div>
                  </div>
                  <Button class="flex" variant="ghost" icon="x" @click="removeFilter(i)" />
                </div>
              </div>
              <Autocomplete value="" :options="filterableFields.data" @change="(e) => setfilter(e,g)"
                :placeholder="__('First name')">
                <template #target="{ togglePopover }">
                  <Button class="!text-ink-gray-5" variant="ghost" @click="togglePopover()" :label="__('Add Filter')">
                    <template #prefix>
                      <FeatherIcon name="plus" class="h-4" />
                    </template>
                  </Button>
                </template>
              </Autocomplete>
            </div>
            <div v-if="filters.size != (g + 1)" class="text-ink-gray-5 separator">
              <span>{{ __("OR") }}</span>
            </div>
          </div>
          <div v-else class="mb-3 flex h-7 items-center px-3 text-sm text-ink-gray-5">
            {{ __('Empty - Choose a field to filter by') }}
          </div>
          <div class="flex items-center justify-between gap-2">
            <Autocomplete v-if="!filters?.size" value="" :options="filterableFields.data" @change="(e) => setfilter(e,'new')"
              :placeholder="__('First name')">
              <template #target="{ togglePopover }">
                <Button class="!text-ink-gray-5" variant="ghost" @click="togglePopover()" :label="__('Add Filter')">
                  <template #prefix>
                    <FeatherIcon name="plus" class="h-4" />
                  </template>
                </Button>
              </template>
            </Autocomplete>
            <Autocomplete v-else value="" :options="filterableFields.data"
              @change="(e) => { addFilterGroup(); setfilter(e, (filters.size - 1)) }" :placeholder="__('First name')">
              <template #target="{ togglePopover }">
                <Button class="!text-ink-gray-5" variant="subtle" @click="togglePopover()"
                  :label="__('Add Filter Group')">
                  <template #prefix>
                    <FeatherIcon name="plus" class="h-4" />
                  </template>
                </Button>
              </template>
            </Autocomplete>
            <Button v-if="filters?.size" class="!text-ink-gray-5" variant="ghost" :label="__('Clear all Filter')"
              @click="clearfilter(close)" />
          </div>
        </div>
      </div>
    </template>
  </NestedPopover>
</template>
<script setup>
import NestedPopover from '@/components/NestedPopover.vue'
import FilterIcon from '@/components/Icons/FilterIcon.vue'
import Link from '@/components/Controls/Link.vue'
import Autocomplete from '@/components/frappe-ui/Autocomplete.vue'
import {
  FormControl,
  createResource,
  Tooltip,
  DatePicker,
  DateTimePicker,
  DateRangePicker,
} from 'frappe-ui'
import { h, computed, onMounted } from 'vue'
import { isMobileView } from '@/composables/settings'

const typeCheck = ['Check']
const typeLink = ['Link', 'Dynamic Link']
const typeNumber = ['Float', 'Int', 'Currency', 'Percent']
const typeSelect = ['Select']
const typeString = ['Data', 'Long Text', 'Small Text', 'Text Editor', 'Text']
const typeDate = ['Date', 'Datetime']

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  default_filters: {
    type: Object,
    default: {},
  },
})

const emit = defineEmits(['update'])

const list = defineModel()

const filterableFields = createResource({
  url: 'crm.api.doc.get_filterable_fields',
  cache: ['filterableFields', props.doctype],
  params: { doctype: props.doctype },
})

onMounted(() => {
  if (filterableFields.data?.length) return
  filterableFields.fetch()
})

const filters = computed(() => {
  if (!list.value?.data) return new Set()
  let allFilters = list.value?.params?.filters || list.value.data?.params?.filters
  if (!allFilters || !filterableFields.data) return new Set()
  // remove default filters
  if (props.default_filters) {
    allFilters = removeCommonFilters(props.default_filters, allFilters)
  }
  allFilters = convertToGroupedFilters(filterableFields.data, allFilters)
  console.log(allFilters);
  
  return allFilters
})

function convertToGroupedFilters(data, allFilters) {
  if (!Array.isArray(allFilters)) allFilters = []
  let initialGroup = allFilters.map((group) => {
    return group.map((filter) => {
      let value = filter
      let field = data.find((f) => f.fieldname === value.fieldname)
      filter.field = field
      if (field?.fieldtype === 'Check') {
        filter.value = value.value ? 'Yes' : 'No'
      }
      filter.operator = oppositeOperatorMap[value.operator]
      return filter
    })
  })
  return new Set(initialGroup)
}

function addFilterGroup() {
  filters.value.add([]);
}

function removeCommonFilters(commonFilters, allFilters) {
  for (const key in commonFilters) {
    if (commonFilters.hasOwnProperty(key) && allFilters.hasOwnProperty(key)) {
      if (commonFilters[key] === allFilters[key]) {
        delete allFilters[key]
      }
    }
  }
  return allFilters
}

function getOperators(fieldtype, fieldname) {
  let options = []
  if (typeString.includes(fieldtype)) {
    options.push(
      ...[
        { label: __('Equals'), value: 'equals' },
        { label: __('Not Equals'), value: 'not equals' },
        { label: __('Like'), value: 'like' },
        { label: __('Not Like'), value: 'not like' },
        { label: __('In'), value: 'in' },
        { label: __('Not In'), value: 'not in' },
        { label: __('Is'), value: 'is' },
      ],
    )
  }
  if (fieldname === '_assign') {
    // TODO: make equals and not equals work
    options = [
      { label: __('Like'), value: 'like' },
      { label: __('Not Like'), value: 'not like' },
      { label: __('Is'), value: 'is' },
    ]
  }
  if (typeNumber.includes(fieldtype)) {
    options.push(
      ...[
        { label: __('Equals'), value: 'equals' },
        { label: __('Not Equals'), value: 'not equals' },
        { label: __('Like'), value: 'like' },
        { label: __('Not Like'), value: 'not like' },
        { label: __('In'), value: 'in' },
        { label: __('Not In'), value: 'not in' },
        { label: __('Is'), value: 'is' },
        { label: __('<'), value: '<' },
        { label: __('>'), value: '>' },
        { label: __('<='), value: '<=' },
        { label: __('>='), value: '>=' },
      ],
    )
  }
  if (typeSelect.includes(fieldtype)) {
    options.push(
      ...[
        { label: __('Equals'), value: 'equals' },
        { label: __('Not Equals'), value: 'not equals' },
        { label: __('In'), value: 'in' },
        { label: __('Not In'), value: 'not in' },
        { label: __('Is'), value: 'is' },
      ],
    )
  }
  if (typeLink.includes(fieldtype)) {
    options.push(
      ...[
        { label: __('Equals'), value: 'equals' },
        { label: __('Not Equals'), value: 'not equals' },
        { label: __('Like'), value: 'like' },
        { label: __('Not Like'), value: 'not like' },
        { label: __('In'), value: 'in' },
        { label: __('Not In'), value: 'not in' },
        { label: __('Is'), value: 'is' },
      ],
    )
  }
  if (typeCheck.includes(fieldtype)) {
    options.push(...[{ label: __('Equals'), value: 'equals' }])
  }
  if (['Duration'].includes(fieldtype)) {
    options.push(
      ...[
        { label: __('Like'), value: 'like' },
        { label: __('Not Like'), value: 'not like' },
        { label: __('In'), value: 'in' },
        { label: __('Not In'), value: 'not in' },
        { label: __('Is'), value: 'is' },
      ],
    )
  }
  if (typeDate.includes(fieldtype)) {
    options.push(
      ...[
        { label: __('Equals'), value: 'equals' },
        { label: __('Not Equals'), value: 'not equals' },
        { label: __('Is'), value: 'is' },
        { label: __('>'), value: '>' },
        { label: __('<'), value: '<' },
        { label: __('>='), value: '>=' },
        { label: __('<='), value: '<=' },
        { label: __('Between'), value: 'between' },
        { label: __('Timespan'), value: 'timespan' },
      ],
    )
  }

  return options
}

function getValueControl(f) {

  let operator = f.operator
  const field = f.field
  const { fieldtype, options } = field

  if (operator == 'is') {
    return h(FormControl, {
      type: 'select',
      options: [
        {
          label: 'Set',
          value: 'set',
        },
        {
          label: 'Not Set',
          value: 'not set',
        },
      ],
    })
  } else if (operator == 'timespan') {
    return h(FormControl, {
      type: 'select',
      options: timespanOptions,
    })
  } else if (['like', 'not like', 'in', 'not in'].includes(operator)) {
    return h(FormControl, { type: 'text' })
  } else if (typeSelect.includes(fieldtype) || typeCheck.includes(fieldtype)) {
    const _options =
      fieldtype == 'Check' ? ['Yes', 'No'] : getSelectOptions(options)
    return h(FormControl, {
      type: 'select',
      options: _options.map((o) => ({
        label: o,
        value: o,
      })),
    })
  } else if (typeLink.includes(fieldtype)) {
    if (fieldtype == 'Dynamic Link') {
      return h(FormControl, { type: 'text' })
    }
    return h(Link, { class: 'form-control', doctype: options, value: f.value })
  } else if (typeNumber.includes(fieldtype)) {
    return h(FormControl, { type: 'number' })
  } else if (typeDate.includes(fieldtype) && operator == 'between') {
    return h(DateRangePicker, { value: f.value, iconLeft: '' })
  } else if (typeDate.includes(fieldtype)) {
    return h(fieldtype == 'Date' ? DatePicker : DateTimePicker, {
      value: f.value,
      iconLeft: '',
    })
  } else {
    return h(FormControl, { type: 'text' })
  }
}

function getDefaultValue(field) {
  if (typeSelect.includes(field.fieldtype)) {
    return getSelectOptions(field.options)[0]
  }
  if (typeCheck.includes(field.fieldtype)) {
    return 'Yes'
  }
  if (typeDate.includes(field.fieldtype)) {
    return null
  }
  return ''
}

function getDefaultOperator(fieldtype) {
  if (typeSelect.includes(fieldtype)) {
    return 'equals'
  }
  if (typeCheck.includes(fieldtype) || typeNumber.includes(fieldtype)) {
    return 'equals'
  }
  if (typeDate.includes(fieldtype)) {
    return 'between'
  }
  return 'like'
}

function getSelectOptions(options) {
  return options.split('\n')
}

function setfilter(data, group = "new") {
  if (!data) return
  if (group == "new") filters.value.add([])
  group = 0
  let groups = Array.from(filters.value)

  groups[group].push({
    fieldname:data.fieldname,
    operator:getDefaultOperator(data.fieldtype),
    value:getDefaultValue(data),
    field:{
      label: data.label,
      fieldname: data.fieldname,
      fieldtype: data.fieldtype,
      options: data.options,
    }
  })
  apply()
}

function updateFilter(data, group, index) {
  if (!data.fieldname) return
  let groups = Array.from(filters.value)

  groups[group][index] = {
    fieldname:data.fieldname,
    operator:getDefaultOperator(data.fieldtype),
    value:getDefaultValue(data),
    field:{
      label: data.label,
      fieldname: data.fieldname,
      fieldtype: data.fieldtype,
      options: data.options,
    }
  }
  apply()
}

function removeFilter(index) {
  filters.value.delete(Array.from(filters.value)[index])
  apply()
}

function clearfilter(close) {
  filters.value.clear()
  apply()
  close && close()
}

function updateValue(value, filter) {
  value = value.target ? value.target.value : value
  if (filter.operator === 'between') {
    filter.value = [value.split(',').fieldname, value.split(',').operator]
  } else {
    filter.value = value
  }
  apply()
}

function updateOperator(event, filter, group, i) {
  let oldOperatorValue = event.target._value
  let newOperatorValue = event.target.value

  filter.operator = newOperatorValue
  if (!isSameTypeOperator(oldOperatorValue, newOperatorValue)) {
    filter.value = getDefaultValue(filter.field)
  }
  if (newOperatorValue === 'is' || newOperatorValue === 'is not') {
    filter.value = 'set'
  }

  apply()
}

function isSameTypeOperator(oldOperator, newOperator) {
  let textOperators = [
    'equals',
    'not equals',
    'in',
    'not in',
    '>',
    '<',
    '>=',
    '<=',
  ]
  if (
    textOperators.includes(oldOperator) &&
    textOperators.includes(newOperator)
  )
    return true
  return false
}

function apply() {
  let _filters = []
  let groups = Array.from(filters.value)

  _filters = groups.map((group) => {
    return group.map((f) => {
      return {
        fieldname:f.fieldname,
        operator:f.operator,
        value:f.value,
      }
    })
  })
  _filters = parseFilters(_filters)
  emit('update', _filters)
}

function parseFilters(filtersData) {
  const obj = filtersData.map((filtersArray) => {
    return filtersArray.map(transformIn)
  })
  let merged = removeEmptyArrayGroup(obj)
  return merged
}

function removeEmptyArrayGroup(array) {
  return array.filter((group) => group.length > 0)
}

function transformIn(f) {
  if (f.operator == 'like' && !f.value.includes('%')) {
    f.value = `%${f.value}%`
  }
  f.operator = operatorMap[f.operator]
  return f
}

const operatorMap = {
  is: 'is',
  'is not': 'is not',
  in: 'in',
  'not in': 'not in',
  equals: '=',
  'not equals': '!=',
  yes: true,
  no: false,
  'like': 'LIKE',
  'not like': 'NOT LIKE',
  '>': '>',
  '<': '<',
  '>=': '>=',
  '<=': '<=',
  between: 'between',
  timespan: 'timespan',
}

const oppositeOperatorMap = {
  is: 'is',
  '=': 'equals',
  '!=': 'not equals',
  equals: 'equals',
  'is not': 'is not',
  true: 'yes',
  false: 'no',
  LIKE: 'like',
  'NOT LIKE': 'not like',
  in: 'in',
  'not in': 'not in',
  '>': '>',
  '<': '<',
  '>=': '>=',
  '<=': '<=',
  between: 'between',
  timespan: 'timespan',
}

const timespanOptions = [
  {
    label: __('Last Week'),
    value: 'last week',
  },
  {
    label: __('Last Month'),
    value: 'last month',
  },
  {
    label: __('Last Quarter'),
    value: 'last quarter',
  },
  {
    label: __('Last 6 Months'),
    value: 'last 6 months',
  },
  {
    label: __('Last Year'),
    value: 'last year',
  },
  {
    label: __('Yesterday'),
    value: 'yesterday',
  },
  {
    label: __('Today'),
    value: 'today',
  },
  {
    label: __('Tomorrow'),
    value: 'tomorrow',
  },
  {
    label: __('This Week'),
    value: 'this week',
  },
  {
    label: __('This Month'),
    value: 'this month',
  },
  {
    label: __('This Quarter'),
    value: 'this quarter',
  },
  {
    label: __('This Year'),
    value: 'this year',
  },
  {
    label: __('Next Week'),
    value: 'next week',
  },
  {
    label: __('Next Month'),
    value: 'next month',
  },
  {
    label: __('Next Quarter'),
    value: 'next quarter',
  },
  {
    label: __('Next 6 Months'),
    value: 'next 6 months',
  },
  {
    label: __('Next Year'),
    value: 'next year',
  },
]
</script>


<style scoped>
.separator {
  width: 100%;
  display: flex;
  align-items: center;
  text-align: center;
}

.separator::before,
.separator::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid #7C7C7C;
  margin: 0 10px;
}
</style>