<template>
  <div class="filter-panel card"> <!-- 'card' class is good for structure -->
    <div class="card-body"> <!-- 'card-body' adds padding -->
      <!-- Tab Switcher with Counts -->
      <div class="mb-4">
        <h6 class="tabs-title-heading">{{ texts.tabsTitle || 'Lead Categories' }}</h6>
        <div class="nav flex-column nav-pills filter-tabs">
          <button
            :class="['nav-link text-start', { active: localCurrentTab === 'new' }]"
            @click="emitTabChange('new')"
            type="button"
            :disabled="isLoading"
          >
            <i class="bi bi-stars me-1"></i> {{ texts.tabNew || 'New' }}
            <span class="badge rounded-pill float-end ms-2">{{ tabCounts.new }}</span>
          </button>
          <button
            :class="['nav-link text-start', { active: localCurrentTab === 'saved' }]"
            @click="emitTabChange('saved')"
            type="button"
            :disabled="isLoading"
          >
            <i class="bi bi-bookmark-check-fill me-1"></i> {{ texts.tabSaved || 'Saved' }}
            <span class="badge rounded-pill float-end ms-2">{{ tabCounts.saved }}</span>
          </button>
          <button
            :class="['nav-link text-start', { active: localCurrentTab === 'archived' }]"
            @click="emitTabChange('archived')"
            type="button"
            :disabled="isLoading"
          >
            <i class="bi bi-archive-fill me-1"></i> {{ texts.tabArchived || 'Archived' }}
            <span class="badge rounded-pill float-end ms-2">{{ tabCounts.archived }}</span>
          </button>
        </div>
      </div>

      <hr class="filter-divider">

      <!-- Filter Sections -->
      <div v-for="filterGroup in filterableFields" :key="filterGroup.key" class="mb-3 filter-group">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <label :for="`filter-${filterGroup.key}`" class="form-label filter-group-label">
            {{ filterGroup.label }}
          </label>
          <button
            v-if="activeFilters[filterGroup.key] && ((Array.isArray(activeFilters[filterGroup.key])) || (!Array.isArray(activeFilters[filterGroup.key]) && activeFilters[filterGroup.key]))"
            @click="clearFilterSection(filterGroup.key)"
            class="btn btn-sm btn-icon-danger py-0 px-1 clear-section-btn"
            :title="texts.clearFilterSectionTooltip + ' ' + filterGroup.label"
          >
            <i class="bi bi-x-circle"></i>
          </button>
        </div>

        <div v-if="['text', 'keywords'].includes(filterGroup.type)" class="input-group input-group-sm mb-2">
          <input
            type="text"
            class="form-control form-control-sm filter-input"
            :id="`filter-input-${filterGroup.key}`"
            v-model="inputValues[filterGroup.key]"
            :placeholder="filterGroup.placeholder || (texts.addFilterPlaceholder + ' ' + filterGroup.label.toLowerCase())"
            @keyup.enter="addTextFilter(filterGroup.key, filterGroup.type === 'keywords')"
          />
          <button class="btn btn-outline-themed btn-sm add-filter-btn" type="button" @click="addTextFilter(filterGroup.key, filterGroup.type === 'keywords')">
            <i class="bi bi-plus-lg"></i>
          </button>
        </div>

        <select
          v-if="filterGroup.type === 'select'"
          class="form-select form-select-sm filter-select mb-2"
          :id="`filter-select-${filterGroup.key}`"
          v-model="inputValues[filterGroup.key]"
          @change="addSelectFilter(filterGroup.key, ($event.target as HTMLSelectElement).value)"
        >
          <option value="">{{ filterGroup.placeholder || (texts.selectFilterPlaceholder + ' ' + filterGroup.label) }}</option>
          <option v-for="option in filterGroup.options" :key="option.value" :value="option.value">
            {{ option.text }}
          </option>
        </select>

        <div v-if="activeFilters[filterGroup.key]" class="d-flex flex-wrap gap-1 mt-1 filter-tags-container">
          <span
            v-for="(item, index) in activeFilters[filterGroup.key]"
            :key="`${filterGroup.key}-${index}`"
            class="badge filter-tag p-1"
          >
            {{ item }}
            <button
              type="button"
              class="btn-close btn-close-sm ms-1 filter-tag-close"
              @click="removeFilterItem(filterGroup.key, item)"
              :aria-label="texts.removeFilterTooltip"
            ></button>
          </span>
        </div>
      </div>
       <hr class="filter-divider mt-4">
        <button @click="clearAllClientFilters" class="btn btn-sm btn-danger w-100 clear-all-btn">
            <i class="bi bi-trash3 me-1"></i> {{ texts.clearAllFiltersButton || "Clear All Filters" }}
        </button>
    </div>
  </div>
</template>

<script setup lang="ts">
// ----- SCRIPT is THE SAME as your provided version -----
import { ref, reactive, watch, computed } from 'vue';
import type { PropType } from 'vue'
import type { LeadTab } from '@/types/tabs';

export interface TabCounts { new: number; saved: number; archived: number; }
export type FilterKey = 'job_title' | 'industry' | 'location' | 'company_name' | 'company_size' | 'keywords' | 'lead_status';

export interface ClientFilterItem {
    key: FilterKey;
    label: string;
    type: 'text' | 'select' | 'keywords';
    options?: { value: string; text: string }[];
    placeholder?: string;
}
export interface ActiveClientFilters {
    job_title?: string[];
    industry?: string[];
    location?: string[];
    company_name?: string[];
    company_size?: string[];
    keywords?: string[];
    lead_status?: string[];
    [key: string]: string[] | undefined;
}


const props = defineProps({
  currentTab: {
    type: String as PropType<LeadTab>,
    required: true,
  },
  tabCounts: {
    type: Object as PropType<TabCounts>,
    required: true,
    default: () => ({ new: 0, saved: 0, archived: 0 }),
  },
  languageStore: {
    type: Object,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  industryOptions: {
    type: Array as PropType<{ value: string; text: string }[]>,
    default: () => [],
  },
  companySizeOptions: {
    type: Array as PropType<{ value: string; text: string }[]>,
    default: () => [
        { value: '1-10', text: '1-10' }, { value: '11-50', text: '11-50' },
        { value: '51-200', text: '51-200' }, { value: '201-500', text: '201-500' },
        { value: '501-1000', text: '501-1000' }, { value: '1001-5000', text: '1001-5000' },
        { value: '5001-10000', text: '5001-10000' }, { value: '10001+', text: '10001+' },
    ],
  },
  leadStatusOptions: {
    type: Array as PropType<{ value: string; text: string }[]>,
    default: () => [
        { value: 'New Prospect', text: 'New Prospect' }, { value: 'Contacted', text: 'Contacted' },
        { value: 'Follow-up', text: 'Follow-up' }, { value: 'Replied', text: 'Replied' },
    ],
  },
});

const emit = defineEmits(['update:currentTab', 'update:filters']);

const localCurrentTab = ref(props.currentTab);
const inputValues = reactive<Record<FilterKey, string>>({
    job_title: '', industry: '', location: '', company_name: '', company_size: '', keywords: '', lead_status: ''
});
const activeFilters = reactive<ActiveClientFilters>({});

const texts = computed(() => {
    const defaults = {
        tabsTitle: 'Lead Categories', tabNew: 'New', tabSaved: 'Saved', tabArchived: 'Archived',
        addFilterPlaceholder: 'Add', selectFilterPlaceholder: 'Select',
        removeFilterTooltip: 'Remove filter', clearAllFiltersButton: 'Clear All Filters',
        clearFilterSectionTooltip: 'Clear section',
        colJobTitle: 'Job Title', colIndustry: 'Industry', colLocation: 'Location', colCompanyName: 'Company Name',
        colCompanySize: 'Company Size', colKeywords: 'Keywords', colStatus: 'Lead Status',
        industryPlaceholder: 'Select Industry', companySizePlaceholder: 'Select Company Size',
    };
    if (props.languageStore && typeof props.languageStore.texts === 'object' && Object.keys(props.languageStore.texts).length > 0) {
        const merged = { ...defaults };
        for (const key in props.languageStore.texts) {
            if (Object.prototype.hasOwnProperty.call(props.languageStore.texts, key)) {
                merged[key as keyof typeof merged] = props.languageStore.texts[key];
            }
        }
        return merged;
    }
    return defaults;
});


const filterableFields = computed<ClientFilterItem[]>(() => [
    { key: 'job_title', label: texts.value.colJobTitle, type: 'text' },
    { key: 'industry', label: texts.value.colIndustry, type: 'select', options: props.industryOptions, placeholder: texts.value.industryPlaceholder},
    { key: 'location', label: texts.value.colLocation, type: 'text' },
    { key: 'company_name', label: texts.value.colCompanyName, type: 'text' },
    { key: 'company_size', label: texts.value.colCompanySize, type: 'select', options: props.companySizeOptions, placeholder: texts.value.companySizePlaceholder },
    { key: 'keywords', label: texts.value.colKeywords, type: 'keywords' },
    { key: 'lead_status', label: texts.value.colStatus, type: 'select', options: props.leadStatusOptions, placeholder: texts.value.selectFilterPlaceholder + ' ' + texts.value.colStatus },
]);


watch(() => props.currentTab, (newVal) => {
  localCurrentTab.value = newVal;
});

function emitTabChange(tab: LeadTab) {
  console.log(`%cFilterPanel: Emitting @update:currentTab -> ${tab}`, 'color: blue; font-weight: bold;'); // Log tab change
  if (props.isLoading) return;
  localCurrentTab.value = tab;
  emit('update:currentTab', tab);
}

function addTextFilter(key: FilterKey, isKeywords: boolean = false) {
    const value = inputValues[key]?.trim();
    if (!value) return;
    if (!activeFilters[key]) {
        activeFilters[key] = [];
    }
    if (isKeywords) {
        if (!activeFilters[key]?.includes(value)) {
            activeFilters[key]?.push(value);
        }
    } else {
        activeFilters[key] = [value];
    }
    inputValues[key] = '';
    emitUpdateFilters();
}

function addSelectFilter(key: FilterKey, value: string) {
    if (value) {
        activeFilters[key] = [value];
    } else {
        delete activeFilters[key];
    }
    emitUpdateFilters();
}

function removeFilterItem(key: FilterKey, itemToRemove: string) {
  if (activeFilters[key]) {
    activeFilters[key] = activeFilters[key]?.filter(item => item !== itemToRemove);
    if (activeFilters[key]?.length === 0) {
      delete activeFilters[key];
    }
    emitUpdateFilters();
  }
}

function clearFilterSection(key: FilterKey) {
    delete activeFilters[key];
    if (inputValues.hasOwnProperty(key)) {
        inputValues[key] = '';
    }
    emitUpdateFilters();
}

function clearAllClientFilters() {
    for (const key in activeFilters) {
        delete activeFilters[key as FilterKey];
    }
     for (const key in inputValues) {
        inputValues[key as FilterKey] = '';
    }
    emitUpdateFilters();
}

function emitUpdateFilters() {
  const filtersToEmit = JSON.parse(JSON.stringify(activeFilters));
  console.log('%cFilterPanel: Emitting @update:filters ->', 'color: blue; font-weight: bold;', JSON.stringify(filtersToEmit)); // Log filters
  console.count('FilterPanel: @update:filters emitted'); // Count how many times this happens
  emit('update:filters', filtersToEmit);
}
</script>