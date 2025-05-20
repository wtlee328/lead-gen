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
                  <div class="col-12">
                    <label
                      for="advKeywords"
                      class="form-label search-panel-adv-label"
                      >{{ texts.keywordsLabel }}</label
                    ><input
                      type="text"
                      class="form-control form-control-sm search-panel-adv-input"
                      id="advKeywords"
                      v-model="advancedFilterInputs.otherKeywords"
                      :placeholder="texts.advKeywordsPlaceholder"
                    />
                  </div>
                  <div class="col-12 text-end">
                    <button
                      type="button"
                      class="btn btn-primary btn-sm search-panel-btn-primary"
                      @click="addAdvancedInputsAsTags"
                    >
                      <i class="bi bi-plus-lg me-1"></i>
                      <span>{{ texts.addFiltersBtn-text }}</span>
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
                  @click="selectAllOnPage"
                  :disabled="
                    table.getRowModel().rows.length === 0 ||
                    table.getIsAllPageRowsSelected() ||
                    isProcessingBatch
                  "
                  :title="texts.selectAllPageTooltip"
                >
                  <i class="bi bi-check2-square me-1"></i>
                  {{ texts.selectAllPageButton }}
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary me-2"
                  @click="deselectAllOnPage"
                  :disabled="selectedRowCount === 0 || isProcessingBatch"
                  :title="texts.deselectAllPageTooltip"
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
                    :disabled="isProcessingBatch"
                  >
                    <span
                      v-if="isProcessingBatch"
                      class="spinner-border spinner-border-sm me-1"
                      role="status"
                      aria-hidden="true"
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
                            disabled: !canBatchSave || isProcessingBatch,
                          }"
                          @click.prevent="
                            !(!canBatchSave || isProcessingBatch) &&
                              batchSaveSelected()
                          "
                          >{{ texts.batchSaveButton }}</a
                        >
                      </li>
                      <li>
                        <a
                          class="dropdown-item"
                          href="#"
                          :class="{
                            disabled: !canBatchArchiveNew || isProcessingBatch,
                          }"
                          @click.prevent="
                            !(!canBatchArchiveNew || isProcessingBatch) &&
                              batchArchiveSelected()
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
                              isProcessingBatch,
                          }"
                          @click.prevent="
                            !(
                              !canBatchRestoreToNewFromSaved ||
                              isProcessingBatch
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
                              !canBatchArchiveSaved || isProcessingBatch,
                          }"
                          @click.prevent="
                            !(!canBatchArchiveSaved || isProcessingBatch) &&
                              batchArchiveSelected()
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
                            disabled: !canBatchMoveToSaved || isProcessingBatch,
                          }"
                          @click.prevent="
                            !(!canBatchMoveToSaved || isProcessingBatch) &&
                              batchMoveToSavedSelected()
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
                              !canBatchDeleteArchived || isProcessingBatch,
                          }"
                          @click.prevent="
                            !(!canBatchDeleteArchived || isProcessingBatch) &&
                              batchDeleteSelected()
                          "
                          >{{ texts.batchDeleteButton }}</a
                        >
                      </li>
                    </template>
                     <!-- Divider if any tab-specific actions were present -->
                    <li v-if="(currentTab === 'new' && (canBatchSave || canBatchArchiveNew)) || (currentTab === 'saved' && (canBatchRestoreToNewFromSaved || canBatchArchiveSaved)) || (currentTab === 'archived' && (canBatchMoveToSaved || canBatchDeleteArchived))">
                      <hr class="dropdown-divider" />
                    </li>

                    <!-- Export CSV Action -->
                    <li>
                      <a
                        class="dropdown-item"
                        href="#"
                        :class="{ disabled: isProcessingBatch || selectedRowCount === 0 }"
                        @click.prevent="!(isProcessingBatch || selectedRowCount === 0) && exportSelectedToCSV()"
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
                  :disabled="isLoadingLeads || isProcessingBatch"
                  :title="texts.refreshButton"
                >
                  <i
                    :class="[
                      'bi',
                      isLoadingLeads || isProcessingBatch
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
                          header.column.getCanSort() && !isProcessingBatch
                            ? header.column.getToggleSortingHandler()?.($event)
                            : undefined
                        "
                        :class="{
                          'cursor-pointer':
                            header.column.getCanSort() && !isProcessingBatch,
                          'sorting-asc': header.column.getIsSorted() === 'asc',
                          'sorting-desc':
                            header.column.getIsSorted() === 'desc',
                        }"
                        :style="getColumnStyle(header.column)" <!-- Pass header.column directly -->
                      >
                        <div class="d-flex align-items-center">
                          <FlexRender
                            v-if="
                              header && header.column && header.column.columnDef
                            "
                            :render="header.column.columnDef.header"
                            :props="header.getContext()"
                          />
                          <div class="ms-1 sort-indicator">
                            <i
                              v-if="header.column.getIsSorted() === 'asc'"
                              class="bi bi-sort-up"
                            ></i>
                            <i
                              v-if="header.column.getIsSorted() === 'desc'"
                              class="bi bi-sort-down"
                            ></i>
                            <i
                              v-if="
                                !header.column.getIsSorted() &&
                                header.column.getCanSort()
                              "
                              class="bi bi-filter"
                            ></i>
                          </div>
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
                        'processing-row-disabled': isProcessingBatch,
                      }"
                    >
                      <td
                        v-for="cell in row.getVisibleCells()"
                        :key="cell.id"
                        :style="getColumnStyle(cell.column)" <!-- Pass cell.column directly -->
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
                  @click="!isProcessingBatch && table.setPageIndex(0)"
                  :disabled="!table.getCanPreviousPage() || isProcessingBatch"
                >
                  <i class="bi bi-chevron-bar-left"></i>
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="!isProcessingBatch && table.previousPage()"
                  :disabled="!table.getCanPreviousPage() || isProcessingBatch"
                >
                  <i class="bi bi-chevron-left me-1"></i
                  >{{ texts.previousPage }}
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="!isProcessingBatch && table.nextPage()"
                  :disabled="!table.getCanNextPage() || isProcessingBatch"
                >
                  {{ texts.nextPage }}<i class="bi bi-chevron-right ms-1"></i>
                </button>
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="
                    !isProcessingBatch &&
                      table.setPageIndex(table.getPageCount() - 1)
                  "
                  :disabled="!table.getCanNextPage() || isProcessingBatch"
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
                  @change="e => !isProcessingBatch && table.setPageSize(Number((e.target as HTMLSelectElement).value))"
                  :disabled="isProcessingBatch"
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
} from "@/components/FilterPanelView.vue";
import { useLanguageStore } from "@/stores/languageStore";
import { useAuthStore } from "@/stores/authStore";
import { supabase } from "@/services/supabaseClient";
import type { Session } from "@supabase/supabase-js";
import { v4 as uuidv4 } from "uuid";
import {
  useVueTable,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  createColumnHelper,
  FlexRender,
  type ColumnDef,
  type SortingState,
  type PaginationState,
  type RowSelectionState,
  type Column, // Explicitly import Column
  type Row,
  type CellContext,
  type HeaderContext,
  type Updater,
} from "@tanstack/vue-table";
import type { LeadTab } from "@/types/tabs";
import { Dropdown } from "bootstrap";
import type { Translations } from "@/types/language";

// IMPORTANT: This module augmentation block MUST be in a global .d.ts file
// (e.g., src/types/tanstack-table.d.ts or env.d.ts) and included in your tsconfig.json.
// Placing it here will cause TypeScript errors during compilation.
// REMOVE this entire commented-out block from your actual .vue file if it's there.
/*
declare module "@tanstack/vue-table" {
  interface ColumnMeta<TData, TValue> {
    style?: Record<string, string>;
  }
}
*/

interface Lead {
  id: string;
  created_at: string;
  user_id: string;
  tab: LeadTab | null;
  first_name?: string | null;
  last_name?: string | null;
  name?: string | null;
  job_title?: string | null;
  industry?: string[] | null; // Confirmed as JSONB array
  location?: string | null;
  company_name?: string | null;
  company_size?: string[] | null; // Confirmed as JSONB array
  phone?: string | null;
  linkedIn_url?: string | null;
  keywords?: string[] | Record<string, any> | string | null; // Flexible for JSONB keywords
  email?: string | null;
  notes?: string | null;
  lead_status?: string | null;
  icebreaker?: string | null;
  source_query_criteria?: Record<string, any> | null;
}
interface FilterTag {
  id: string;
  type: "jobTitle" | "industry" | "location" | "companySize" | "otherKeywords";
  value: string; // Keep as string for inputs, will convert to string[] for DB query
  displayValue: string;
  label: string;
}

const languageStore = useLanguageStore();
const authStore = useAuthStore();

// New: State to manage expanded keywords per row
const expandedKeywords = ref<Record<string, boolean>>({});
const MAX_VISIBLE_KEYWORDS = 3; // Number of keywords to show initially

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
  industry: "", // String for select binding
  location: "",
  companySize: "", // String for select binding
  otherKeywords: "",
});
const filterTags = ref<FilterTag[]>([]);
const isSearchingLeads = ref(false);
const searchMessage = ref<string | null>(null);
const searchStatus = ref<"success" | "error" | "warning" | null>(null);
const N8N_WEBHOOK_URL = import.meta.env
  .VITE_N8N_LEAD_INGESTION_WEBHOOK_URL as string;
const tableData = ref<Lead[]>([]);
const isLoadingLeads = ref(false);
const initialLoadComplete = ref(false);
const sorting = ref<SortingState>([]);
const pagination = ref<PaginationState>({ pageIndex: 0, pageSize: 15 });
const rowSelection = ref<RowSelectionState>({});
const isProcessingBatch = ref(false);
const batchActionsDropdownToggleRef = ref<HTMLButtonElement | null>(null);
const columnHelper = createColumnHelper<Lead>();

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
  keywordsLabel: "Other Keywords",
  advKeywordsPlaceholder: "e.g., innovative, AI, B2B",
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
  deselectAllButton: "Deselect All",
  batchActionsDropdownTitle: "Actions for Selected",
  selectAllPageTooltip: "Select all leads on current page",
  deselectAllPageTooltip: "Deselect all leads on current page",
  batchSaveButton: "Save Selected",
  batchArchiveButton: "Archive Selected",
  batchRestoreButton: "Restore Selected to New",
  batchDeleteButton: "Delete Selected",
  batchMoveToSavedButton: "Move Selected to Saved",
  confirmBatchSave: (count: number) =>
    `Are you sure you want to save ${count} selected lead(s)?`,
  confirmBatchArchive: (count: number) =>
    `Are you sure you want to archive ${count} selected lead(s)?`,
  confirmBatchRestore: (count: number) =>
    `Are you sure you want to restore ${count} selected lead(s) to 'New'?`,
  confirmBatchDelete: (count: number) =>
    `Are you sure you want to permanently delete ${count} selected lead(s)? This action cannot be undone.`,
  confirmBatchMoveToSaved: (count: number) =>
    `Are you sure you want to move ${count} selected lead(s) to 'Saved'?`,
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
  // New localization keys for keywords expansion
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
          isProcessingBatch.value || table.getRowModel().rows.length === 0,
        onChange: table.getToggleAllPageRowsSelectedHandler(),
        title: texts.value.selectAllPageTooltip,
      }),
    cell: ({ row }: CellContext<Lead, unknown>) =>
      h("input", {
        type: "checkbox",
        class: "form-check-input",
        style: "cursor: pointer;",
        checked: row.getIsSelected(),
        disabled: !row.getCanSelect() || isProcessingBatch.value,
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
              disabled: isProcessingBatch.value,
              onClick: () =>
                !isProcessingBatch.value && updateLeadTab(lead.id, "saved"),
            },
            [h("i", { class: "bi bi-bookmark-check" })]
          )
        );
        buttons.push(
          h(
            "button",
            {
              onClick: () =>
                !isProcessingBatch.value && updateLeadTab(lead.id, "archived"),
              class: `btn btn-sm btn-outline-warning ${
                buttons.length > 0 ? "ms-1" : ""
              }`,
              disabled: isProcessingBatch.value,
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
                !isProcessingBatch.value && updateLeadTab(lead.id, "new"),
              class: "btn btn-sm btn-outline-secondary",
              disabled: isProcessingBatch.value,
              title: texts.value.tooltipRestore,
            },
            [h("i", { class: "bi bi-arrow-counterclockwise" })]
          )
        );
        buttons.push(
          h(
            "button",
            {
              onClick: () =>
                !isProcessingBatch.value && updateLeadTab(lead.id, "archived"),
              class: `btn btn-sm btn-outline-warning ${
                buttons.length > 0 ? "ms-1" : ""
              }`,
              disabled: isProcessingBatch.value,
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
                !isProcessingBatch.value && updateLeadTab(lead.id, "saved"),
              class: "btn btn-sm btn-outline-secondary",
              disabled: isProcessingBatch.value,
              title: texts.value.tooltipMoveToSaved,
            },
            [h("i", { class: "bi bi-bookmark-plus" })]
          )
        );
        buttons.push(
          h(
            "button",
            {
              onClick: () => !isProcessingBatch.value && deleteLead(lead.id),
              class: `btn btn-sm btn-outline-danger ${
                buttons.length > 0 ? "ms-1" : ""
              }`,
              disabled: isProcessingBatch.value,
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
        left: "60px",
        width: "150px",
        minWidth: "150px",
        textAlign: "center",
        verticalAlign: "middle",
        zIndex: "17",
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
    size: 180,
    meta: {
      style: {
        position: "sticky",
        left: "210px",
        minWidth: "180px",
        width: "180px",
        zIndex: "16",
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
      // Handle both string[] and single string for robustness
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
      // Fallback for unexpected single string values
      if (typeof industries === "string" && industries.trim() !== "") {
        return h(
          "span",
          { class: "badge bg-info text-dark me-1 mb-1" },
          industries
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
    cell: (info: CellContext<Lead, Lead["company_size"]>) => {
      const sizes = info.getValue();
      // Handle both string[] and single string for robustness
      if (Array.isArray(sizes) && sizes.length > 0) {
        return h(
          "div",
          { style: "max-width: 150px; white-space: normal;" },
          sizes.map((size) =>
            h("span", { class: "badge bg-secondary me-1 mb-1" }, String(size))
          )
        );
      }
      // Fallback for unexpected single string values
      if (typeof sizes === "string" && sizes.trim() !== "") {
        return h("span", { class: "badge bg-secondary me-1 mb-1" }, sizes);
      }
      return "N/A";
    },
    enableSorting: true,
    size: 110,
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

      // Robustly convert keywords to an array of strings
      if (Array.isArray(leadRawKeywords)) {
        actualKeywordsArray = leadRawKeywords
          .map((kw) => String(kw).trim()) // Ensure trim is called on string
          .filter(Boolean);
      } else if (
        typeof leadRawKeywords === "string" &&
        leadRawKeywords.trim() !== ""
      ) {
        actualKeywordsArray = leadRawKeywords
          .split(",")
          .map((kw) => kw.trim()) // Ensure trim is called on string
          .filter(Boolean);
      } else if (
        leadRawKeywords &&
        typeof leadRawKeywords === "object" &&
        !Array.isArray(leadRawKeywords)
      ) {
        // If it's an object, try to extract values (e.g., from a JSON object {k1: 'v1', k2: 'v2'})
        actualKeywordsArray = Object.values(leadRawKeywords)
          .map((kw) => String(kw).trim()) // Ensure trim is called on string
          .filter(Boolean);
      }

      if (actualKeywordsArray.length === 0) {
        return "N/A";
      }

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
                event.stopPropagation(); // Prevent row selection if clicking button
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

      // Filter(Boolean) removes the null toggleButton if it's not needed, preventing an empty node
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
  columnHelper.accessor("lead_status", {
    id: "lead_status",
    header: () => texts.value.colStatus,
    cell: (info: CellContext<Lead, Lead["lead_status"]>) => {
      const status = info.getValue();
      return status
        ? h("span", { class: `badge ${getStatusBadgeClass(status)}` }, status)
        : "N/A";
    },
    enableSorting: true,
    size: 130,
    meta: {
      style: {
        position: "sticky",
        right: "0px",
        minWidth: "130px",
        width: "130px",
        zIndex: "16",
        backgroundColor: "var(--card-bg-current)",
        borderLeft: "1px solid var(--border-color-current)",
      },
    },
  }),
]);

// Updated: Refined parameter type for getColumnStyle
function getColumnStyle(column: Column<Lead, unknown>) {
  const baseStyle: Record<string, string> = {
    "user-select": column.getCanSort() && !isProcessingBatch.value ? "pointer" : "none",
    verticalAlign: "middle",
  };
  if (!column.columnDef.meta?.style?.width) {
    baseStyle.width = `${column.columnDef.size}px`;
  }
  if (!column.columnDef.meta?.style?.minWidth) {
    baseStyle.minWidth = `${column.columnDef.size}px`;
  }
  const metaStyle = column.columnDef.meta?.style || {};
  return { ...baseStyle, ...metaStyle };
}


const table = useVueTable({
  get data() {
    return tableData.value;
  },
  columns: columns.value,
  state: {
    get sorting() {
      return sorting.value;
    },
    get pagination() {
      return pagination.value;
    },
    get rowSelection() {
      return rowSelection.value;
    },
  },
  enableRowSelection: true,
  onRowSelectionChange: (updater: Updater<RowSelectionState>) => {
    if (isProcessingBatch.value) return;
    rowSelection.value =
      typeof updater === "function" ? updater(rowSelection.value) : updater;
  },
  onSortingChange: (updater: Updater<SortingState>) => {
    if (isProcessingBatch.value) return;
    const oldSortingString = JSON.stringify(sorting.value);
    const newSortingState =
      typeof updater === "function" ? updater(sorting.value) : updater;
    if (JSON.stringify(newSortingState) !== oldSortingString) {
      sorting.value = newSortingState;
      console.log(
        `%cLeadGenFormView: SORTING CHANGED (Values Differ). From: ${oldSortingString} -> To: ${JSON.stringify(
          sorting.value
        )}`,
        "color: orange; font-weight: bold;"
      );
      console.count("LeadGenFormView: onSortingChange (fetch triggered)");
      fetchLeadsForCurrentUser(true);
    } else {
      sorting.value = newSortingState;
      console.log(
        `%cLeadGenFormView: SORTING state updated by table (ref changed, values same). Current: ${JSON.stringify(
          sorting.value
        )}. NO FETCH.`,
        "color: orange;"
      );
      console.count("LeadGenFormView: onSortingChange (ref updated, no fetch)");
    }
  },
  onPaginationChange: (updater: Updater<PaginationState>) => {
    if (isProcessingBatch.value) return;
    const oldPageIndex = pagination.value.pageIndex;
    const oldPageSize = pagination.value.pageSize;
    const newPaginationState =
      typeof updater === "function" ? updater(pagination.value) : updater;
    if (
      newPaginationState.pageIndex !== oldPageIndex ||
      newPaginationState.pageSize !== oldPageSize
    ) {
      pagination.value = newPaginationState;
      console.log(
        `%cLeadGenFormView: PAGINATION CHANGED (Values Differ). From Index: ${oldPageIndex}, Size: ${oldPageSize} -> To Index: ${pagination.value.pageIndex}, Size: ${pagination.value.pageSize}`,
        "color: orange; font-weight: bold;"
      );
      console.count("LeadGenFormView: onPaginationChange (fetch triggered)");
      fetchLeadsForCurrentUser(true);
    } else {
      pagination.value = newPaginationState;
      console.log(
        `%cLeadGenFormView: PAGINATION state updated by table (ref changed, values same). Index: ${pagination.value.pageIndex}, Size: ${pagination.value.pageSize}. NO FETCH.`,
        "color: orange;"
      );
      console.count(
        "LeadGenFormView: onPaginationChange (ref updated, no fetch)"
      );
    }
  },
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  manualPagination: true,
  manualSorting: true,
});

const selectAllOnPage = () => {
  if (isProcessingBatch.value) return;
  table.toggleAllPageRowsSelected(true);
};
const deselectAllOnPage = () => {
  if (isProcessingBatch.value) return;
  table.toggleAllPageRowsSelected(false);
};
const selectedRowCount = computed(
  () => table.getSelectedRowModel().rows.length
);

const canBatchSave = computed(
  () =>
    currentTab.value === "new" &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table
      .getSelectedRowModel()
      .rows.some((row: Row<Lead>) => row.original.tab === "new")
);
const canBatchArchiveNew = computed(
  () =>
    currentTab.value === "new" &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table
      .getSelectedRowModel()
      .rows.some((row: Row<Lead>) => row.original.tab === "new")
);
const canBatchRestoreToNewFromSaved = computed(
  () =>
    currentTab.value === "saved" &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table
      .getSelectedRowModel()
      .rows.some((row: Row<Lead>) => row.original.tab === "saved")
);
const canBatchArchiveSaved = computed(
  () =>
    currentTab.value === "saved" &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table
      .getSelectedRowModel()
      .rows.some((row: Row<Lead>) => row.original.tab === "saved")
);
const canBatchMoveToSaved = computed(
  () =>
    currentTab.value === "archived" &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table
      .getSelectedRowModel()
      .rows.some((row: Row<Lead>) => row.original.tab === "archived")
);
const canBatchDeleteArchived = computed(
  () =>
    currentTab.value === "archived" &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0
);

const batchProcessLeads = async (
  targetTabOrAction: LeadTab | "delete",
  actionNameKey: keyof Pick<
    Translations,
    | "confirmBatchSave"
    | "confirmBatchArchive"
    | "confirmBatchRestore"
    | "confirmBatchDelete"
    | "confirmBatchMoveToSaved"
  >,
  filterFn: (lead: Lead) => boolean,
  operationFn: (
    leadId: string,
    target?: LeadTab
  ) => Promise<{ success: boolean; error?: any }>
) => {
  if (isProcessingBatch.value) return;
  const selectedRows = table.getSelectedRowModel().rows;
  if (selectedRows.length === 0) return;

  const leadsToProcess: Lead[] = selectedRows
    .map((row: Row<Lead>) => row.original)
    .filter(filterFn);

  const actionNameForNoLeadsMsg = actionNameKey
    .replace("confirmBatch", "")
    .toLowerCase();
  if (leadsToProcess.length === 0 && targetTabOrAction !== "delete") {
    searchMessage.value = texts.value.noLeadsEligibleForAction(
      actionNameForNoLeadsMsg
    );
    searchStatus.value = "warning";
    return;
  }
  const confirmMessageFn = texts.value[actionNameKey] as (
    count: number
  ) => string;
  if (!confirm(confirmMessageFn(leadsToProcess.length))) return;

  isProcessingBatch.value = true;
  const processingActionName = actionNameKey.replace("confirmBatch", "");
  searchMessage.value = `Processing ${processingActionName} batch... (${leadsToProcess.length} leads)`;
  searchStatus.value = null;
  let successCount = 0;
  let errorCount = 0;

  const results: PromiseSettledResult<{ success: boolean; error?: any }>[] =
    await Promise.allSettled(
      leadsToProcess.map((lead: Lead) =>
        operationFn(
          lead.id,
          targetTabOrAction !== "delete" ? targetTabOrAction : undefined
        )
      )
    );

  results.forEach(
    (
      result: PromiseSettledResult<{ success: boolean; error?: any }>,
      index: number
    ) => {
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
    }
  );

  searchMessage.value = texts.value.batchActionResult(
    processingActionName,
    successCount,
    errorCount
  );
  searchStatus.value =
    errorCount > 0 ? (successCount > 0 ? "warning" : "error") : "success";
  rowSelection.value = {};
  await fetchLeadsForCurrentUser(true);
  await fetchTabCounts(authStore.user?.id);
  isProcessingBatch.value = false;
};

const batchSaveSelected = () =>
  batchProcessLeads(
    "saved",
    "confirmBatchSave",
    (lead) => lead.tab === "new",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchArchiveSelected = () =>
  batchProcessLeads(
    "archived",
    "confirmBatchArchive",
    (lead) =>
      currentTab.value === "new" ? lead.tab === "new" : lead.tab === "saved",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchRestoreSelected = () =>
  batchProcessLeads(
    "new",
    "confirmBatchRestore",
    (lead) => lead.tab === "saved",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchMoveToSavedSelected = () =>
  batchProcessLeads(
    "saved",
    "confirmBatchMoveToSaved",
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
  if (isProcessingBatch.value || selectedRowCount.value === 0) {
    return;
  }

  const selectedRows = table.getSelectedRowModel().rows;
  const leadsToExport: Lead[] = selectedRows.map((row) => row.original);

  if (leadsToExport.length === 0) {
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

  const csvRows: string[] = [];
  csvRows.push(headers.join(","));

  const formatCSVCell = (value: any): string => {
    if (value === null || typeof value === "undefined") {
      return "";
    }
    let stringValue = String(value);

    if (Array.isArray(value)) {
      stringValue = value.map((item) => String(item).replace(/"/g, '""')).join("; ");
    } else if (typeof value === "object" && value !== null) {
      try {
        stringValue = JSON.stringify(value);
      } catch (e) {
        stringValue = "[Object]";
      }
    }

    if (
      stringValue.includes('"') ||
      stringValue.includes(',') ||
      stringValue.includes('\n') ||
      stringValue.includes('\r')
    ) {
      return `"${stringValue.replace(/"/g, '""')}"`;
    }
    return stringValue;
  };

  leadsToExport.forEach((lead) => {
    const row = [
      formatCSVCell(lead.id),
      formatCSVCell(lead.created_at ? new Date(lead.created_at).toISOString() : ""),
      formatCSVCell(lead.tab),
      formatCSVCell(lead.lead_status),
      formatCSVCell(lead.first_name),
      formatCSVCell(lead.last_name),
      formatCSVCell(
        lead.name || `${lead.first_name || ""} ${lead.last_name || ""}`.trim()
      ),
      formatCSVCell(lead.job_title),
      formatCSVCell(lead.industry),
      formatCSVCell(lead.location),
      formatCSVCell(lead.company_name),
      formatCSVCell(lead.company_size),
      formatCSVCell(lead.phone),
      formatCSVCell(lead.linkedIn_url),
      formatCSVCell(lead.keywords),
      formatCSVCell(lead.email),
      formatCSVCell(lead.notes),
      formatCSVCell(lead.icebreaker),
      formatCSVCell(lead.source_query_criteria),
    ];
    csvRows.push(row.join(","));
  });

  const csvString = csvRows.join("\r\n");
  const blob = new Blob([`\uFEFF${csvString}`], { type: "text/csv;charset=utf-8;" });

  const link = document.createElement("a");
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    const timestamp = new Date().toISOString().slice(0, 19).replace(/[-:T]/g, "");
    link.setAttribute("href", url);
    link.setAttribute("download", `leads_export_${timestamp}.csv`);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  } else {
    alert(
      "CSV export initiated. Your browser may handle the download differently or require manual saving."
    );
    const encodedUri = encodeURI("data:text/csv;charset=utf-8," + `\uFEFF${csvString}`);
    const newWindow = window.open(encodedUri);
    if (!newWindow) {
      alert(
        "Could not open a new window for CSV download. Please check your popup blocker settings."
      );
    }
  }
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
      const currentSelection = { ...rowSelection.value };
      if (currentSelection[leadId]) {
        delete currentSelection[leadId];
        rowSelection.value = currentSelection;
      }
      await fetchLeadsForCurrentUser(true);
      await fetchTabCounts(authStore.user?.id);
    }
    return { success: true, leadId, newTab };
  } catch (error: any) {
    if (!isBatchOperation) {
      searchMessage.value = texts.value.leadUpdateError + ` (${error.message})`;
      searchStatus.value = "error";
    }
    console.error(`Error updating lead ${leadId} tab:`, error);
    return { success: false, leadId, newTab, error };
  } finally {
    if (!isProcessingBatch.value) isProcessingBatch.value = false;
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
    const { error } = await supabase.from("leads").delete().eq("id", leadId);

    if (error) throw error;

    if (!isBatchOperation) {
      searchMessage.value = texts.value.leadDeletedSuccess;
      searchStatus.value = "success";

      const currentSelection = { ...rowSelection.value };
      if (currentSelection[leadId]) {
        delete currentSelection[leadId];
        rowSelection.value = currentSelection;
      }
      await fetchLeadsForCurrentUser(true);
      await fetchTabCounts(authStore.user?.id);
    }
    return { success: true };
  } catch (error: any) {
    if (!isBatchOperation) {
      searchMessage.value = texts.value.leadDeleteError + ` (${error.message})`;
      searchStatus.value = "error";
    }
    console.error(`Error deleting lead ${leadId}:`, error);
    return { success: false, error };
  } finally {
    if (!isProcessingBatch.value) isProcessingBatch.value = false;
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
  () => {
    console.log(
      "Language changed, consider re-fetching or re-evaluating texts if necessary."
    );
  }
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
      initialLoadComplete.value = false;
      activeClientFilters.value = {};
      await fetchTabCounts(newUser.id);
      await fetchLeadsForCurrentUser(true);
    } else if (!newUser && oldUser) {
      await archiveUnsavedLeads(oldUser.id);
      tableData.value = [];
      rowSelection.value = {};
      initialLoadComplete.value = false;
      pagination.value.pageIndex = 0;
      sorting.value = [];
      currentTab.value = "new";
      // @ts-ignore
      table.setPageCount(0);
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
      if (!existingDropdown) {
        new Dropdown(batchActionsDropdownToggleRef.value);
      }
    }
  }
});

const isAdvancedCriteriaActive = computed(
  () =>
    (showAdvancedFilters.value && naturalLanguageQuery.value.trim() === "") ||
    filterTags.value.length > 0
);
function handleTabChangeFromPanel(newTab: LeadTab) {
  console.log(
    `%cLeadGenFormView: Received @update:currentTab -> ${newTab}`,
    "color: green; font-weight: bold;"
  );
  console.count("LeadGenFormView: handleTabChangeFromPanel called");
  changeTab(newTab);
}
function handleClientFiltersUpdate(updatedFilters: ActiveClientFilters) {
  console.log(
    "%cLeadGenFormView: Received @update:filters ->",
    "color: green; font-weight: bold;",
    JSON.stringify(updatedFilters)
  );
  console.count("LeadGenFormView: handleClientFiltersUpdate called");
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
    const [newRes, savedRes, archivedRes] = await Promise.all([
      supabase
        .from("leads")
        .select("id", { count: "exact", head: true })
        .match({ user_id: userId, tab: "new" }),
      supabase
        .from("leads")
        .select("id", { count: "exact", head: true })
        .match({ user_id: userId, tab: "saved" }),
      supabase
        .from("leads")
        .select("id", { count: "exact", head: true })
        .match({ user_id: userId, tab: "archived" }),
    ]);
    tabCounts.value = {
      new: newRes.count ?? 0,
      saved: savedRes.count ?? 0,
      archived: archivedRes.count ?? 0,
    };
  } catch (error) {
    console.error("Error fetching tab counts:", error);
    tabCounts.value = { new: 0, saved: 0, archived: 0 };
  }
}
function changeTab(newTab: LeadTab) {
  if (
    isLoadingLeads.value ||
    newTab === currentTab.value ||
    isProcessingBatch.value
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
  if (!userId) {
    return false;
  }
  try {
    const { error } = await supabase
      .from("leads")
      .update({ tab: "archived" })
      .match({ user_id: userId, tab: "new" });
    if (error) throw error;
    return true;
  } catch (e) {
    console.error("Error archiving unsaved leads:", e);
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
    console.error("Error checking for unsaved leads:", e);
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
    otherKeywords: "keywordsLabel",
  };
  // @ts-ignore
  return (texts.value as any)[map[type]] || type;
}
function addAdvancedInputsAsTags() {
  const i = advancedFilterInputs;
  if (typeof i.jobTitle === 'string' && i.jobTitle.trim()) addTag("jobTitle", i.jobTitle.trim());
  if (typeof i.industry === 'string' && i.industry)
    addTag(
      "industry",
      i.industry,
      languageStore.industries?.find((o) => o.value === i.industry)?.text
    );
  if (typeof i.location === 'string' && i.location.trim()) addTag("location", i.location.trim());
  if (typeof i.companySize === 'string' && i.companySize) addTag("companySize", i.companySize);
  if (typeof i.otherKeywords === 'string' && i.otherKeywords.trim())
    i.otherKeywords
      .trim()
      .split(",")
      .forEach((k) => {
        if (typeof k === 'string' && k.trim()) addTag("otherKeywords", k.trim());
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
  if (type !== "otherKeywords")
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
  const nq = typeof naturalLanguageQuery.value === 'string' && naturalLanguageQuery.value.trim();
  const tags = filterTags.value.length > 0;
  // Make sure advanced inputs are trimmed before checking if they are non-empty
  const untagged = Object.values(advancedFilterInputs).some(
    (v) => typeof v === 'string' && v.trim() !== ""
  );

  // If no natural language query and no tags, check if advanced filters are *active* and populated
  if (!nq && !tags && (showAdvancedFilters.value || untagged)) {
    // If showAdvancedFilters is active, and jobTitle or industry are required, check them
    // This logic relies on `isAdvancedCriteriaActive` which checks both `showAdvancedFilters` and `filterTags.length`
    if (showAdvancedFilters.value && (!naturalLanguageQuery.value || naturalLanguageQuery.value.trim() === "")) { // Only strict validation if NLP is empty AND advanced is shown
        if (typeof advancedFilterInputs.jobTitle === 'string' && !advancedFilterInputs.jobTitle.trim()) {
            searchMessage.value = texts.value.errorRequired(getFieldLabel("jobTitle"));
            searchStatus.value = "error";
            return false;
        }
        if (typeof advancedFilterInputs.industry === 'string' && !advancedFilterInputs.industry) { // Industry select will be empty string if not selected
            searchMessage.value = texts.value.errorRequired(getFieldLabel("industry"));
            searchStatus.value = "error";
            return false;
        }
    }
  }
  // This is the fallback if no criteria at all
  if (!nq && !tags && !untagged) {
    searchMessage.value = texts.value.noSearchCriteria;
    searchStatus.value = "error";
    return false;
  }
  return true;
}

async function submitLeadSearchCriteria() {
  if (isProcessingBatch.value || isSearchingLeads.value) return;
  if (
    showAdvancedFilters.value &&
    Object.values(advancedFilterInputs).some((v) => typeof v === 'string' && v.trim())
  )
    addAdvancedInputsAsTags();

  if (!validateSearchCriteria()) return;

  const user = authStore.user;
  if (user && (await hasUnsavedLeads(user.id))) {
    if (!confirm(texts.value.confirmArchiveUnsaved)) return;
    if (!(await archiveUnsavedLeads(user.id))) return;
    searchMessage.value = texts.value.unsavedLeadsArchived;
    searchStatus.value = "warning";
    await fetchTabCounts(user.id);
  }

  const payload: { mainQuery?: string; filters?: Record<string, any> } = {};
  if (typeof naturalLanguageQuery.value === 'string' && naturalLanguageQuery.value.trim())
    payload.mainQuery = naturalLanguageQuery.value.trim();
  if (filterTags.value.length > 0) {
    payload.filters = {};
    filterTags.value.forEach((t) => {
      // For JSONB array filters, the backend expects an array even if it's a single value from a select
      if (t.type === "otherKeywords" || t.type === "industry" || t.type === "companySize") {
        // Ensure that we create an array. If `payload.filters![t.type]` already exists and is an array, concatenate.
        // If it's single-valued or doesn't exist, create a new array with `t.value`.
        const currentFilterValue = payload.filters![t.type];
        if (Array.isArray(currentFilterValue)) {
            currentFilterValue.push(t.value);
        } else {
            payload.filters![t.type] = [t.value];
        }
      } else {
        payload.filters![t.type] = t.value;
      }
    });
  }
  if (
    !payload.mainQuery &&
    (!payload.filters || Object.keys(payload.filters).length === 0)
  ) {
    searchMessage.value = texts.value.noSearchCriteria;
    searchStatus.value = "error";
    return;
  }
  await handleTriggerN8nLeadSearch(payload);
}
async function handleTriggerN8nLeadSearch(criteriaPayload: any) {
  isSearchingLeads.value = true;
  if (searchStatus.value !== "warning") {
    searchMessage.value = null;
    searchStatus.value = null;
  }
  const session = authStore.session;
  if (!session?.access_token || !N8N_WEBHOOK_URL) {
    const currentMsg = searchMessage.value;
    const errorMsg = !session?.access_token
      ? texts.value.userNotAuthMessage
      : texts.value.n8nConfigError;
    searchMessage.value = currentMsg ? `${currentMsg}. ${errorMsg}` : errorMsg;
    searchStatus.value = "error";
    isSearchingLeads.value = false;
    return;
  }
  try {
    const res = await fetch(N8N_WEBHOOK_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${session.access_token}`,
      },
      body: JSON.stringify(criteriaPayload),
    });
    const result = await (res.headers
      .get("content-type")
      ?.includes("application/json")
      ? res.json()
      : { message: await res.text() });
    if (!res.ok)
      throw new Error(result.message || `N8N Error: ${res.statusText}`);

    const successMsg = result.message || texts.value.searchLeadsSuccess;
    searchMessage.value =
      searchStatus.value === "warning"
        ? `${searchMessage.value}. ${successMsg}`
        : successMsg;
    searchStatus.value = "success";

    naturalLanguageQuery.value = "";
    filterTags.value = [];

    if (currentTab.value !== "new") {
      changeTab("new");
    } else {
      pagination.value.pageIndex = 0;
      rowSelection.value = {};
      await fetchLeadsForCurrentUser(true);
      await fetchTabCounts(authStore.user?.id);
    }
  } catch (e: any) {
    console.error("Error triggering N8N lead search:", e);
    const errorTxt = texts.value.alertError + e.message;
    searchMessage.value =
      searchStatus.value === "warning"
        ? `${searchMessage.value}. ${errorTxt}`
        : errorTxt;
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

async function fetchLeadsForCurrentUser(forceRefresh = false) {
  console.log(
    `%cLeadGenFormView: fetchLeadsForCurrentUser CALLED. forceRefresh: ${forceRefresh}`,
    "color: red; font-weight: bold;",
    `\n  Current Tab: ${currentTab.value}`,
    `\n  Pagination: Index=${pagination.value.pageIndex}, Size=${pagination.value.pageSize}`,
    `\n  Sorting: ${JSON.stringify(sorting.value)}`,
    `\n  Active Client Filters: ${JSON.stringify(activeClientFilters.value)}`
  );
  console.count("LeadGenFormView: fetchLeadsForCurrentUser execution count");

  if (
    (isLoadingLeads.value && !forceRefresh) ||
    (isProcessingBatch.value && !forceRefresh)
  ) {
    console.log(
      "%cLeadGenFormView: fetchLeadsForCurrentUser SKIPPED (isLoading or isProcessingBatch)",
      "color: gray;"
    );
    return;
  }
  isLoadingLeads.value = true;

  const user = authStore.user;
  if (!user) {
    console.log(
      "%cLeadGenFormView: fetchLeadsForCurrentUser SKIPPED (no user)",
      "color: gray;"
    );
    tableData.value = [];
    rowSelection.value = {};
    isLoadingLeads.value = false;
    initialLoadComplete.value = true;
    // @ts-ignore
    table.setPageCount(0);
    tabCounts.value = { new: 0, saved: 0, archived: 0 };
    return;
  }
  const selectFields = `id, created_at, user_id, tab, lead_status, icebreaker, source_query_criteria, first_name, last_name, name, job_title, industry, location, company_name, company_size, phone, linkedIn_url, keywords, email, notes`;
  try {
    let query = supabase
      .from("leads")
      .select(selectFields, { count: "exact" })
      .eq("user_id", user.id)
      .eq("tab", currentTab.value);

    Object.entries(activeClientFilters.value).forEach(([key, values]) => {
      if (Array.isArray(values) && values.length > 0) { // Ensure values is a non-empty array
        const filterKey = key as keyof Lead;

        // Unified handling for JSONB array columns: keywords, industry, company_size
        if (filterKey === "keywords" || filterKey === "industry" || filterKey === "company_size") {
          // Map values to ensure they are strings and correctly quoted/escaped for the literal array
          const cleanedValues = values.map(v => `"${String(v).replace(/"/g, '""')}"`);
          const filterValue = `{${cleanedValues.join(',')}}`;
          query = query.filter(filterKey, 'ov', filterValue); // 'overlaps' operator
        } else if (filterKey === "lead_status") {
          // lead_status is likely a single text column or an enum
          if (values.length === 1) {
            query = query.eq(filterKey, values[0]);
          } else { // Multiple values
            query = query.in(filterKey, values);
          }
        } else if (
          ["job_title", "location", "company_name"].includes(filterKey)
        ) {
          const orConditions = values
            .map((val) => `${filterKey}.ilike.%${String(val).trim()}%`) // Ensure val is string before trim
            .join(",");
          if (orConditions) query = query.or(orConditions);
        }
      }
    });

    if (sorting.value.length > 0) {
      const sortColumn = sorting.value[0];
      const dbSortColumn = sortColumn.id;
      const allowedSort = [
        "name",
        "job_title",
        "company_name",
        "email",
        "created_at",
        "lead_status",
      ];
      if (allowedSort.includes(dbSortColumn)) {
        query = query.order(dbSortColumn, { ascending: !sortColumn.desc });
      } else {
        query = query.order("created_at", { ascending: false });
        if (dbSortColumn !== "created_at") {
          console.warn(
            `Unmapped/array sort attempt: ${dbSortColumn}. Defaulting to sort by created_at.`
          );
        }
      }
    } else {
      query = query.order("created_at", { ascending: false });
    }

    const page = pagination.value.pageIndex;
    const pageSize = pagination.value.pageSize;
    query = query.range(page * pageSize, (page + 1) * pageSize - 1);

    console.log(
      "%cLeadGenFormView: Supabase Query constructed. Attempting to execute...",
      "color: purple;",
      `Parameters - Tab: ${currentTab.value}, Page: ${page}, PageSize: ${pageSize}`
    );

    const { data: fetchedData, error, status, count } = await query;

    console.log(
      `%cLeadGenFormView: Supabase Response -> Status: ${status}, Count: ${count}, Fetched Data Length: ${
        fetchedData?.length || 0
      }`,
      "color: purple; font-weight: bold;",
      error ? `Error: ${error.message}` : "No Supabase error."
    );

    if (error && status !== 406) {
      if (error.message.includes("JWT")) {
        searchMessage.value = texts.value.accessDeniedMessage;
        searchStatus.value = "error";
        await authStore.signOut();
      } else {
        console.error("Supabase fetch error:", error);
      }
      tableData.value = [];
      // @ts-ignore
      table.setPageCount(0);
    } else {
      tableData.value = fetchedData || [];
      const totalCount = count || 0;
      const newPageCount = Math.ceil(totalCount / pageSize);
      // @ts-ignore
      table.setPageCount(newPageCount);

      const currentPageIndex = pagination.value.pageIndex;
      console.log(
        `%cLeadGenFormView: Pagination correction check -> CurrentIndex: ${currentPageIndex}, NewPageCount: ${newPageCount}, TotalCount: ${totalCount}, CurrentTab: ${currentTab.value}`,
        "color: #007bff;"
      );

      if (currentPageIndex >= newPageCount && newPageCount > 0) {
        console.log(
          `%cLeadGenFormView: Correcting pagination. Current page (${currentPageIndex}) is out of new bounds (${
            newPageCount - 1
          }). Setting to ${newPageCount - 1}.`,
          "color: #007bff; font-style: italic;"
        );
        pagination.value.pageIndex = newPageCount - 1;
      } else if (
        currentPageIndex > 0 &&
        totalCount === 0 &&
        currentTab.value !== "new"
      ) {
        console.log(
          `%cLeadGenFormView: Correcting pagination. Current page (${currentPageIndex}) has no items on non-'new' tab. Setting to page 0.`,
          "color: #007bff; font-style: italic;"
        );
        pagination.value.pageIndex = 0;
      }
    }
  } catch (e: any) {
    console.error(
      "%cLeadGenFormView: ERROR caught in fetchLeadsForCurrentUser try-catch block:",
      "background: red; color: white; font-weight: bold;",
      e
    );
    if (!searchMessage.value) {
      searchMessage.value = texts.value.alertError + (e.message || "Unknown error");
      searchStatus.value = "error";
    }
    tableData.value = [];
    // @ts-ignore
    table.setPageCount(0);
  } finally {
    isLoadingLeads.value = false;
    if (!initialLoadComplete.value) initialLoadComplete.value = true;
    console.log(
      "%cLeadGenFormView: fetchLeadsForCurrentUser FINISHED.",
      "color: red;"
    );
  }
}

function getStatusBadgeClass(status?: string | null): string {
  if (!status) return "bg-secondary text-white";
  switch (status.toLowerCase().replace(/\s+/g, "")) {
    case "newprospect":
      return "bg-primary text-white";
    case "icebreakersent":
    case "contacted":
      return "bg-success text-white";
    case "follow-up":
      return "bg-warning text-dark";
    case "replied":
      return "bg-info text-dark";
    case "archived":
      return "bg-secondary text-white";
    default:
      return "bg-light text-dark border";
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
  }
});
</script>