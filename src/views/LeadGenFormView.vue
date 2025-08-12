<template>
  <div class="lead-gen-view-wrapper">
    <div class="view-main-content">
      <div class="filter-sidebar-view" :class="{ collapsed: sidebarCollapsed }">
        <div
          class="filter-header d-flex justify-content-between align-items-center"
        >
          <h5 class="m-0 fw-bold" v-if="!sidebarCollapsed">
            {{ texts.filtersTitle }}
          </h5>
          <button class="btn btn-sm btn-icon" @click="toggleSidebar">
            <i
              class="bi"
              :class="sidebarCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"
            ></i>
          </button>
        </div>
        <div class="filter-content" v-if="!sidebarCollapsed">
          <FilterPanelView
            :currentTab="currentTab"
            :tabCounts="tabCounts"
            :languageStore="languageStore"
            :isLoading="isLoadingLeads || isSearchingLeads"
            :industryOptions="languageStore.industries || []"
            :companySizeOptions="companySizeOptionsForFilter"
            :leadStatusOptions="leadStatusOptionsForFilter"
            @update:currentTab="handleTabChangeFromPanel"
            @update:filters="handleClientFiltersUpdate"
          />
        </div>
      </div>

      <div class="content-area-view">
        <div class="search-panel" :class="{ collapsed: !showSearchForm }">
          <div
            class="search-panel-header d-flex justify-content-between align-items-center mb-2"
          >
            <h5 class="m-0 search-panel-title">{{ texts.formDescription }}</h5>
            <button
              class="btn btn-sm btn-icon search-panel-toggle-icon"
              @click="toggleSearchForm"
            >
              <i
                :class="[
                  'bi',
                  showSearchForm ? 'bi-chevron-up' : 'bi-chevron-down',
                ]"
              ></i>
            </button>
          </div>
          <div class="search-panel-body" v-if="showSearchForm">
            <form @submit.prevent="submitLeadSearchCriteria">
              <div class="mb-3">
                <label
                  for="naturalLanguageQuery"
                  class="form-label search-panel-label fw-medium"
                  >{{ texts.mainQueryLabel }}</label
                >
                <textarea
                  class="form-control form-control-lg search-panel-textarea"
                  id="naturalLanguageQuery"
                  rows="2"
                  v-model="naturalLanguageQuery"
                  :placeholder="texts.mainQueryPlaceholder"
                ></textarea>
              </div>
              <div class="d-flex flex-wrap mb-3 gap-2 search-panel-actions">
                <button
                  type="button"
                  class="btn btn-light btn-sm search-panel-btn-light"
                  @click="toggleAdvancedFilters"
                >
                  <i
                    :class="[
                      'bi me-1',
                      showAdvancedFilters ? 'bi-funnel-fill' : 'bi-funnel',
                    ]"
                  ></i>
                  {{
                    showAdvancedFilters
                      ? texts.advancedBtnTextHide
                      : texts.advancedBtnTextShow
                  }}
                </button>
                <button
                  type="submit"
                  class="btn btn-primary btn-sm px-3 search-panel-btn-primary"
                  :disabled="isSearchingLeads"
                >
                  <span
                    v-if="isSearchingLeads"
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                  ></span>
                  <i v-else class="bi bi-search me-1"></i>
                  {{ texts.searchLeadsButton }}
                </button>
              </div>
              <div
                :class="[
                  'advanced-filters-panel-content',
                  { show: showAdvancedFilters },
                ]"
              >
                <hr class="my-2 search-panel-divider" />
                <div class="row g-2">
                  <div class="col-md-6">
                    <label
                      for="advJobTitle"
                      class="form-label search-panel-adv-label"
                      >{{ texts.jobTitleLabel }}
                      <span v-if="isAdvancedCriteriaActive" class="text-danger"
                        >*</span
                      ></label
                    ><input
                      type="text"
                      class="form-control form-control-sm search-panel-adv-input"
                      id="advJobTitle"
                      v-model="advancedFilterInputs.jobTitle"
                    />
                  </div>
                  <div class="col-md-6">
                    <label
                      for="advIndustry"
                      class="form-label search-panel-adv-label"
                      >{{ texts.industryLabel }}
                      <span v-if="isAdvancedCriteriaActive" class="text-danger"
                        >*</span
                      ></label
                    ><select
                      class="form-select form-select-sm search-panel-adv-select"
                      id="advIndustry"
                      v-model="advancedFilterInputs.industry"
                    >
                      <option value="" disabled>
                        {{ texts.industryPlaceholder }}
                      </option>
                      <option
                        v-for="industryOpt in languageStore.industries || []"
                        :key="industryOpt.value"
                        :value="industryOpt.value"
                      >
                        {{ industryOpt.text }}
                      </option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label
                      for="advLocation"
                      class="form-label search-panel-adv-label"
                      >{{ texts.locationLabel }}</label
                    ><input
                      type="text"
                      class="form-control form-control-sm search-panel-adv-input"
                      id="advLocation"
                      v-model="advancedFilterInputs.location"
                    />
                  </div>
                  <div class="col-md-6">
                    <label
                      for="advCompanySize"
                      class="form-label search-panel-adv-label"
                      >{{ texts.companySizeLabel }}</label
                    ><select
                      class="form-select form-select-sm search-panel-adv-select"
                      id="advCompanySize"
                      v-model="advancedFilterInputs.companySize"
                    >
                      <option value="" disabled>
                        {{ texts.companySizePlaceholder }}
                      </option>
                      <option value="1-10">1-10</option>
                      <option value="11-50">11-50</option>
                      <option value="51-200">51-200</option>
                      <option value="201-500">201-500</option>
                      <option value="501-1000">501-1000</option>
                      <option value="1001-5000">1001-5000</option>
                      <option value="5001-10000">5001-10000</option>
                      <option value="10001+">10001+</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label
                      for="advCompanyNames"
                      class="form-label search-panel-adv-label"
                      >{{ texts.companyNamesLabel }}</label
                    ><input
                      type="text"
                      class="form-control form-control-sm search-panel-adv-input"
                      id="advCompanyNames"
                      v-model="advancedFilterInputs.companyNames"
                      :placeholder="texts.companyNamesPlaceholder"
                    />
                  </div>
                  <div class="col-md-6">
                    <label
                      for="advGeneralKeywords"
                      class="form-label search-panel-adv-label"
                      >{{ texts.generalKeywordsLabel }}</label
                    ><input
                      type="text"
                      class="form-control form-control-sm search-panel-adv-input"
                      id="advGeneralKeywords"
                      v-model="advancedFilterInputs.generalKeywords"
                      :placeholder="texts.generalKeywordsPlaceholder"
                    />
                  </div>
                  <div class="col-12 text-end">
                    <button
                      type="button"
                      class="btn btn-primary btn-sm search-panel-btn-primary"
                      @click="addAdvancedInputsAsTags"
                    >
                      <i class="bi bi-plus-lg me-1"></i>
                      <span>{{ texts.addFiltersBtnText }}</span>
                    </button>
                  </div>
                </div>
              </div>
              <div v-if="filterTags && filterTags.length > 0" class="mt-3">
                <label class="form-label search-panel-label fw-medium">{{
                  texts.tagAreaLabel
                }}</label>
                <div class="d-flex flex-wrap gap-2">
                  <span
                    v-for="tag in filterTags || []"
                    :key="tag.id"
                    class="tag-pill search-panel-tag"
                  >
                    <strong class="me-1">{{ tag.label }}:</strong>
                    {{ tag.displayValue }}
                    <button
                      type="button"
                      class="btn-close btn-close-sm ms-2"
                      @click="removeFilterTag(tag.id)"
                      :aria-label="`${texts.removeFilterTooltip} ${tag.label}`"
                    ></button
                  ></span>
                </div>
              </div>
            </form>
            <transition name="fade">
              <div
                v-if="searchMessage"
                :class="[
                  'mt-3 alert search-panel-alert',
                  searchStatus === 'success'
                    ? 'alert-success'
                    : searchStatus === 'warning'
                    ? 'alert-warning'
                    : 'alert-danger',
                ]"
                role="alert"
              >
                {{ searchMessage }}
              </div>
            </transition>
          </div>
        </div>

        <div class="table-section-view">
          <div class="table-header">
            <div
              class="d-flex justify-content-between align-items-center w-100"
            >
              <div class="d-flex align-items-center">
                <button
                  class="btn btn-sm btn-outline-secondary me-2"
                  @click="selectAllMatchingLeads"
                  :disabled="
                    totalRowCount === 0 ||
                    allFilteredLeadsSelected ||
                    isProcessingBatch ||
                    isSelectingAllLeads
                  "
                  :title="texts.selectAllTooltip"
                >
                  <span
                    v-if="isSelectingAllLeads"
                    class="spinner-border spinner-border-sm me-1"
                    role="status"
                  ></span>
                  <i v-else class="bi bi-check2-square me-1"></i>
                  {{ texts.selectAllButton }}
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary me-2"
                  @click="deselectAllGlobalLeads"
                  :disabled="
                    selectedRowCount === 0 ||
                    isProcessingBatch ||
                    isSelectingAllLeads
                  "
                  :title="texts.deselectAllButton"
                >
                  <i class="bi bi-square me-1"></i>
                  {{ texts.deselectAllButton }}
                </button>

                <div v-if="selectedRowCount > 0" class="btn-group me-2">
                  <button
                    id="batchActionsDropdownButton"
                    ref="batchActionsDropdownToggleRef"
                    type="button"
                    class="btn btn-sm btn-primary dropdown-toggle"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                    :disabled="isProcessingBatch || isSelectingAllLeads"
                  >
                    <span
                      v-if="isProcessingBatch"
                      class="spinner-border spinner-border-sm me-1"
                      role="status"
                    ></span>
                    {{ texts.batchActionsDropdownTitle }} ({{
                      selectedRowCount
                    }})
                  </button>
                  <ul class="dropdown-menu">
                    <template v-if="currentTab === 'new'">
                      <li>
                        <a
                          class="dropdown-item"
                          href="#"
                          :class="{
                            disabled:
                              !canBatchSave ||
                              isProcessingBatch ||
                              isSelectingAllLeads,
                          }"
                          @click.prevent="
                            !(
                              !canBatchSave ||
                              isProcessingBatch ||
                              isSelectingAllLeads
                            ) && batchSaveSelected()
                          "
                          >{{ texts.batchSaveButton }}</a
                        >
                      </li>
                      <li>
                        <a
                          class="dropdown-item"
                          href="#"
                          :class="{
                            disabled:
                              !canBatchArchiveNew ||
                              isProcessingBatch ||
                              isSelectingAllLeads,
                          }"
                          @click.prevent="
                            !(
                              !canBatchArchiveNew ||
                              isProcessingBatch ||
                              isSelectingAllLeads
                            ) && batchArchiveSelected()
                          "
                          >{{ texts.batchArchiveButton }}</a
                        >
                      </li>
                    </template>

                    <template v-if="currentTab === 'saved'">
                      <li>
                        <a
                          class="dropdown-item"
                          href="#"
                          :class="{
                            disabled:
                              !canBatchRestoreToNewFromSaved ||
                              isProcessingBatch ||
                              isSelectingAllLeads,
                          }"
                          @click.prevent="
                            !(
                              !canBatchRestoreToNewFromSaved ||
                              isProcessingBatch ||
                              isSelectingAllLeads
                            ) && batchRestoreSelected()
                          "
                          >{{ texts.batchRestoreButton }}</a
                        >
                      </li>
                      <li>
                        <a
                          class="dropdown-item"
                          href="#"
                          :class="{
                            disabled:
                              !canBatchArchiveSaved ||
                              isProcessingBatch ||
                              isSelectingAllLeads,
                          }"
                          @click.prevent="
                            !(
                              !canBatchArchiveSaved ||
                              isProcessingBatch ||
                              isSelectingAllLeads
                            ) && batchArchiveSelected()
                          "
                          >{{ texts.batchArchiveButton }}</a
                        >
                      </li>
                    </template>

                    <template v-if="currentTab === 'archived'">
                      <li>
                        <a
                          class="dropdown-item"
                          href="#"
                          :class="{
                            disabled:
                              !canBatchMoveToSaved ||
                              isProcessingBatch ||
                              isSelectingAllLeads,
                          }"
                          @click.prevent="
                            !(
                              !canBatchMoveToSaved ||
                              isProcessingBatch ||
                              isSelectingAllLeads
                            ) && batchMoveToSavedSelected()
                          "
                          >{{ texts.batchMoveToSavedButton }}</a
                        >
                      </li>
                      <li><hr class="dropdown-divider" /></li>
                      <li>
                        <a
                          class="dropdown-item text-danger"
                          href="#"
                          :class="{
                            disabled:
                              !canBatchDeleteArchived ||
                              isProcessingBatch ||
                              isSelectingAllLeads,
                          }"
                          @click.prevent="
                            !(
                              !canBatchDeleteArchived ||
                              isProcessingBatch ||
                              isSelectingAllLeads
                            ) && batchDeleteSelected()
                          "
                          >{{ texts.batchDeleteButton }}</a
                        >
                      </li>
                    </template>
                    <li
                      v-if="
                        (currentTab === 'new' &&
                          (canBatchSave || canBatchArchiveNew)) ||
                        (currentTab === 'saved' &&
                          (canBatchRestoreToNewFromSaved ||
                            canBatchArchiveSaved)) ||
                        (currentTab === 'archived' &&
                          (canBatchMoveToSaved || canBatchDeleteArchived))
                      "
                    >
                      <hr class="dropdown-divider" />
                    </li>

                    <li>
                      <a
                        class="dropdown-item"
                        href="#"
                        :class="{
                          disabled:
                            isProcessingBatch ||
                            selectedRowCount === 0 ||
                            isSelectingAllLeads,
                        }"
                        @click.prevent="
                          !(
                            isProcessingBatch ||
                            selectedRowCount === 0 ||
                            isSelectingAllLeads
                          ) && exportSelectedToCSV()
                        "
                      >
                        <i class="bi bi-file-earmark-spreadsheet me-1"></i>
                        {{ texts.batchExportCSVButton }}
                      </a>
                    </li>
                  </ul>
                </div>
              </div>

              <div class="d-flex align-items-center">
                <button
                  class="btn btn-sm btn-icon me-2"
                  @click="toggleSearchForm"
                  :title="
                    showSearchForm
                      ? texts.searchFormToggleHideTooltip
                      : texts.searchFormToggleShowTooltip
                  "
                >
                  <i
                    :class="[
                      'bi',
                      showSearchForm
                        ? 'bi-arrows-angle-contract'
                        : 'bi-arrows-angle-expand',
                    ]"
                  ></i>
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="fetchLeadsForCurrentUser(true)"
                  :disabled="
                    isLoadingLeads || isProcessingBatch || isSelectingAllLeads
                  "
                  :title="texts.refreshButton"
                >
                  <i
                    :class="[
                      'bi',
                      isLoadingLeads || isProcessingBatch || isSelectingAllLeads
                        ? 'bi-arrow-clockwise spin-animation'
                        : 'bi-arrow-clockwise',
                    ]"
                  ></i>
                </button>
              </div>
            </div>
          </div>

          <div class="table-content">
            <transition name="fade" mode="out-in">
              <div
                v-if="isLoadingLeads && !isProcessingBatch"
                key="loading"
                class="loading-empty-state"
              >
                <div
                  class="spinner-border text-primary mb-3"
                  role="status"
                ></div>
                <p class="text-muted">{{ texts.loadingLeads }}</p>
              </div>
              <div
                v-else-if="
                  tableData.length === 0 &&
                  currentTab === 'new' &&
                  !initialLoadComplete &&
                  !searchMessage
                "
                key="empty-new"
                class="loading-empty-state"
              >
                <i class="bi bi-search display-1 text-muted mb-3"></i>
                <p class="lead mb-0">{{ texts.noNewLeadsYet }}</p>
              </div>
              <div
                v-else-if="tableData.length === 0"
                key="empty-generic"
                class="loading-empty-state"
              >
                <i class="bi bi-inbox display-1 text-muted mb-3"></i>
                <p class="lead">{{ noLeadsMessageForTab }}</p>
              </div>
              <div v-else key="table" class="table-wrapper">
                <table class="table table-hover lead-table mb-0">
                  <thead>
                    <tr
                      v-if="table && table.getHeaderGroups()"
                      v-for="headerGroup in table.getHeaderGroups()"
                      :key="headerGroup.id"
                    >
                      <th
                        v-for="header in headerGroup.headers"
                        :key="header.id"
                        :colSpan="header.colSpan"
                        @click="
                          header.column.getCanSort() &&
                          !isProcessingBatch &&
                          !isSelectingAllLeads
                            ? header.column.getToggleSortingHandler()?.($event)
                            : undefined
                        "
                        :class="{
                          'cursor-pointer':
                            header.column.getCanSort() &&
                            !isProcessingBatch &&
                            !isSelectingAllLeads,
                          'sorting-asc': header.column.getIsSorted() === 'asc',
                          'sorting-desc':
                            header.column.getIsSorted() === 'desc',
                        }"
                        :style="getColumnStyle(header.column)"
                      >
                        <div class="d-flex align-items-center">
                          <FlexRender
                            v-if="
                              header && header.column && header.column.columnDef
                            "
                            :render="header.column.columnDef.header"
                            :props="header.getContext()"
                          />
                        </div>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-if="table && table.getRowModel && table.getRowModel()"
                      v-for="row in table.getRowModel().rows"
                      :key="row.id"
                      :class="{
                        'table-active': row.getIsSelected(),
                        'processing-row-disabled':
                          isProcessingBatch || isSelectingAllLeads,
                      }"
                    >
                      <td
                        v-for="cell in row.getVisibleCells()"
                        :key="cell.id"
                        :style="getColumnStyle(cell.column)"
                      >
                        <FlexRender
                          v-if="cell && cell.column && cell.column.columnDef"
                          :render="cell.column.columnDef.cell"
                          :props="cell.getContext()"
                        />
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </transition>
          </div>

          <div
            class="table-footer"
            v-if="table && table.getPageCount && table.getPageCount() > 0"
          >
            <div class="d-flex justify-content-between align-items-center">
              <div class="btn-group">
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="
                    !isSelectingAllLeads &&
                      table.setPageIndex(0)
                  "
                  :disabled="
                    !table.getCanPreviousPage() ||
                    isSelectingAllLeads
                  "
                >
                  <i class="bi bi-chevron-bar-left"></i>
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="
                    !isSelectingAllLeads &&
                      table.previousPage()
                  "
                  :disabled="
                    !table.getCanPreviousPage() ||
                    isSelectingAllLeads
                  "
                >
                  <i class="bi bi-chevron-left me-1"></i
                  >{{ texts.previousPage }}
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="
                    !isSelectingAllLeads &&
                      table.nextPage()
                  "
                  :disabled="
                    !table.getCanNextPage() ||
                    isSelectingAllLeads
                  "
                >
                  {{ texts.nextPage }}<i class="bi bi-chevron-right ms-1"></i>
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="
                    !isSelectingAllLeads &&
                      table.setPageIndex(table.getPageCount() - 1)
                  "
                  :disabled="
                    !table.getCanNextPage() ||
                    isSelectingAllLeads
                  "
                >
                  <i class="bi bi-chevron-bar-right"></i>
                </button>
              </div>
              <div class="d-flex align-items-center">
                <span class="me-2 text-muted small"
                  >{{ texts.pageText }}
                  {{ table.getState().pagination.pageIndex + 1 }}
                  {{ texts.ofText }} {{ table.getPageCount() }}</span
                >
                <select
                  class="form-select form-select-sm"
                  style="width: auto"
                  :value="table.getState().pagination.pageSize"
                  @change="e => !isSelectingAllLeads && table.setPageSize(Number((e.target as HTMLSelectElement).value))"
                  :disabled="isSelectingAllLeads"
                >
                  <option
                    v-for="size in [10, 15, 25, 50, 100]"
                    :key="size"
                    :value="size"
                  >
                    {{ texts.showNum }} {{ size }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch, h, nextTick } from "vue";
import FilterPanelView, {
  type ActiveClientFilters,
  type TabCounts,
  type FilterKey,
} from "@/components/FilterPanelView.vue";
import { useLanguageStore } from '@/stores/languageStore';

import type { Table } from '@tanstack/vue-table';
import { useAuthStore } from "@/stores/authStore";
import { supabase } from "@/services/supabaseClient";
import type { Session } from "@supabase/supabase-js";
import { v4 as uuidv4 } from "uuid";
import {
  useVueTable,
  getCoreRowModel,
  getSortedRowModel,
  createColumnHelper,
  FlexRender,
  type ColumnDef,
  type SortingState,
  type PaginationState,
  type RowSelectionState,
  type Column,
  type CellContext,
  type HeaderContext,
  type Updater,
} from "@tanstack/vue-table";
import type { LeadTab } from "@/types/tabs";
import { Dropdown } from "bootstrap";
import type { Translations } from "@/types/language";

interface Lead {
  id: string;
  created_at: string;
  user_id: string;
  tab: LeadTab | null;
  first_name?: string | null;
  last_name?: string | null;
  name?: string | null;
  job_title?: string | null;
  industry?: string[] | null; // This will still receive the original array from the view
  location?: string | null;
  company_name?: string | null;
  company_size?: number | null;
  phone?: string | null;
  linkedIn_url?: string | null;
  keywords?: string[] | null; // This will still receive the original JSONB array from the view
  email?: string | null;
  notes?: string | null;
  lead_status?: string | null;
  icebreaker?: string | null;
  source_query_criteria?: Record<string, any> | null;
}
interface FilterTag {
  id: string;
  type:
    | "jobTitle"
    | "industry"
    | "location"
    | "companySize"
    | "companyNames"
    | "generalKeywords";
  value: string;
  displayValue: string;
  label: string;
}

const languageStore = useLanguageStore();
const authStore = useAuthStore();

const expandedKeywords = ref<Record<string, boolean>>({});
const MAX_VISIBLE_KEYWORDS = 3;

function toggleKeywordsExpansion(rowId: string) {
  expandedKeywords.value[rowId] = !expandedKeywords.value[rowId];
}

const sidebarCollapsed = ref(false);
const showSearchForm = ref(true);
const currentTab = ref<LeadTab>("new");
const tabCounts = ref<TabCounts>({ new: 0, saved: 0, archived: 0 });
const activeClientFilters = ref<ActiveClientFilters>({});
const naturalLanguageQuery = ref("");
const showAdvancedFilters = ref(false);
const advancedFilterInputs = reactive({
  jobTitle: "",
  industry: "",
  location: "",
  companySize: "",
  companyNames: "",
  generalKeywords: "",
});
const filterTags = ref<FilterTag[]>([]);
const isSearchingLeads = ref(false);
const searchStatus = ref<"success" | "error" | "warning" | "info" | null>(null);
const searchMessage = ref<string | null>(null);
const tableData = ref<Lead[]>([]);
const isLoadingLeads = ref(false);
const initialLoadComplete = ref(false);
const sorting = ref<SortingState>([]);
const pagination = ref<PaginationState>({ pageIndex: 0, pageSize: 15 });
const rowSelection = ref<RowSelectionState>({});
const isProcessingBatch = ref(false);
const batchActionsDropdownToggleRef = ref<HTMLButtonElement | null>(null);
const columnHelper = createColumnHelper<Lead>();

const totalRowCount = ref(0);
const isSelectingAllLeads = ref(false);

const defaultTexts = {
  mainQueryLabel: "Briefly describe the type of prospects you're looking for:",
  mainQueryPlaceholder:
    "e.g., 'Software engineers in fintech startups in London'",
  advancedBtnTextShow: "Advanced Filters",
  advancedBtnTextHide: "Hide Filters",
  jobTitleLabel: "Job Title",
  industryLabel: "Industry",
  locationLabel: "Country/City",
  companySizeLabel: "Company Size",
  companyNamesLabel: "Company Names",
  companyNamesPlaceholder: "e.g., Google, Microsoft, AWS.",
  generalKeywordsLabel: "Keywords",
  generalKeywordsPlaceholder: "e.g., SaaS, AI, cloud computing.",
  addFiltersBtnText: "Add Filters",
  tagAreaLabel: "Selected Filters:",
  removeFilterTooltip: "Remove filter",
  searchLeadsButton: "Find Prospects",
  dashboardTitle: "Prospects Dashboard",
  formDescription: "Define Your Prospect Persona",
  industryPlaceholder: "Select Industry",
  companySizePlaceholder: "Select Company Size",
  leadsListTitle: "Prospects",
  refreshButton: "Refresh",
  loadingLeads: "Loading...",
  colName: "Name",
  colJobTitle: "Job Title",
  colIndustry: "Industry",
  colLocation: "Location",
  colCompanyName: "Company",
  colCompanySize: "Company Size",
  colPhone: "Phone",
  colLinkedIn: "LinkedIn",
  colKeywords: "Keywords",
  colEmail: "Email",
  colNotes: "Notes",
  colCreatedAt: "Date Added",
  colStatus: "Status",
  n8nConfigError: "N8N configuration error. Contact admin.",
  searchLeadsSuccess:
    "Search submitted successfully. Results are in the 'New' tab.",
  alertError: "Error: ",
  alertSuccess: "Success: ",
  alertWarning: "Warning: ",
  userNotAuthMessage: "User not authenticated. Please log in.",
  errorRequired: (fieldName: string) => `${fieldName} is required.`,
  noSearchCriteria: "Please enter search criteria.",
  previousPage: "Previous",
  nextPage: "Next",
  pageText: "Page",
  ofText: "of",
  showNum: "Show",
  accessDeniedMessage: "Access Denied.",
  tabNew: "New",
  tabSaved: "Saved",
  tabArchived: "Archived",
  confirmArchiveUnsaved:
    "You have unsaved leads. Starting a new search will archive them. Proceed?",
  unsavedLeadsArchived: "Unsaved leads moved to 'Archived'.",
  noNewLeadsYet: "Submit a search to find new prospects or check other tabs.",
  noSavedLeads: "No leads saved yet. Save leads from the 'New' tab.",
  noArchivedLeads: "No leads have been archived.",
  noLeadsFound: "No prospects found for this tab.",
  colActions: "Actions",
  actionSaveTooltip: "Save Lead",
  actionArchiveTooltip: "Archive Lead",
  actionRestoreTooltip: "Move to New",
  actionDeleteTooltip: "Delete Lead",
  actionMoveToSavedTooltip: "Move to Saved",
  tooltipSave: "Save",
  tooltipArchive: "Archive",
  tooltipRestore: "Restore",
  tooltipMoveToSaved: "Move to Saved",
  tooltipDelete: "Delete",
  leadSavedSuccess: "Lead saved successfully.",
  leadArchivedSuccess: "Lead archived successfully.",
  leadRestoredSuccess: "Lead moved to 'New' successfully.",
  leadDeletedSuccess: "Lead deleted successfully.",
  leadUpdateError: "Failed to update lead status.",
  leadDeleteError: "Failed to delete lead.",
  autoArchiveError: "Failed to auto-archive unsaved leads.",
  filtersTitle: "Filters",
  tabsTitle: "Lead Categories",
  addFilterPlaceholder: "Add",
  selectFilterPlaceholder: "Select",
  clearAllFiltersButton: "Clear All Filters",
  clearFilterSectionTooltip: "Clear section",
  selectAllPageButton: "Select Page",
  selectAllPageTooltip: "Select all leads on current page",
  selectAllButton: "Select All",
  selectAllTooltip: "Select all matching leads across all pages",
  deselectAllButton: "Deselect All",
  deselectAllPageTooltip: "Deselect all leads on current page",
  batchActionsDropdownTitle: "Actions for Selected",
  batchSaveButton: "Save Selected",
  batchArchiveButton: "Archive Selected",
  batchRestoreButton: "Restore Selected to New",
  batchDeleteButton: "Delete Selected",
  batchMoveToSavedButton: "Move Selected to Saved",
  confirmBatchDelete: (count: number) =>
    `Are you sure you want to permanently delete ${count} selected lead(s)? This action cannot be undone.`,
  noLeadsEligibleForAction: (action: string) =>
    `No selected leads are eligible for ${action}.`,
  batchActionResult: (action: string, success: number, failed: number) =>
    `${action}: ${success} succeeded, ${failed} failed.`,
  searchFormToggleShowTooltip: "Show Search Form",
  searchFormToggleHideTooltip: "Hide Search Form",
  statusNewProspect: "New Prospect",
  statusContacted: "Contacted",
  statusFollowUp: "Follow-up",
  statusReplied: "Replied",
  batchExportCSVButton: "Export Selected to CSV",
  showLessButton: "Show less",
  showMoreButtonText: (count: number) => `... (${count} more)`,
};

const texts = computed((): Translations & typeof defaultTexts => {
  if (
    languageStore &&
    typeof languageStore.texts === "object" &&
    languageStore.texts !== null &&
    Object.keys(languageStore.texts).length > 0
  ) {
    // @ts-ignore
    return { ...defaultTexts, ...languageStore.texts };
  }
  return defaultTexts as Translations & typeof defaultTexts;
});

const companySizeOptionsForFilter = computed(() => [
  { value: "1-10", text: "1-10" },
  { value: "11-50", text: "11-50" },
  { value: "51-200", text: "51-200" },
  { value: "201-500", text: "201-500" },
  { value: "501-1000", text: "501-1000" },
  { value: "1001-5000", text: "1001-5000" },
  { value: "5001-10000", text: "5001-10000" },
  { value: "10001+", text: "10001+" },
]);

const leadStatusOptionsForFilter = computed(() => [
  { value: "New Prospect", text: texts.value.statusNewProspect },
  { value: "Contacted", text: texts.value.statusContacted },
  { value: "Follow-up", text: texts.value.statusFollowUp },
  { value: "Replied", text: texts.value.statusReplied },
]);

const noLeadsMessageForTab = computed(() => {
  switch (currentTab.value) {
    case "new":
      return texts.value.noNewLeadsYet;
    case "saved":
      return texts.value.noSavedLeads;
    case "archived":
      return texts.value.noArchivedLeads;
    default:
      return texts.value.noLeadsFound;
  }
});

const columns = computed<ColumnDef<Lead, any>[]>(() => [
  columnHelper.display({
    id: "select",
    header: ({ table }: HeaderContext<Lead, unknown>) =>
      h("input", {
        type: "checkbox",
        class: "form-check-input",
        style: "cursor: pointer;",
        checked: table.getIsAllPageRowsSelected(),
        indeterminate: table.getIsSomePageRowsSelected(),
        disabled:
          isProcessingBatch.value ||
          isSelectingAllLeads.value ||
          table.getRowModel().rows.length === 0,
        onChange: (e: Event) => {
          if (isProcessingBatch.value || isSelectingAllLeads.value) return;
          if ((e.target as HTMLInputElement).checked) selectAllOnPage();
          else deselectAllOnPage();
        },
        title: texts.value.selectAllPageTooltip,
      }),
    cell: ({ row }: CellContext<Lead, unknown>) =>
      h("input", {
        type: "checkbox",
        class: "form-check-input",
        style: "cursor: pointer;",
        checked: row.getIsSelected(),
        disabled:
          !row.getCanSelect() ||
          isProcessingBatch.value ||
          isSelectingAllLeads.value,
        onChange: row.getToggleSelectedHandler(),
      }),
    size: 60,
    meta: {
      style: {
        position: "sticky",
        left: "0px",
        width: "60px",
        minWidth: "60px",
        textAlign: "center",
        verticalAlign: "middle",
        zIndex: "18",
        backgroundColor: "var(--card-bg-current)",
        borderRight: "1px solid var(--border-color-current)",
      },
    },
  }),
  columnHelper.accessor("name", {
    id: "name",
    header: () => texts.value.colName,
    cell: (info: CellContext<Lead, Lead["name"]>) =>
      info.getValue() ||
      `${info.row.original.first_name || ""} ${
        info.row.original.last_name || ""
      }`.trim() ||
      "N/A",
    enableSorting: true,
    size: 144,
    meta: {
      style: {
        position: "sticky",
        left: "60px",
        minWidth: "144px",
        width: "144px",
        zIndex: "17",
        backgroundColor: "var(--card-bg-current)",
        borderRight: "1px solid var(--border-color-current)",
      },
    },
  }),
  columnHelper.accessor("job_title", {
    id: "job_title",
    header: () => texts.value.colJobTitle,
    cell: (info: CellContext<Lead, Lead["job_title"]>) =>
      info.getValue() || "N/A",
    enableSorting: true,
    size: 200,
    meta: { style: { minWidth: "200px", width: "200px" } },
  }),
  columnHelper.accessor("industry", {
    id: "industry",
    header: () => texts.value.colIndustry,
    cell: (info: CellContext<Lead, Lead["industry"]>) => {
      const industries = info.getValue();
      if (Array.isArray(industries) && industries.length > 0) {
        return h(
          "div",
          { style: "max-width: 200px; white-space: normal;" },
          industries.map((ind) =>
            h(
              "span",
              { class: "badge bg-info text-dark me-1 mb-1" },
              String(ind)
            )
          )
        );
      }
      return "N/A";
    },
    enableSorting: true,
    size: 160,
    meta: {
      style: { minWidth: "160px", width: "160px", whiteSpace: "normal" },
    },
  }),
  columnHelper.accessor("location", {
    id: "location",
    header: () => texts.value.colLocation,
    cell: (info: CellContext<Lead, Lead["location"]>) =>
      info.getValue() || "N/A",
    enableSorting: true,
    size: 150,
    meta: { style: { minWidth: "150px", width: "150px" } },
  }),
  columnHelper.accessor("company_name", {
    id: "company_name",
    header: () => texts.value.colCompanyName,
    cell: (info: CellContext<Lead, Lead["company_name"]>) =>
      info.getValue() || "N/A",
    enableSorting: true,
    size: 180,
    meta: { style: { minWidth: "180px", width: "180px" } },
  }),
  columnHelper.accessor("company_size", {
    id: "company_size",
    header: () => texts.value.colCompanySize,
    cell: (info: CellContext<Lead, Lead["company_size"]>) =>
      info.getValue() ?? "N/A",
    enableSorting: true,
    size: 180,
    meta: {
      style: { minWidth: "110px", width: "110px", whiteSpace: "normal" },
    },
  }),
  columnHelper.accessor("phone", {
    id: "phone",
    header: () => texts.value.colPhone,
    cell: (info: CellContext<Lead, Lead["phone"]>) => info.getValue() || "N/A",
    enableSorting: false,
    size: 140,
    meta: { style: { minWidth: "140px", width: "140px" } },
  }),
  columnHelper.accessor("linkedIn_url", {
    id: "linkedIn_url",
    header: () => texts.value.colLinkedIn,
    cell: (info: CellContext<Lead, Lead["linkedIn_url"]>) => {
      const url = info.getValue();
      return url
        ? h(
            "a",
            {
              href: url,
              target: "_blank",
              rel: "noopener noreferrer",
              class: "text-primary",
              title: url,
            },
            "Profile"
          )
        : "N/A";
    },
    enableSorting: false,
    size: 80,
    meta: { style: { minWidth: "80px", width: "80px" } },
  }),
  columnHelper.accessor("keywords", {
    id: "keywords",
    header: () => texts.value.colKeywords,
    cell: ({ row }: CellContext<Lead, Lead["keywords"]>) => {
      const leadRawKeywords = row.original.keywords;
      const rowId = row.id;
      let actualKeywordsArray: string[] = [];
      if (Array.isArray(leadRawKeywords)) {
        actualKeywordsArray = leadRawKeywords
          .map((kw) => String(kw).trim())
          .filter(Boolean);
      }
      if (actualKeywordsArray.length === 0) return "N/A";
      const isExpanded = !!expandedKeywords.value[rowId];
      const keywordsToDisplay = isExpanded
        ? actualKeywordsArray
        : actualKeywordsArray.slice(0, MAX_VISIBLE_KEYWORDS);
      const hasMoreKeywords = actualKeywordsArray.length > MAX_VISIBLE_KEYWORDS;
      const keywordElements = keywordsToDisplay.map((keyword) =>
        h(
          "span",
          { class: "badge bg-secondary me-1 mb-1 keyword-tag" },
          keyword
        )
      );
      const toggleButton = hasMoreKeywords
        ? h(
            "button",
            {
              class: "btn btn-link btn-sm p-0 ms-1 show-more-keywords-btn",
              type: "button",
              onClick: (event: MouseEvent) => {
                event.stopPropagation();
                toggleKeywordsExpansion(rowId);
              },
            },
            isExpanded
              ? texts.value.showLessButton
              : texts.value.showMoreButtonText(
                  actualKeywordsArray.length - MAX_VISIBLE_KEYWORDS
                )
          )
        : null;
      return h(
        "div",
        { class: "keywords-cell-container" },
        [...keywordElements, toggleButton].filter(Boolean)
      );
    },
    enableSorting: false,
    size: 250,
    meta: {
      style: { minWidth: "250px", width: "250px", whiteSpace: "normal" },
    },
  }),
  columnHelper.accessor("email", {
    id: "email",
    header: () => texts.value.colEmail,
    cell: (info: CellContext<Lead, Lead["email"]>) => info.getValue() || "N/A",
    enableSorting: true,
    size: 220,
    meta: { style: { minWidth: "220px", width: "220px" } },
  }),
  columnHelper.accessor("notes", {
    id: "notes",
    header: () => texts.value.colNotes,
    cell: (info: CellContext<Lead, Lead["notes"]>) => info.getValue() || "N/A",
    enableSorting: false,
    size: 250,
    meta: { style: { minWidth: "250px", width: "250px" } },
  }),
  columnHelper.accessor("created_at", {
    id: "created_at",
    header: () => texts.value.colCreatedAt,
    cell: (info: CellContext<Lead, Lead["created_at"]>) =>
      info.getValue() ? new Date(info.getValue()).toLocaleDateString() : "N/A",
    enableSorting: true,
    size: 100,
    meta: { style: { minWidth: "100px", width: "100px" } },
  }),
  columnHelper.display({
    id: "actions",
    header: () => texts.value.colActions,
    cell: (info: CellContext<Lead, unknown>) => {
      const lead = info.row.original;
      const buttons = [];
      if (currentTab.value === "new" && lead.tab === "new") {
        buttons.push(
          h(
            "button",
            {
              class: "btn btn-sm btn-outline-success",
              title: texts.value.tooltipSave,
              disabled: isProcessingBatch.value || isSelectingAllLeads.value,
              onClick: () =>
                !(isProcessingBatch.value || isSelectingAllLeads.value) &&
                updateLeadTab(lead.id, "saved"),
            },
            [h("i", { class: "bi bi-bookmark-check" })]
          )
        );
        buttons.push(
          h(
            "button",
            {
              onClick: () =>
                !(isProcessingBatch.value || isSelectingAllLeads.value) &&
                updateLeadTab(lead.id, "archived"),
              class: `btn btn-sm btn-outline-warning${buttons.length > 0 ? ' ms-1' : ''}`,
              disabled: isProcessingBatch.value || isSelectingAllLeads.value,
              title: texts.value.tooltipArchive,
            },
            [h("i", { class: "bi bi-archive" })]
          )
        );
      } else if (currentTab.value === "saved" && lead.tab === "saved") {
        buttons.push(
          h(
            "button",
            {
              onClick: () =>
                !(isProcessingBatch.value || isSelectingAllLeads.value) &&
                updateLeadTab(lead.id, "new"),
              class: "btn btn-sm btn-outline-secondary",
              title: texts.value.tooltipRestore,
              disabled: isProcessingBatch.value || isSelectingAllLeads.value,
            },
            [h("i", { class: "bi bi-arrow-counterclockwise" })]
          )
        );
        buttons.push(
          h(
            "button",
            {
              onClick: () =>
                !(isProcessingBatch.value || isSelectingAllLeads.value) &&
                updateLeadTab(lead.id, "archived"),
              class: `btn btn-sm btn-outline-warning${buttons.length > 0 ? ' ms-1' : ''}`,
              disabled: isProcessingBatch.value || isSelectingAllLeads.value,
              title: texts.value.tooltipArchive,
            },
            [h("i", { class: "bi bi-archive" })]
          )
        );
      } else if (currentTab.value === "archived" && lead.tab === "archived") {
        buttons.push(
          h(
            "button",
            {
              onClick: () =>
                !(isProcessingBatch.value || isSelectingAllLeads.value) &&
                updateLeadTab(lead.id, "saved"),
              class: "btn btn-sm btn-outline-secondary",
              disabled: isProcessingBatch.value || isSelectingAllLeads.value,
              title: texts.value.tooltipMoveToSaved,
            },
            [h("i", { class: "bi bi-bookmark-plus" })]
          )
        );
        buttons.push(
          h(
            "button",
            {
              onClick: () =>
                !(isProcessingBatch.value || isSelectingAllLeads.value) &&
                deleteLead(lead.id),
              class: `btn btn-sm btn-outline-danger${buttons.length > 0 ? ' ms-1' : ''}`,
              disabled: isProcessingBatch.value || isSelectingAllLeads.value,
                            title: texts.value.tooltipDelete,
            },
            [h("i", { class: "bi bi-trash" })]
          )
        );
      }
      return h(
        "div",
        {
          class:
            "btn-group btn-group-sm table-action-buttons d-flex justify-content-center",
        },
        buttons
      );
    },
    size: 150,
    meta: {
      style: {
        position: "sticky",
        right: "0px",
        width: "150px",
        minWidth: "150px",
        textAlign: "center",
        verticalAlign: "middle",
        zIndex: "18",
        backgroundColor: "var(--card-bg-current)",
        borderLeft: "1px solid var(--border-color-current)",
      },
    },
  }),
]);

function getColumnStyle(column: Column<Lead, unknown>) {
  // Ensure column and its properties exist to prevent null reference errors
  if (!column || !column.columnDef) {
    return {};
  }
  
  const baseStyle: Record<string, string> = {
    "user-select":
      column.getCanSort() &&
      !isProcessingBatch.value &&
      !isSelectingAllLeads.value
        ? "pointer"
        : "none",
    verticalAlign: "middle",
  };
  
  // Safely access column size with fallback
  const columnSize = column.columnDef.size || 100;
  
  if (!column.columnDef.meta?.style?.width)
    baseStyle.width = `${columnSize}px`;
  if (!column.columnDef.meta?.style?.minWidth)
    baseStyle.minWidth = `${columnSize}px`;
    
  const metaStyle = column.columnDef.meta?.style || {};
  
  // Create a safe copy of styles, handling CSS custom properties properly
  const validStyle: Record<string, string> = {};
  
  try {
    Object.entries({ ...baseStyle, ...metaStyle }).forEach(([key, value]) => {
      // Validate key: must be a valid CSS property name
      if (key && typeof key === 'string' && key.trim() !== '' && value != null) {
        // Convert camelCase to kebab-case for CSS properties
        const cssKey = key.replace(/([A-Z])/g, '-$1').toLowerCase();
        
        // Ensure value is a string and handle CSS custom properties
        let cssValue = String(value);
        
        // Don't modify CSS custom properties (var(--property-name))
        if (!cssValue.startsWith('var(')) {
          // Only remove quotes from non-CSS-custom-property values
          cssValue = cssValue.replace(/["']/g, '');
        }
        
        if (cssValue.trim() !== '') {
          validStyle[cssKey] = cssValue;
        }
      }
    });
  } catch (error) {
    console.warn('Error processing column styles:', error);
    // Return minimal safe styles on error
    return {
      'vertical-align': 'middle',
      'user-select': 'none'
    };
  }
  
  return validStyle;
}
const table: Table<Lead> = useVueTable({
  get data() {
    return tableData.value || [];
  },
    columns: columns.value,
    state: {
      get sorting() {
        return sorting.value || [];
      },
      get pagination() {
        return pagination.value || { pageIndex: 0, pageSize: 15 };
      },
      get rowSelection() {
        return rowSelection.value || {};
      },
    },
  enableRowSelection: true,
  onRowSelectionChange: (updater: Updater<RowSelectionState>) => {
    if (isProcessingBatch.value || isSelectingAllLeads.value) return;
    rowSelection.value =
      typeof updater === "function" ? updater(rowSelection.value) : updater;
  },
  onSortingChange: (updater: Updater<SortingState>) => {
    if (isProcessingBatch.value || isSelectingAllLeads.value) return;
    const oldSortingString = JSON.stringify(sorting.value);
    const newSortingState =
      typeof updater === "function" ? updater(sorting.value) : updater;
    if (JSON.stringify(newSortingState) !== oldSortingString) {
      sorting.value = newSortingState;
      // Clear row selection to prevent race condition when data updates
      rowSelection.value = {};
      fetchLeadsForCurrentUser(true);
    } else {
      sorting.value = newSortingState;
    }
  },
  onPaginationChange: (updater: Updater<PaginationState>) => {
    if (isProcessingBatch.value || isSelectingAllLeads.value) return;
    const oldPageIndex = pagination.value.pageIndex;
    const oldPageSize = pagination.value.pageSize;
    const newPaginationState =
      typeof updater === "function" ? updater(pagination.value) : updater;
    if (
      newPaginationState.pageIndex !== oldPageIndex ||
      newPaginationState.pageSize !== oldPageSize
    ) {
      pagination.value = newPaginationState;
      // Clear row selection to prevent race condition when data updates
      rowSelection.value = {};
      fetchLeadsForCurrentUser(true);
    } else {
      pagination.value = newPaginationState;
    }
  },
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  manualPagination: true,
  manualSorting: true,
  get rowCount() {
    return totalRowCount.value;
  },
  getRowId: (row: Lead) => row.id,
});
const selectAllOnPage = () => {
  if (isProcessingBatch.value || isSelectingAllLeads.value) return;
  table.toggleAllPageRowsSelected(true);
};
const deselectAllOnPage = () => {
  if (isProcessingBatch.value || isSelectingAllLeads.value) return;
  table.toggleAllPageRowsSelected(false);
};
function parseCompanySizeRange(rangeString: string): {
  min?: number;
  max?: number;
} {
  if (rangeString.endsWith("+")) {
    const min = parseInt(rangeString.slice(0, -1), 10);
    return isNaN(min) ? {} : { min };
  }
  const parts = rangeString.split("-").map((p) => parseInt(p.trim(), 10));
  if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
    return { min: parts[0], max: parts[1] };
  }
  return {};
}

// Corrected mapping: keys match FilterKey (received from FilterPanelView), values are view column names
const COLUMN_MAPPING: Record<FilterKey, string> = {
    job_title: 'job_title', // Matches directly
    industry: 'industry_text', // Maps to the new text column in the view
    location: 'location', // Matches directly
    company_size: 'company_size', // Matches directly
    company_name: 'company_name', // Maps to company_name (your filter for companyNames)
    keywords: 'keywords_text', // Maps to the new text column in the view
    lead_status: 'lead_status', // Matches directly
};

const selectAllMatchingLeads = async () => {
  if (isProcessingBatch.value || isSelectingAllLeads.value) return;
  isSelectingAllLeads.value = true;
  searchMessage.value = "Selecting all matching leads...";
  searchStatus.value = "info";
  try {
    const user = authStore.user;
    if (!user) {
      searchMessage.value = texts.value.userNotAuthMessage;
      searchStatus.value = "error";
      return;
    }
    // IMPORTANT: Query the new view instead of the original table
    let query = supabase
      .from("leads_search_view") // Changed from "leads" to your new view name
      .select("id") // Only fetch IDs
      .eq("user_id", user.id)
      .eq("tab", currentTab.value);

    // Apply active client filters
    Object.entries(activeClientFilters.value).forEach(([filterKey, values]) => {
      if (Array.isArray(values) && values.length > 0) {
        const typedFilterKey = filterKey as FilterKey;
        // Use the mapped column name for the Supabase query
        const actualColumnName = COLUMN_MAPPING[typedFilterKey];
        
        if (!actualColumnName) {
            console.warn(`selectAllMatchingLeads: No column mapping found for filter key: ${typedFilterKey}`);
            return; // Skip this filter if no mapping found
        }

        switch (typedFilterKey) { // Switch on the original filter key type
          case "lead_status":
            query = query.in(actualColumnName, values);
            break;
          case "company_size":
            // This logic is already correct for numeric range filtering
            const companySizeOrFilters: string[] = [];
            values.forEach((rangeStr) => {
              const { min, max } = parseCompanySizeRange(rangeStr);
              if (min !== undefined && max !== undefined) {
                companySizeOrFilters.push(
                  `and(${actualColumnName}.gte.${min},${actualColumnName}.lte.${max})`
                );
              } else if (min !== undefined) {
                companySizeOrFilters.push(`${actualColumnName}.gte.${min}`);
              }
            });
            if (companySizeOrFilters.length > 0) {
              query = query.or(companySizeOrFilters.join(","));
            }
            break;
          // Group all fuzzy text search fields here
          case "job_title":
          case "location":
          case "company_name":
          case "industry":
          case "keywords":
            // For these fields, now use ilike on the new text columns from the view (or original text columns)
            const orFuzzyConditions = values
              .map((val) => `${actualColumnName}.ilike.%${String(val).trim()}%`)
              .join(",");
            if (orFuzzyConditions) query = query.or(orFuzzyConditions);
            break;
          default:
            // This default should ideally never be hit if all FilterKey types are covered
            console.warn(
              `selectAllMatchingLeads: Unhandled filter key type in switch: ${typedFilterKey}. Please add it to COLUMN_MAPPING and switch cases.`
            );
            break;
        }
      }
    });
    const { data: leadIds, error } = await query;
    if (error) {
      console.error(
        "Error during selectAllMatchingLeads query:",
        error,
        "Query filters:",
        JSON.stringify(activeClientFilters.value)
      );
      throw error;
    }
    const newSelection: RowSelectionState = {};
    if (leadIds)
      leadIds.forEach((lead) => {
        newSelection[lead.id] = true;
      });
    rowSelection.value = newSelection;
    searchMessage.value = `Selected ${leadIds?.length || 0} leads.`;
    searchStatus.value = "success";
  } catch (error: any) {
    console.error("Error selecting all filtered leads:", error);
    searchMessage.value = `Error selecting all leads: ${error.message}`;
    searchStatus.value = "error";
  } finally {
    isSelectingAllLeads.value = false;
  }
};

const deselectAllGlobalLeads = () => {
  if (isProcessingBatch.value || isSelectingAllLeads.value) return;
  rowSelection.value = {};
  searchMessage.value = "All leads deselected.";
  searchStatus.value = "info";
};
const selectedRowCount = computed(() => Object.keys(rowSelection.value).length);
const allFilteredLeadsSelected = computed(
  () =>
    totalRowCount.value > 0 && selectedRowCount.value === totalRowCount.value
);
const canBatchSave = computed(
  () =>
    currentTab.value === "new" &&
    !isProcessingBatch.value &&
    !isSelectingAllLeads.value &&
    selectedRowCount.value > 0 &&
    Object.keys(rowSelection.value).some((id) =>
      tableData.value.some((lead) => lead.id === id && lead.tab === "new")
    )
);
const canBatchArchiveNew = computed(
  () =>
    currentTab.value === "new" &&
    !isProcessingBatch.value &&
    !isSelectingAllLeads.value &&
    selectedRowCount.value > 0 &&
    Object.keys(rowSelection.value).some((id) =>
      tableData.value.some((lead) => lead.id === id && lead.tab === "new")
    )
);
const canBatchRestoreToNewFromSaved = computed(
  () =>
    currentTab.value === "saved" &&
    !isProcessingBatch.value &&
    !isSelectingAllLeads.value &&
    selectedRowCount.value > 0 &&
    Object.keys(rowSelection.value).some((id) =>
      tableData.value.some((lead) => lead.id === id && lead.tab === "saved")
    )
);
const canBatchArchiveSaved = computed(
  () =>
    currentTab.value === "saved" &&
    !isProcessingBatch.value &&
    !isSelectingAllLeads.value &&
    selectedRowCount.value > 0 &&
    Object.keys(rowSelection.value).some((id) =>
      tableData.value.some((lead) => lead.id === id && lead.tab === "saved")
    )
);
const canBatchMoveToSaved = computed(
  () =>
    currentTab.value === "archived" &&
    !isProcessingBatch.value &&
    !isSelectingAllLeads.value &&
    selectedRowCount.value > 0 &&
    Object.keys(rowSelection.value).some((id) =>
      tableData.value.some((lead) => lead.id === id && lead.tab === "archived")
    )
);
const canBatchDeleteArchived = computed(
  () =>
    currentTab.value === "archived" &&
    !isProcessingBatch.value &&
    !isSelectingAllLeads.value &&
    selectedRowCount.value > 0
);

const batchProcessLeads = async (
  targetTabOrAction: LeadTab | "delete",
  actionNameKey: keyof Pick<
    Translations,
    |
      "confirmBatchSave"
    |
      "confirmBatchArchive"
    |
      "confirmBatchRestore"
    |
      "confirmBatchDelete"
    |
      "confirmBatchMoveToSaved"
  > | null,
  filterFn: (lead: Lead) => boolean,
  operationFn: (
    leadId: string,
    target?: LeadTab
  ) => Promise<{ success: boolean; error?: any }>
) => {
  if (isProcessingBatch.value || isSelectingAllLeads.value) return;

  isProcessingBatch.value = true; // Set at the beginning of the entire process

  try { // Outer try block to ensure finally always runs
    const selectedLeadIds = Object.keys(rowSelection.value);
    if (selectedLeadIds.length === 0) {
      searchMessage.value = texts.value.noLeadsEligibleForAction("process");
      searchStatus.value = "warning";
      return; // Early exit
    }
    const user = authStore.user;
    if (!user?.id) {
      searchMessage.value = texts.value.userNotAuthMessage;
      searchStatus.value = "error";
      return; // Early exit
    }

    let leadsToProcess: Lead[] = [];
    try { // Inner try-catch for Supabase fetch
      const { data, error } = await supabase
        .from("leads_search_view") // Batch operations should use the same view as regular queries
        .select(selectFields) // Fixed typo: was selectFeellslds
        .in("id", selectedLeadIds)
        .eq("user_id", user.id);
      if (error) throw error;
      leadsToProcess = data || [];
    } catch (e: any) {
      console.error("Error during batch operation leads fetch:", e);
      searchMessage.value =
        texts.value.alertError +
        `Batch operation failed during fetch: ${e.message}`;
      searchStatus.value = "error";
      return; // Exit early on inner error
    }

    if (filterFn) {
      const leadsBeforeFilter = leadsToProcess.length;
      leadsToProcess = leadsToProcess.filter(filterFn);
      if (leadsBeforeFilter !== leadsToProcess.length) {
         console.log(`Batch Process: Filtered leads. Before: ${leadsBeforeFilter}, After: ${leadsToProcess.length}`);
      }
    }

    if (actionNameKey) {
      const actionNameForNoLeadsMsg = actionNameKey
        .replace("confirmBatch", "")
        .toLowerCase();
      if (leadsToProcess.length === 0 && targetTabOrAction !== "delete") {
        searchMessage.value = texts.value.noLeadsEligibleForAction(
          actionNameForNoLeadsMsg
        );
        searchStatus.value = "warning";
        return; // Early exit
      }
      const confirmMessageFn = texts.value[actionNameKey] as (
        count: number
      ) => string;
      if (!confirm(confirmMessageFn(leadsToProcess.length))) return; // Early exit (user cancelled)
    } else if (leadsToProcess.length === 0) {
      searchMessage.value = texts.value.noLeadsEligibleForAction("process");
      searchStatus.value = "warning";
      return; // Early exit if no leads and no confirmation
    }

    const processingActionName = actionNameKey ? actionNameKey.replace("confirmBatch", "") : targetTabOrAction;
    let successCount = 0;
    let errorCount = 0;
    const totalLeads = leadsToProcess.length;
    
    // Process leads in smaller batches to keep UI responsive
    const batchSize = 5;
    const results: PromiseSettledResult<any>[] = [];
    
    for (let i = 0; i < totalLeads; i += batchSize) {
      const currentBatch = leadsToProcess.slice(i, i + batchSize);
      const processed = i + currentBatch.length;
      
      // Update progress message
      searchMessage.value = `Processing ${processingActionName} batch... (${processed}/${totalLeads} leads)`;
      searchStatus.value = null;
      
      // Allow UI to update
      await nextTick();
      
      // Process current batch
      const batchResults = await Promise.allSettled(
        currentBatch.map((lead: Lead) =>
          operationFn(
            lead.id,
            targetTabOrAction !== "delete" ? targetTabOrAction : undefined
          )
        )
      );
      
      results.push(...batchResults);
      
      // Small delay to keep UI responsive
      await new Promise(resolve => setTimeout(resolve, 50));
    }

    results.forEach((result, index) => {
      const leadProcessed = leadsToProcess[index];
      if (
        result.status === "fulfilled" &&
        result.value &&
        result.value.success
      ) {
        successCount++;
      } else {
        errorCount++;
        console.error(
          `Batch ${processingActionName} error for lead ID ${leadProcessed?.id}:`,
          result.status === "rejected" ? result.reason : result.value
        );
      }
    });

    searchMessage.value = texts.value.batchActionResult(
      processingActionName,
      successCount,
      errorCount
    );
    searchStatus.value =
      errorCount > 0 ? (successCount > 0 ? "warning" : "error") : "success";
    
    // Clear row selection BEFORE fetching new data to prevent race condition
    rowSelection.value = {};
    
    try {
      // Force UI update before fetching new data
      await nextTick();
      
      // Force table to re-render by triggering a state change
      if (table) {
        table.resetRowSelection();
      }
      
      // Force a complete refresh of the current tab data
      pagination.value.pageIndex = 0;
      sorting.value = [];
      activeClientFilters.value = {};
      
      // Allow UI to stabilize before fetching new data
      await nextTick();
      
      // Fetch updated data and counts
      await fetchLeadsForCurrentUser(true);
      await fetchTabCounts(authStore.user?.id);
      
      // Final UI update
      await nextTick();
      
    } catch (refreshError: any) {
      console.error('Error during data refresh:', refreshError);
      // Fallback: simple data refresh without complex state manipulation
      try {
        await fetchLeadsForCurrentUser(true);
        await fetchTabCounts(authStore.user?.id);
      } catch (fallbackError: any) {
        console.error('Fallback refresh also failed:', fallbackError);
      }
    }
    
    console.log('Batch operation completed, data refreshed');
    console.log('Current table data count:', tableData.value.length);
    console.log('Current tab counts:', tabCounts.value);
    console.log('Current tab:', currentTab.value);
    console.log('Row selection state:', rowSelection.value);

  } catch (error: any) { // Catch any unexpected errors from the outer try block
    console.error("Unexpected error in batchProcessLeads:", error);
    if (!searchMessage.value) { // Only set if no specific message was already set
      searchMessage.value = texts.value.alertError + (error instanceof Error ? error.message : String(error));
      searchStatus.value = "error";
    }
  } finally {
    isProcessingBatch.value = false; // Always reset this flag when the function exits
  }
};
const batchSaveSelected = () =>
  batchProcessLeads(
    "saved",
    null,
    (lead) => lead.tab === "new",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchArchiveSelected = () =>
  batchProcessLeads(
    "archived",
    null,
    (lead) =>
      currentTab.value === "new" ? lead.tab === "new" : lead.tab === "saved",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchRestoreSelected = () =>
  batchProcessLeads(
    "new",
    null,
    (lead) => lead.tab === "saved",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchMoveToSavedSelected = () =>
  batchProcessLeads(
    "saved",
    null,
    (lead) => lead.tab === "archived",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchDeleteSelected = () =>
  batchProcessLeads(
    "delete",
    "confirmBatchDelete",
    (lead) => lead.tab === "archived",
    (leadId) => deleteLead(leadId, true)
  );
const exportSelectedToCSV = () => {
  if (
    isProcessingBatch.value ||
    selectedRowCount.value === 0 ||
    isSelectingAllLeads.value
  ) {
    searchMessage.value = "No leads to export.";
    searchStatus.value = "warning";
    return;
  }
  const selectedLeadIds = Object.keys(rowSelection.value);
  if (selectedLeadIds.length === 0) {
    searchMessage.value = "No leads to export.";
    searchStatus.value = "warning";
    return;
  }
  const fetchLeadsForExport = async () => {
    const user = authStore.user;
    if (!user?.id) {
      searchMessage.value = texts.value.userNotAuthMessage;
      searchStatus.value = "error";
      return [];
    }
    try {
      // For export, fetch from the view to get the same data structure as displayed
      const { data, error } = await supabase
        .from("leads_search_view") // Use view to access industry_text and keywords_text
        .select(selectFields)
        .in("id", selectedLeadIds)
        .eq("user_id", user.id);
      if (error) throw error;
      return data || [];
    } catch (e: any) {
      searchMessage.value =
        texts.value.alertError + `CSV export failed: ${e.message}`;
      searchStatus.value = "error";
      return [];
    }
  };
  fetchLeadsForExport()
    .then((leadsToExportData: Lead[] | undefined) => {
      if (!leadsToExportData || leadsToExportData.length === 0) {
        searchMessage.value = "No leads to export.";
        searchStatus.value = "warning";
        return;
      }
      const headers = [
        "ID",
        "Date Added",
        "Tab",
        "Status",
        "First Name",
        "Last Name",
        "Full Name",
        "Job Title",
        "Industry",
        "Location",
        "Company Name",
        "Company Size",
        "Phone",
        "LinkedIn URL",
        "Keywords",
        "Email",
        "Notes",
        "Icebreaker",
        "Source Query Criteria",
      ];
      const csvRows: string[] = [headers.join(",")];
      const formatCSVCell = (value: any): string => {
        if (value === null || typeof value === "undefined") return "";
        let stringValue = String(value);
        if (Array.isArray(value))
          stringValue = value
            .map((item) => String(item).replace(/"/g, '""'))
            .join("; ");
        else if (typeof value === "object" && value !== null) {
          try {
            stringValue = JSON.stringify(value);
          } catch (e) {
            stringValue = "[Object]";
          }
        }
        if (
          stringValue.includes('"') ||
          stringValue.includes(",") ||
          stringValue.includes("\n") ||
          stringValue.includes("\r")
        )
          return `"${stringValue.replace(/"/g, '""')}"`;
        return stringValue;
      };
      leadsToExportData.forEach((lead) => {
        const row = [
          formatCSVCell(lead.id),
          formatCSVCell(
            lead.created_at ? new Date(lead.created_at).toISOString() : ""
          ),
          formatCSVCell(lead.tab),
          formatCSVCell(lead.lead_status),
          formatCSVCell(lead.first_name),
          formatCSVCell(lead.last_name),
          formatCSVCell(
            lead.name ||
              (typeof lead.first_name === "string" ? lead.first_name : "") +
                (typeof lead.last_name === "string" ? " " + lead.last_name : "")
          ),
          formatCSVCell(lead.job_title),
          formatCSVCell(lead.industry), // Will export original array
          formatCSVCell(lead.location),
          formatCSVCell(lead.company_name),
          formatCSVCell(lead.company_size),
          formatCSVCell(lead.phone),
          formatCSVCell(lead.linkedIn_url),
          formatCSVCell(lead.keywords), // Will export original JSONB
          formatCSVCell(lead.email),
          formatCSVCell(lead.notes),
          formatCSVCell(lead.icebreaker),
          formatCSVCell(lead.source_query_criteria),
        ];
        csvRows.push(row.join(","));
      });
      const csvString = csvRows.join("\r\n");
      const blob = new Blob([`\uFEFF${csvString}`], {
        type: "text/csv;charset=utf-8;",
      });
      const link = document.createElement("a");
      if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        const timestamp = new Date()
          .toISOString()
          .slice(0, 19)
          .replace(/[-:T]/g, "");
        link.setAttribute("href", url);
        link.setAttribute("download", `leads_export_${timestamp}.csv`);
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      } else {
        const encodedUri = encodeURI(
          "data:text/csv;charset=utf-8," + `\uFEFF${csvString}`
        );
        const newWindow = window.open(encodedUri);
        if (!newWindow) alert("Could not open window.");
      }
      searchMessage.value = `Exported ${leadsToExportData.length} leads to CSV.`;
      searchStatus.value = "success";
      rowSelection.value = {};
    })
    .catch((e) => {
      if (!searchMessage.value) {
        searchMessage.value =
          texts.value.alertError +
          (e.message || "Unknown error during export.");
      }
      searchStatus.value = "error";
    });
};
async function updateLeadTab(
  leadId: string,
  newTab: LeadTab,
  isBatchOperation: boolean = false
): Promise<{
  success: boolean;
  leadId?: string;
  newTab?: LeadTab;
  error?: any;
}> {
  if (!isBatchOperation) {
    isProcessingBatch.value = true;
    if (searchStatus.value !== "error") {
      searchMessage.value = null;
      searchStatus.value = null;
    }
  }
  try {
    // Updates always target the original table
    const { error } = await supabase
      .from("leads")
      .update({ tab: newTab })
      .eq("id", leadId);
    if (error) throw error;
    if (!isBatchOperation) {
      switch (newTab) {
        case "saved":
          searchMessage.value = texts.value.leadSavedSuccess;
          break;
        case "archived":
          searchMessage.value = texts.value.leadArchivedSuccess;
          break;
        case "new":
          searchMessage.value = texts.value.leadRestoredSuccess;
          break;
      }
      searchStatus.value = "success";
      // Clear the specific row selection and fetch updated data
      const currentSelection = { ...rowSelection.value };
      if (currentSelection[leadId]) {
        delete currentSelection[leadId];
        rowSelection.value = currentSelection;
      }
      await fetchLeadsForCurrentUser(true);
      await fetchTabCounts(authStore.user?.id);
    }
    return { success: true, leadId, newTab, error: undefined };
  } catch (error: any) {
    if (!isBatchOperation) {
      searchMessage.value = texts.value.leadUpdateError + ` (${error.message})`;
      searchStatus.value = "error";
    }
    return { success: false, leadId, newTab, error };
  } finally {
    if (!isBatchOperation) isProcessingBatch.value = false;
  }
}
async function deleteLead(
  leadId: string,
  isBatchOperation: boolean = false
): Promise<{ success: boolean; error?: any }> {
  if (!isBatchOperation) {
    isProcessingBatch.value = true;
    if (searchStatus.value !== "error") {
      searchMessage.value = null;
      searchStatus.value = null;
    }
  }
  try {
    // Deletes always target the original table
    const { error } = await supabase.from("leads").delete().eq("id", leadId);
    if (error) throw error;
    if (!isBatchOperation) {
      searchMessage.value = texts.value.leadDeletedSuccess;
      searchStatus.value = "success";
      
      // Clear the specific row selection and fetch updated data
      const currentSelection = { ...rowSelection.value };
      if (currentSelection[leadId]) {
        delete currentSelection[leadId];
        rowSelection.value = currentSelection;
      }
      await fetchLeadsForCurrentUser(true);
      await fetchTabCounts(authStore.user?.id);
    }
    return { success: true, error: undefined };
  } catch (error: any) {
    if (!isBatchOperation) {
      searchMessage.value = texts.value.leadDeleteError + ` (${error.message})`;
      searchStatus.value = "error";
    }
    return { success: false, error };
  } finally {
    if (!isBatchOperation) isProcessingBatch.value = false;
  }
}
function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value;
}
function toggleSearchForm() {
  showSearchForm.value = !showSearchForm.value;
}
watch(
  () => languageStore.currentLang,
  () => {}
);
watch(
  () => authStore.user,
  async (newUser, oldUser) => {
    if (newUser && newUser.id !== oldUser?.id) {
      currentTab.value = "new";
      pagination.value.pageIndex = 0;
      sorting.value = [];
      rowSelection.value = {};
      tableData.value = [];
      totalRowCount.value = 0;
      initialLoadComplete.value = false;
      activeClientFilters.value = {};
      await fetchTabCounts(newUser.id);
      await fetchLeadsForCurrentUser(true);
    } else if (!newUser && oldUser) {
      await archiveUnsavedLeads(oldUser.id);
      tableData.value = [];
      rowSelection.value = {};
      totalRowCount.value = 0;
      initialLoadComplete.value = false;
      pagination.value.pageIndex = 0;
      sorting.value = [];
      currentTab.value = "new";
      searchMessage.value = null;
      searchStatus.value = null;
      tabCounts.value = { new: 0, saved: 0, archived: 0 };
      activeClientFilters.value = {};
    }
  }
);
watch(selectedRowCount, async (newCount, oldCount) => {
  if (newCount > 0 && oldCount === 0) {
    await nextTick();
    if (batchActionsDropdownToggleRef.value) {
      const existingDropdown = Dropdown.getInstance(
        batchActionsDropdownToggleRef.value
      );
      if (!existingDropdown) new Dropdown(batchActionsDropdownToggleRef.value);
    }
  }
});
const isAdvancedCriteriaActive = computed(
  () =>
    (showAdvancedFilters.value &&
      typeof naturalLanguageQuery.value === "string" &&
      naturalLanguageQuery.value.trim() === "") ||
    filterTags.value.length > 0
);
function handleTabChangeFromPanel(newTab: LeadTab) {
  changeTab(newTab);
}
function handleClientFiltersUpdate(updatedFilters: ActiveClientFilters) {
  activeClientFilters.value = updatedFilters;
  pagination.value.pageIndex = 0;
  rowSelection.value = {};
  fetchLeadsForCurrentUser(true);
}
async function fetchTabCounts(userId: string | undefined) {
  if (!userId) {
    tabCounts.value = { new: 0, saved: 0, archived: 0 };
    return;
  }
  try {
    // Tab counts should still query the base table for accurate counts
    const [newRes, savedRes, archivedRes] = await Promise.all([
      supabase
        .from("leads") // Keep leads here
        .select("id", { count: "exact", head: true })
        .match({ user_id: userId, tab: "new" }),
      supabase
        .from("leads") // Keep leads here
        .select("id", { count: "exact", head: true })
        .match({ user_id: userId, tab: "saved" }),
      supabase
        .from("leads") // Keep leads here
        .select("id", { count: "exact", head: true })
        .match({ user_id: userId, tab: "archived" }),
    ]);
    tabCounts.value = {
      new: newRes.count ?? 0,
      saved: savedRes.count ?? 0,
      archived: archivedRes.count ?? 0,
    };
  } catch (error) {
    tabCounts.value = { new: 0, saved: 0, archived: 0 };
  }
}
function changeTab(newTab: LeadTab) {
  if (
    isLoadingLeads.value ||
    newTab === currentTab.value ||
    isProcessingBatch.value ||
    isSelectingAllLeads.value
  )
    return;
  currentTab.value = newTab;
  pagination.value.pageIndex = 0;
  sorting.value = [];
  rowSelection.value = {};
  activeClientFilters.value = {};
  fetchLeadsForCurrentUser(true);
}
async function archiveUnsavedLeads(
  userId: string | undefined
): Promise<boolean> {
  if (!userId) return false;
  try {
    const { error } = await supabase
      .from("leads")
      .update({ tab: "archived" })
      .match({ user_id: userId, tab: "new" });
    if (error) throw error;
    return true;
  } catch (e) {
    return false;
  }
}
async function hasUnsavedLeads(userId: string | undefined): Promise<boolean> {
  if (!userId) return false;
  try {
    const { count, error } = await supabase
      .from("leads")
      .select("id", { count: "exact", head: true })
      .match({ user_id: userId, tab: "new" });
    if (error) throw error;
    return (count ?? 0) > 0;
  } catch (e) {
    return false;
  }
}
function toggleAdvancedFilters() {
  showAdvancedFilters.value = !showAdvancedFilters.value;
}
function getFieldLabel(type: FilterTag["type"]): string {
  const map = {
    jobTitle: "jobTitleLabel",
    industry: "industryLabel",
    location: "locationLabel",
    companySize: "companySizeLabel",
    companyNames: "companyNamesLabel",
    generalKeywords: "generalKeywordsLabel",
  };
  /* @ts-ignore */ return (texts.value as any)[map[type]] || type;
}
function addAdvancedInputsAsTags() {
  const i = advancedFilterInputs;
  if (typeof i.jobTitle === "string" && i.jobTitle.trim())
    addTag("jobTitle", i.jobTitle.trim());
  if (typeof i.industry === "string" && i.industry)
    addTag(
      "industry",
      i.industry,
      languageStore.industries?.find((o) => o.value === i.industry)?.text
    );
  if (typeof i.location === "string" && i.location.trim())
    addTag("location", i.location.trim());
  if (typeof i.companySize === "string" && i.companySize)
    addTag("companySize", i.companySize);
  if (typeof i.companyNames === "string" && i.companyNames.trim())
    i.companyNames
      .trim()
      .split(",")
      .forEach((k) => {
        if (typeof k === "string" && k.trim()) addTag("companyNames", k.trim());
      });
  if (typeof i.generalKeywords === "string" && i.generalKeywords.trim())
    i.generalKeywords
      .trim()
      .split(",")
      .forEach((k) => {
        if (typeof k === "string" && k.trim())
          addTag("generalKeywords", k.trim());
      });
  Object.keys(i).forEach((k) => (i[k as keyof typeof i] = ""));
}
function addTag(
  type: FilterTag["type"],
  value: string,
  displayValueOverride?: string
) {
  const dVal = displayValueOverride || value;
  const lbl = getFieldLabel(type);
  if (type !== "companyNames" && type !== "generalKeywords")
    filterTags.value = filterTags.value.filter((t) => t.type !== type);
  if (
    filterTags.value.some(
      (t) => t.type === type && t.value.toLowerCase() === value.toLowerCase()
    )
  )
    return;
  filterTags.value.push({
    id: uuidv4(),
    type,
    value,
    displayValue: dVal,
    label: lbl,
  });
}
function removeFilterTag(tagId: string) {
  filterTags.value = filterTags.value.filter((t) => t.id !== tagId);
}
function validateSearchCriteria(): boolean {
  searchMessage.value = null;
  searchStatus.value = null;
  const nqHasContent =
    typeof naturalLanguageQuery.value === "string" &&
    naturalLanguageQuery.value.trim() !== "";
  const hasAppliedFilterTags = filterTags.value.length > 0;
  if (!nqHasContent && !hasAppliedFilterTags) {
    searchMessage.value = texts.value.noSearchCriteria;
    searchStatus.value = "error";
    return false;
  }
  const hasRequiredInputsFilled =
    filterTags.value.some((tag) => tag.type === "jobTitle") &&
    filterTags.value.some((tag) => tag.type === "industry");
  if (
    showAdvancedFilters.value &&
    !nqHasContent &&
    !hasAppliedFilterTags &&
    !hasRequiredInputsFilled
  ) {
    if (!filterTags.value.some((tag) => tag.type === "jobTitle")) {
      searchMessage.value = texts.value.errorRequired(
        getFieldLabel("jobTitle")
      );
      searchStatus.value = "error";
      return false;
    }
    if (!filterTags.value.some((tag) => tag.type === "industry")) {
      searchMessage.value = texts.value.errorRequired(
        getFieldLabel("industry")
      );
      searchStatus.value = "error";
      return false;
    }
  }
  return true;
}
async function submitLeadSearchCriteria() {
  if (isSearchingLeads.value) return;

  const hasNewLeads = tabCounts.value.new > 0;
  if (hasNewLeads) {
    if (confirm(texts.value.confirmArchiveUnsaved)) {
      await archiveAllNewLeads();
      searchMessage.value = texts.value.unsavedLeadsArchived;
      searchStatus.value = "info";
    } else {
      return;
    }
  }

  const criteriaPayload = {
    mainQuery: naturalLanguageQuery.value,
    filters: {
      jobTitle: filterTags.value.find(t => t.type === 'jobTitle')?.value || '',
      industry: filterTags.value.find(t => t.type === 'industry')?.value || '',
      location: filterTags.value.find(t => t.type === 'location')?.value || '',
      companySize: filterTags.value.find(t => t.type === 'companySize')?.value || '',
      companyNames: filterTags.value.filter(t => t.type === 'companyNames').map(t => t.value),
      keywords: filterTags.value.filter(t => t.type === 'generalKeywords').map(t => t.value),
    }
  };

  if (!criteriaPayload.mainQuery && Object.values(criteriaPayload.filters).every(v => !v || (Array.isArray(v) && v.length === 0))) {
    searchMessage.value = texts.value.noSearchCriteria;
    searchStatus.value = "warning";
    return;
  }

  await handleLeadSearch(criteriaPayload);
}
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:7860/api/v1";

async function archiveAllNewLeads() {
  try {
    // Step 1: Get a fresh, guaranteed valid session from Supabase.
    const { data: { session }, error: sessionError } = await supabase.auth.getSession();

    if (sessionError) {
      throw new Error(`Failed to retrieve auth session: ${sessionError.message}`);
    }
    if (!session) {
      throw new Error("User is not authenticated.");
    }
    
    // Step 2: Manually set the Authorization header for the function call.
    const { error } = await supabase.functions.invoke('archive-new-leads-on-logout', {
      headers: {
        'Authorization': `Bearer ${session.access_token}`
      }
    });
    
    if (error) throw error;
    
  } catch (error: any) {
    console.error("Error archiving new leads:", error);
    searchMessage.value = texts.value.autoArchiveError + ` ${error.message}`;
    searchStatus.value = "error";
  }
}

async function handleLeadSearch(criteriaPayload: any) {
  isSearchingLeads.value = true;
  searchMessage.value = null;
  searchStatus.value = null;

  try {
    // Force refresh the session to get the latest JWT token
    const { data: { session }, error: sessionError } = await supabase.auth.getSession();

    if (sessionError) {
      throw new Error(`Failed to retrieve auth session: ${sessionError.message}`);
    }
    
    if (!session?.access_token) {
      searchMessage.value = texts.value.userNotAuthMessage;
      searchStatus.value = "error";
      // Optionally, redirect to login
      // authStore.signOut(); 
      return;
    }

    const res = await fetch(`${API_BASE_URL}/leads/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.access_token}`,
      },
      body: JSON.stringify(criteriaPayload),
    });

    if (!res.ok) {
      // Try to parse the error response, but handle cases where it's not valid JSON
      let errorDetail = `API Error: ${res.status} ${res.statusText}`;
      try {
        const result = await res.json();
        errorDetail = result.detail || result.message || errorDetail;
      } catch (e) {
        // Ignore JSON parsing errors if the response is not JSON
      }
      throw new Error(errorDetail);
    }

    searchMessage.value = texts.value.searchLeadsSuccess;
    searchStatus.value = "success";
    await fetchLeadsForCurrentUser(true);
    await fetchTabCounts(authStore.user?.id);
  } catch (error: any) {
    searchMessage.value = texts.value.alertError + error.message;
    searchStatus.value = "error";
  } finally {
    isSearchingLeads.value = false;
  }
}
async function getSupabaseSession(): Promise<Session | null> {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession();
  if (error || !session) {
    if (authStore.isAuthenticated) await authStore.signOut();
    searchMessage.value = error
      ? texts.value.alertError + error.message
      : texts.value.userNotAuthMessage;
    searchStatus.value = "error";
    return null;
  }
  return session;
}

// Updated selectFields to include the new _text columns from the view
const selectFields = `id, created_at, user_id, tab, lead_status, icebreaker, source_query_criteria, first_name, last_name, name, job_title, industry, industry_text, location, company_name, company_size, phone, linkedIn_url, keywords, keywords_text, email, notes`;

async function fetchLeadsForCurrentUser(forceRefresh = false) {
  if (
    (isLoadingLeads.value && !forceRefresh) ||
    (isProcessingBatch.value && !forceRefresh) ||
    (isSelectingAllLeads.value && !forceRefresh)
  ) {
    return;
  }
  isLoadingLeads.value = true;
  const user = authStore.user;
  if (!user) {
    tableData.value = [];
    rowSelection.value = {};
    isLoadingLeads.value = false;
    initialLoadComplete.value = true;
    totalRowCount.value = 0;
    tabCounts.value = { new: 0, saved: 0, archived: 0 };
    return;
  }

  try {
    // IMPORTANT: Query the new view instead of the original table
    let query = supabase
      .from("leads_search_view") // Changed from "leads" to your new view name
      .select(selectFields, { count: "exact" })
      .eq("user_id", user.id)
      .eq("tab", currentTab.value);

    // Apply active client filters
    Object.entries(activeClientFilters.value).forEach(([filterKey, values]) => {
      if (Array.isArray(values) && values.length > 0) {
        const typedFilterKey = filterKey as FilterKey;
        // Use the mapped column name for the Supabase query
        const actualColumnName = COLUMN_MAPPING[typedFilterKey];
        
        if (!actualColumnName) {
            console.warn(`fetchLeadsForCurrentUser: No column mapping found for filter key: ${typedFilterKey}. This filter will be ignored.`);
            return; // Skip this filter if no mapping found
        }

        switch (typedFilterKey) { // Switch on the original filter key type
          case "lead_status":
            query = query.in(actualColumnName, values);
            break;
          case "company_size":
            // This logic is already correct for numeric range filtering
            const companySizeOrFilters: string[] = [];
            values.forEach((rangeStr) => {
              const { min, max } = parseCompanySizeRange(rangeStr);
              if (min !== undefined && max !== undefined) {
                companySizeOrFilters.push(
                  `and(${actualColumnName}.gte.${min},${actualColumnName}.lte.${max})`
                );
              } else if (min !== undefined) {
                companySizeOrFilters.push(`${actualColumnName}.gte.${min}`);
              }
            });
            if (companySizeOrFilters.length > 0) {
              query = query.or(companySizeOrFilters.join(","));
            }
            break;
          // Group all fuzzy text search fields here, using the actualColumnName (which might be _text)
          case "job_title":
          case "location":
          case "company_name":
          case "industry":
          case "keywords":
            // For these fields, now use ilike on the new text columns from the view (or original text columns)
            const orFuzzyConditions = values
              .map((val) => `${actualColumnName}.ilike.%${String(val).trim()}%`)
              .join(",");
            if (orFuzzyConditions) query = query.or(orFuzzyConditions);
            break;
          default:
            // This default should ideally never be hit if all FilterKey types are covered
            console.warn(
              `fetchLeadsForCurrentUser: Unhandled filter key type in switch: ${typedFilterKey}. Please add it to COLUMN_MAPPING and switch cases.`
            );
            break;
        }
      }
    });

    if (sorting.value.length > 0) {
      const sortColumn = sorting.value[0];
      const dbSortColumn = sortColumn.id;
      // Allow sorting on the original columns, as they exist in the view
      // Note: Sorting on the _text columns might be unexpected for arrays/JSONB if not carefully considered.
      // Keeping original column names for sorting for consistency with initial data display.
      const allowedSort = [
        "name",
        "job_title",
        "company_name",
        "email",
        "created_at",
        "lead_status",
        "company_size",
        "industry", // Sorting on array columns can be complex, default behavior might be lexical
        "keywords", // Sorting on JSONB columns also complex, default behavior might be lexical
      ];
      if (allowedSort.includes(dbSortColumn)) {
        query = query.order(dbSortColumn, { ascending: !sortColumn.desc });
      } else {
        // Fallback for sorting on columns not in allowedSort
        query = query.order("created_at", { ascending: false });
      }
    } else {
      query = query.order("created_at", { ascending: false });
    }

    const page = pagination.value.pageIndex;
    const pageSize = pagination.value.pageSize;
    query = query.range(page * pageSize, (page + 1) * pageSize - 1);

    const { data: fetchedData, error, status, count } = await query;

    if (error && status !== 406) {
      console.error(
        "Supabase fetch error:",
        error,
        "Query filters:",
        JSON.stringify(activeClientFilters.value)
      );
      if (error.message.includes("JWT")) {
        searchMessage.value = texts.value.accessDeniedMessage;
        searchStatus.value = "error";
        await authStore.signOut();
      }
      tableData.value = [];
      totalRowCount.value = 0;
    } else if (error) {
      console.warn(
        "Supabase fetch warning/non-blocking error:",
        error,
        "Query filters:",
        JSON.stringify(activeClientFilters.value)
      );
      tableData.value = fetchedData || [];
      totalRowCount.value = count || (fetchedData ? (fetchedData as Lead[]).length : 0);
      // You can keep the error message here if you want to notify user about filter issues
      // if (error.code === "PGRST100" || error.code === "42883") {
      //   searchMessage.value = `Filter error: ${error.message}. Some filters may not be applied correctly.`;
      //   searchStatus.value = "warning";
      // }
    } else {
      tableData.value = fetchedData || [];
      const totalCount = count || 0;
      totalRowCount.value = totalCount;
      const newPageCount = Math.ceil(totalCount / pageSize);
      const currentPageIndex = pagination.value.pageIndex;
      if (newPageCount > 0 && currentPageIndex >= newPageCount) {
        pagination.value.pageIndex = newPageCount - 1;
      } else if (
        currentPageIndex > 0 &&
        totalCount === 0 &&
        currentTab.value !== "new"
      ) {
        pagination.value.pageIndex = 0;
      }
    }
  } catch (e: any) {
    if (!searchMessage.value) {
      searchMessage.value =
        texts.value.alertError + (e.message || "Unknown error");
    }
    searchStatus.value = "error";
    tableData.value = [];
    totalRowCount.value = 0;
  } finally {
    isLoadingLeads.value = false;
    if (!initialLoadComplete.value) initialLoadComplete.value = true;
  }
}

onMounted(async () => {
  const session = authStore.session || (await getSupabaseSession());
  if (session && authStore.user) {
    await fetchTabCounts(authStore.user.id);
    await fetchLeadsForCurrentUser(true);
  } else {
    isLoadingLeads.value = false;
    initialLoadComplete.value = true;
    tabCounts.value = { new: 0, saved: 0, archived: 0 };
    totalRowCount.value = 0;
  }
});
</script>