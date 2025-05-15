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
                      :aria-label="
                        (texts.removeFilterTooltip || 'Remove') +
                        ' ' +
                        tag.label
                      "
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
                            disabled: !canBatchRestoreToNewFromSaved || isProcessingBatch,
                          }"
                          @click.prevent="
                            !(!canBatchRestoreToNewFromSaved || isProcessingBatch) &&
                              batchRestoreSelected()
                          "
                          >{{ texts.batchRestoreButton }}</a 
                        >
                      </li>
                      <li>
                        <a
                          class="dropdown-item"
                          href="#"
                          :class="{
                            disabled: !canBatchArchiveSaved || isProcessingBatch,
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
                       <li><hr class="dropdown-divider"></li>
                      <li>
                        <a
                          class="dropdown-item text-danger"
                          href="#"
                          :class="{
                            disabled: !canBatchDeleteArchived || isProcessingBatch,
                          }"
                          @click.prevent="
                            !(!canBatchDeleteArchived || isProcessingBatch) &&
                              batchDeleteSelected()
                          "
                          >{{ texts.batchDeleteButton }}</a
                        >
                      </li>
                    </template>
                  </ul>
                </div>
              </div>

              <div class="d-flex align-items-center">
                <button
                  class="btn btn-sm btn-icon me-2"
                  @click="toggleSearchForm"
                  :title="
                    showSearchForm ? texts.searchFormToggleHideTooltip : texts.searchFormToggleShowTooltip
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
                <div class="spinner-border text-primary mb-3" role="status"></div>
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
              <div v-else-if="tableData.length === 0" key="empty-generic" class="loading-empty-state">
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
                          'sorting-desc': header.column.getIsSorted() === 'desc',
                        }"
                        :style="getColumnStyle(header)"
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
                        :style="getColumnStyle(cell)"
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
import type { Session, PostgrestFilterBuilder } from "@supabase/supabase-js";
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
} from "@tanstack/vue-table";
import type { LeadTab } from "@/types/tabs";
import { Dropdown } from "bootstrap";

declare module "@tanstack/vue-table" {
  interface ColumnMeta<TData, TValue> {
    style?: Record<string, string>;
  }
}

interface Lead {
  id: string;
  created_at: string;
  user_id: string;
  tab: LeadTab | null;
  first_name?: string | null;
  last_name?: string | null;
  name?: string | null;
  job_title?: string | null;
  industry?: string[] | null;
  location?: string | null;
  company_name?: string | null;
  company_size?: string[] | null;
  phone?: string | null;
  linkedIn_url?: string | null;
  keywords?: any | null;
  email?: string | null;
  notes?: string | null;
  lead_status?: string | null;
  icebreaker?: string | null;
  source_query_criteria?: any | null;
}
interface FilterTag {
  id: string;
  type: "jobTitle" | "industry" | "location" | "companySize" | "otherKeywords";
  value: string;
  displayValue: string;
  label: string;
}

const languageStore = useLanguageStore();
const authStore = useAuthStore();

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

const texts = computed(() => {
  const defaults = {
    mainQueryLabel:
      "Briefly describe the type of prospects you're looking for:",
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
    actionSaveTooltip: "Save Lead", // More descriptive tooltip for the actual action
    actionArchiveTooltip: "Archive Lead",
    actionRestoreTooltip: "Move to New",
    actionDeleteTooltip: "Delete Lead",
    actionMoveToSavedTooltip: "Move to Saved",
    tooltipSave: "Save", // Simple hover text
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
  };
  if (
    languageStore &&
    typeof languageStore.texts === "object" &&
    Object.keys(languageStore.texts).length > 0
  ) {
    const mergedTexts = { ...defaults };
    for (const key in languageStore.texts) {
      if (Object.prototype.hasOwnProperty.call(languageStore.texts, key)) {
        // @ts-ignore
        mergedTexts[key as keyof typeof mergedTexts] = languageStore.texts[
          key
        ] as any;
      }
    }
    return mergedTexts;
  }
  return defaults;
});

const noLeadsMessageForTab = computed(() => {
  switch (currentTab.value) {
    case 'new':
      return texts.value.noNewLeadsYet;
    case 'saved':
      return texts.value.noSavedLeads;
    case 'archived':
      return texts.value.noArchivedLeads;
    default:
      return texts.value.noLeadsFound;
  }
});

const columns = computed<ColumnDef<Lead, any>[]>(() => [
  columnHelper.display({
    id: "select",
    header: ({ table }) =>
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
    cell: ({ row }) =>
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
        zIndex: 18, 
        backgroundColor: "var(--card-bg-current)",
        borderRight: "1px solid var(--border-color-current)",
      },
    },
  }),
  columnHelper.display({
    id: "actions",
    header: () => texts.value.colActions,
    cell: (info) => {
      const lead = info.row.original;
      const buttons = [];

      if (currentTab.value === "new" && lead.tab === "new") {
        buttons.push(
          h(
            "button",
            {
              class: "btn btn-sm btn-outline-success",
              title: texts.value.tooltipSave, // Use simple tooltip
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
              title: texts.value.tooltipArchive, // Use simple tooltip
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
              title: texts.value.tooltipRestore, // Use simple tooltip
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
              title: texts.value.tooltipArchive, // Use simple tooltip
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
              title: texts.value.tooltipMoveToSaved, // Use simple tooltip
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
              title: texts.value.tooltipDelete, // Use simple tooltip
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
        zIndex: 17, 
        backgroundColor: "var(--card-bg-current)",
        borderRight: "1px solid var(--border-color-current)",
      },
    },
  }),
  columnHelper.accessor("name", {
    id: "name",
    header: () => texts.value.colName,
    cell: (info) =>
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
        zIndex: 16, 
        backgroundColor: "var(--card-bg-current)",
        borderRight: "1px solid var(--border-color-current)",
      },
    },
  }),
  columnHelper.accessor("job_title", {
    id: "job_title",
    header: () => texts.value.colJobTitle,
    cell: (info) => info.getValue() || "N/A",
    enableSorting: true,
    size: 200,
    meta: { style: { minWidth: "200px", width: "200px" } },
  }),
  columnHelper.accessor("industry", {
    id: "industry",
    header: () => texts.value.colIndustry,
    cell: (info) => {
      const industries = info.getValue();
      if (Array.isArray(industries) && industries.length > 0) {
        return h(
          "div",
          { style: "max-width: 200px; white-space: normal;" },
          industries.map((ind) =>
            h("span", { class: "badge bg-info text-dark me-1 mb-1" }, ind)
          )
        );
      }
      return Array.isArray(industries) ? "N/A" : industries || "N/A";
    },
    enableSorting: true,
    size: 160,
    meta: { style: { minWidth: "160px", width: "160px" } },
  }),
  columnHelper.accessor("location", {
    id: "location",
    header: () => texts.value.colLocation,
    cell: (info) => info.getValue() || "N/A",
    enableSorting: true,
    size: 150,
    meta: { style: { minWidth: "150px", width: "150px" } },
  }),
  columnHelper.accessor("company_name", {
    id: "company_name",
    header: () => texts.value.colCompanyName,
    cell: (info) => info.getValue() || "N/A",
    enableSorting: true,
    size: 180,
    meta: { style: { minWidth: "180px", width: "180px" } },
  }),
  columnHelper.accessor("company_size", {
    id: "company_size",
    header: () => texts.value.colCompanySize,
    cell: (info) => {
      const sizes = info.getValue();
      if (Array.isArray(sizes) && sizes.length > 0) {
        return h(
          "div",
          { style: "max-width: 150px; white-space: normal;" },
          sizes.map((size) =>
            h("span", { class: "badge bg-secondary me-1 mb-1" }, size)
          )
        );
      }
      return Array.isArray(sizes) ? "N/A" : sizes || "N/A";
    },
    enableSorting: true,
    size: 110,
    meta: { style: { minWidth: "110px", width: "110px" } },
  }),
  columnHelper.accessor("phone", {
    id: "phone",
    header: () => texts.value.colPhone,
    cell: (info) => info.getValue() || "N/A",
    enableSorting: false,
    size: 140,
    meta: { style: { minWidth: "140px", width: "140px" } },
  }),
  columnHelper.accessor("linkedIn_url", {
    id: "linkedIn_url",
    header: () => texts.value.colLinkedIn,
    cell: (info) => {
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
    cell: (info) => {
      const keywords = info.getValue();
      let kwsArray: string[] = [];
      if (Array.isArray(keywords)) {
        kwsArray = keywords.filter(Boolean).map(String);
      } else if (typeof keywords === "string" && keywords.trim() !== "") {
        kwsArray = keywords
          .split(",")
          .map((kw) => kw.trim())
          .filter(Boolean);
      } else if (
        keywords &&
        typeof keywords === "object" &&
        !Array.isArray(keywords)
      ) {
        kwsArray = Object.values(keywords).filter(Boolean).map(String);
      }
      if (kwsArray.length > 0) {
        return h(
          "div",
          { style: "max-width: 250px; white-space: normal;" },
          kwsArray.map((kw) =>
            h("span", { class: "badge bg-secondary me-1 mb-1" }, kw)
          )
        );
      }
      return "N/A";
    },
    enableSorting: false,
    size: 250,
    meta: { style: { minWidth: "250px", width: "250px" } },
  }),
  columnHelper.accessor("email", {
    id: "email",
    header: () => texts.value.colEmail,
    cell: (info) => info.getValue() || "N/A",
    enableSorting: true,
    size: 220,
    meta: { style: { minWidth: "220px", width: "220px" } },
  }),
  columnHelper.accessor("notes", {
    id: "notes",
    header: () => texts.value.colNotes,
    cell: (info) => info.getValue() || "N/A",
    enableSorting: false,
    size: 250,
    meta: { style: { minWidth: "250px", width: "250px" } },
  }),
  columnHelper.accessor("created_at", {
    id: "created_at",
    header: () => texts.value.colCreatedAt,
    cell: (info) =>
      info.getValue() ? new Date(info.getValue()).toLocaleDateString() : "N/A",
    enableSorting: true,
    size: 100,
    meta: { style: { minWidth: "100px", width: "100px" } },
  }),
  columnHelper.accessor("lead_status", {
    id: "lead_status",
    header: () => texts.value.colStatus,
    cell: (info) => {
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
        zIndex: 16, 
        backgroundColor: "var(--card-bg-current)",
        borderLeft: "1px solid var(--border-color-current)",
      },
    },
  }),
]);

function getColumnStyle(headerOrCell: any) {
  const baseStyle: Record<string, string> = {
    "user-select":
      headerOrCell.column.getCanSort() && !isProcessingBatch.value
        ? "pointer"
        : "none",
    verticalAlign: "middle",
  };
  if (!headerOrCell.column.columnDef.meta?.style?.width) {
    baseStyle.width = `${headerOrCell.column.columnDef.size}px`;
  }
  if (!headerOrCell.column.columnDef.meta?.style?.minWidth) {
    baseStyle.minWidth = `${headerOrCell.column.columnDef.size}px`;
  }
  const metaStyle = headerOrCell.column.columnDef.meta?.style || {};
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
  onRowSelectionChange: (updater) => {
    if (isProcessingBatch.value) return;
    rowSelection.value =
      typeof updater === "function" ? updater(rowSelection.value) : updater;
  },
  onSortingChange: (updater) => {
    if (isProcessingBatch.value) return;
    sorting.value =
      typeof updater === "function" ? updater(sorting.value) : updater;
    fetchLeadsForCurrentUser(true);
  },
  onPaginationChange: (updater) => {
    if (isProcessingBatch.value) return;
    pagination.value =
      typeof updater === "function" ? updater(pagination.value) : updater;
    fetchLeadsForCurrentUser(true);
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

// --- BATCH ACTION ELIGIBILITY COMPUTED PROPERTIES ---
const canBatchSave = computed(
  () =>
    currentTab.value === 'new' &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table.getSelectedRowModel().rows.some((row) => row.original.tab === "new")
);
const canBatchArchiveNew = computed(
  () =>
    currentTab.value === 'new' &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table.getSelectedRowModel().rows.some((row) => row.original.tab === "new")
);
const canBatchRestoreToNewFromSaved = computed(
  () =>
    currentTab.value === 'saved' &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table.getSelectedRowModel().rows.some((row) => row.original.tab === "saved")
);
const canBatchArchiveSaved = computed(
  () =>
    currentTab.value === 'saved' &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table.getSelectedRowModel().rows.some((row) => row.original.tab === "saved")
);
const canBatchMoveToSaved = computed(
  () =>
    currentTab.value === 'archived' &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0 &&
    table.getSelectedRowModel().rows.some((row) => row.original.tab === "archived")
);
const canBatchDeleteArchived = computed(
  () =>
    currentTab.value === 'archived' &&
    !isProcessingBatch.value &&
    selectedRowCount.value > 0
);


const batchProcessLeads = async (
  targetTabOrAction: LeadTab | "delete",
  actionNameKey:
    | "confirmBatchSave"
    | "confirmBatchArchive"
    | "confirmBatchRestore"
    | "confirmBatchDelete"
    | "confirmBatchMoveToSaved", // Added new key
  filterFn: (lead: Lead) => boolean,
  operationFn: (leadId: string, target?: LeadTab) => Promise<{success: boolean, error?: any}>
) => {
  if (isProcessingBatch.value) return;
  const selectedRows = table.getSelectedRowModel().rows;
  if (selectedRows.length === 0) return;

  const leadsToProcess = selectedRows
    .map((row) => row.original)
    .filter(filterFn);

  const actionNameForNoLeadsMsg = actionNameKey
    .replace("confirmBatch", "")
    .toLowerCase();

  if (leadsToProcess.length === 0 && targetTabOrAction !== 'delete') { // Delete might proceed if any selected, even if filterFn then reduces to 0.
    searchMessage.value = texts.value.noLeadsEligibleForAction(
      actionNameForNoLeadsMsg
    );
    searchStatus.value = "warning";
    return;
  }
  
  // @ts-ignore
  const confirmMessageFn = texts.value[actionNameKey];
  if (!confirm(confirmMessageFn(leadsToProcess.length))) return;

  isProcessingBatch.value = true;
  const processingActionName = actionNameKey.replace("confirmBatch", ""); // Simple way to get 'Save', 'Archive', etc.
  searchMessage.value = `Processing ${processingActionName} batch... (${leadsToProcess.length} leads)`;
  searchStatus.value = null;

  let successCount = 0;
  let errorCount = 0;

  const results = await Promise.allSettled(
    leadsToProcess.map((lead) => operationFn(lead.id, targetTabOrAction !== 'delete' ? targetTabOrAction : undefined))
  );

  results.forEach((result) => {
    if (result.status === "fulfilled" && result.value && result.value.success) {
      successCount++;
    } else {
      errorCount++;
      console.error(
        `Batch ${processingActionName} error for a lead:`,
        result.status === "rejected" ? result.reason : result.value
      );
    }
  });

  // @ts-ignore
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
  batchProcessLeads("saved", "confirmBatchSave",
    (lead) => lead.tab === "new",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchArchiveSelected = () => // This handler is called by both 'new' and 'saved' tab archive buttons
  batchProcessLeads("archived", "confirmBatchArchive",
    (lead) => currentTab.value === 'new' ? lead.tab === "new" : lead.tab === "saved", // Filter based on current tab context
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchRestoreSelected = () => // This is for 'saved' tab -> 'new'
  batchProcessLeads("new", "confirmBatchRestore",
    (lead) => lead.tab === "saved", // Filter for saved leads
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchMoveToSavedSelected = () => // New handler for 'archived' -> 'saved'
  batchProcessLeads("saved", "confirmBatchMoveToSaved",
    (lead) => lead.tab === "archived",
    (leadId, tab) => updateLeadTab(leadId, tab!, true)
  );
const batchDeleteSelected = () =>
  batchProcessLeads("delete", "confirmBatchDelete",
    (lead) => lead.tab === "archived", // Ensure we only delete from archived in this context
    (leadId) => deleteLead(leadId, true)
);

async function updateLeadTab(
  leadId: string,
  newTab: LeadTab,
  isBatchOperation: boolean = false
): Promise<{ success: boolean; leadId?: string; newTab?: LeadTab; error?: any }> {
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
    if(!isBatchOperation) isProcessingBatch.value = false;
  }
}

async function deleteLead(leadId: string, isBatchOperation: boolean = false): Promise<{success: boolean, error?: any}> {
  if (!isBatchOperation) {
    isProcessingBatch.value = true;
    if (searchStatus.value !== 'error') {
        searchMessage.value = null;
        searchStatus.value = null;
    }
  }

  try {
    const { error } = await supabase
      .from("leads")
      .delete()
      .eq("id", leadId);

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
    if(!isBatchOperation) isProcessingBatch.value = false;
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
    console.log("Language changed, consider re-fetching or re-evaluating texts if necessary.");
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
    (showAdvancedFilters.value && !naturalLanguageQuery.value.trim()) ||
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
  if (i.jobTitle.trim()) addTag("jobTitle", i.jobTitle.trim());
  if (i.industry)
    addTag(
      "industry",
      i.industry,
      languageStore.industries?.find((o) => o.value === i.industry)?.text
    );
  if (i.location.trim()) addTag("location", i.location.trim());
  if (i.companySize) addTag("companySize", i.companySize);
  if (i.otherKeywords.trim())
    i.otherKeywords
      .trim()
      .split(",")
      .forEach((k) => {
        if (k.trim()) addTag("otherKeywords", k.trim());
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
  const nq = !!naturalLanguageQuery.value.trim();
  const tags = filterTags.value.length > 0;
  const untagged = Object.values(advancedFilterInputs).some(
    (v) => v && String(v).trim() !== ""
  );
  if (!nq && !tags && (showAdvancedFilters.value || untagged)) {
    if (!advancedFilterInputs.jobTitle.trim()) {
      searchMessage.value = texts.value.errorRequired(
        getFieldLabel("jobTitle")
      );
      searchStatus.value = "error";
      return false;
    }
    if (!advancedFilterInputs.industry) {
      searchMessage.value = texts.value.errorRequired(
        getFieldLabel("industry")
      );
      searchStatus.value = "error";
      return false;
    }
  }
  if (!nq && !tags && !untagged) {
    searchMessage.value = texts.value.noSearchCriteria;
    searchStatus.value = "error";
    return false;
  }
  return true;
}
async function submitLeadSearchCriteria() {
 if (isProcessingBatch.value || isSearchingLeads.value)
    return;
  if (
    showAdvancedFilters.value &&
    Object.values(advancedFilterInputs).some((v) => String(v).trim())
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
  if (naturalLanguageQuery.value.trim())
    payload.mainQuery = naturalLanguageQuery.value.trim();
  if (filterTags.value.length > 0) {
    payload.filters = {};
    filterTags.value.forEach((t) => {
      if (t.type === "otherKeywords") {
        payload.filters!.otherKeywords = [
          ...(payload.filters!.otherKeywords || []),
          t.value,
        ];
      } else {
        payload.filters![t.type] = t.value;
      }
    });
  }
  if (
    !payload.mainQuery &&
    (!payload.filters || !Object.keys(payload.filters).length)
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
  if ((isLoadingLeads.value && !forceRefresh) || (isProcessingBatch.value && !forceRefresh) ) {
    return;
  }
  isLoadingLeads.value = true;

  const user = authStore.user;
  if (!user) {
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
    let query: PostgrestFilterBuilder<any, any, Lead[], "leads", any> = supabase
      .from("leads")
      .select(selectFields, { count: "exact" })
      .eq("user_id", user.id)
      .eq("tab", currentTab.value);

    Object.entries(activeClientFilters.value).forEach(([key, values]) => {
      if (values && values.length > 0) {
        const filterKey = key as keyof Lead;
        if (filterKey === "keywords") {
          const keywordOrConditions = values
            .map((val) => `${filterKey}.ilike.%${val}%`)
            .join(",");
          if (keywordOrConditions) query = query.or(keywordOrConditions);
        } else if (filterKey === "industry" || filterKey === "company_size") {
            if (Array.isArray(values) && values.every(v => typeof v === 'string')) {
                const filterValue = `{${values.join(',')}}`;
                query = query.filter(filterKey, 'ov', filterValue);
            }
        } else if (filterKey === "lead_status" && values.length === 1) {
            query = query.eq(filterKey, values[0]);
        } else if (["job_title", "location", "company_name"].includes(filterKey)) {
          const orConditions = values
            .map((val) => `${filterKey}.ilike.%${val}%`)
            .join(",");
          if (orConditions) query = query.or(orConditions);
        }
      }
    });
    if (sorting.value.length > 0) {
      const sortColumn = sorting.value[0];
      const dbSortColumn = sortColumn.id;
      const allowedSort = ["name", "job_title", "company_name", "email", "created_at", "lead_status"];
      if (allowedSort.includes(dbSortColumn))
        query = query.order(dbSortColumn, { ascending: !sortColumn.desc });
      else {
        query = query.order("created_at", { ascending: false });
        if (dbSortColumn !== "created_at") console.warn(`Unmapped/array sort attempt: ${dbSortColumn}`);
      }
    } else {
      query = query.order("created_at", { ascending: false });
    }
    const page = pagination.value.pageIndex;
    const pageSize = pagination.value.pageSize;
    query = query.range(page * pageSize, (page + 1) * pageSize - 1);

    const { data: fetchedData, error, status, count } = await query;

    if (error && status !== 406) {
      if (error.message.includes("JWT")) {
        searchMessage.value = texts.value.accessDeniedMessage;
        searchStatus.value = "error";
        await authStore.signOut();
      } else {
        console.error("Supabase fetch error:", error);
        throw error;
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
      if (currentPageIndex >= newPageCount && newPageCount > 0) {
        pagination.value.pageIndex = newPageCount - 1;
      } else if (currentPageIndex > 0 && totalCount === 0 && currentTab.value !== 'new') {
        pagination.value.pageIndex = 0;
      }
    }
  } catch (e: any) {
    console.error("ERROR caught in fetchLeadsForCurrentUser:", e);
    if (!searchMessage.value) {
        searchMessage.value = texts.value.alertError + e.message;
        searchStatus.value = "error";
    }
    tableData.value = [];
    // @ts-ignore
    table.setPageCount(0);
  } finally {
    isLoadingLeads.value = false;
    if (!initialLoadComplete.value) initialLoadComplete.value = true;
  }
}

function getStatusBadgeClass(status?: string | null): string {
  if (!status) return "bg-secondary text-white";
  switch (status.toLowerCase().replace(/\s+/g, "")) {
    case "newprospect": return "bg-primary text-white";
    case "icebreakersent": case "contacted": return "bg-success text-white";
    case "follow-up": return "bg-warning text-dark";
    case "replied": return "bg-info text-dark";
    case "archived": return "bg-secondary text-white";
    default: return "bg-light text-dark border";
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

<style scoped>
/* --- Base & Form Styles --- */
.lead-gen-view-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  background-color: var(--content-bg-current);
}
.view-main-content {
  display: flex;
  flex-grow: 1;
  overflow: hidden;
  min-height: 0;
}
.filter-sidebar-view {
  width: 18%;
  min-width: 280px;
  max-width: 450px;
  background-color: var(--card-bg-current);
  border-right: 1px solid var(--border-color-current);
  display: flex;
  flex-direction: column;
  transition: width 0.2s ease-out, min-width 0.2s ease-out;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 1px 0 3px rgba(0, 0, 0, 0.04);
}
.filter-sidebar-view.collapsed {
  width: 60px;
  min-width: 60px;
}
.filter-sidebar-view.collapsed .filter-content,
.filter-sidebar-view.collapsed .filter-header h5 {
  display: none;
}
.filter-sidebar-view .filter-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border-color-current);
  height: 60px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.filter-sidebar-view .filter-header h5 {
  color: var(--text-color-base-current);
  margin-bottom: 0;
}
.filter-sidebar-view .filter-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0rem;
}
.content-area-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 1rem;
  gap: 1rem;
}

/* --- Search Panel Specific Styling --- */
.search-panel {
  padding: 1.5rem;
  background-color: var(--card-bg-current);
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
  flex-shrink: 0;
  transition: max-height 0.3s ease-out, padding 0.3s ease-out,
    opacity 0.3s ease-out;
  max-height: 1000px;
  overflow: hidden;
  opacity: 1;
  border: 1px solid var(--border-color-current);
}
.search-panel.collapsed {
  max-height: 60px;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}
.search-panel.collapsed .search-panel-body {
  display: none;
}
.search-panel-header .search-panel-title {
  color: var(--text-color-base-current);
  font-weight: 600;
  font-size: 1.05rem;
}
.search-panel-header .search-panel-toggle-icon.btn-icon {
  color: var(--text-muted-current);
}
.search-panel-header .search-panel-toggle-icon.btn-icon:hover {
  color: var(--text-color-base-current);
}
.search-panel-body .search-panel-label.form-label {
  color: var(--text-color-base-current);
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 0.35rem;
}
.search-panel-body .search-panel-textarea.form-control-lg {
  background-color: var(--card-bg-current);
  color: var(--text-color-base-current);
  border-color: var(--border-color-current);
  font-size: 1rem;
}
.search-panel-body .search-panel-textarea.form-control-lg::placeholder {
  color: var(--text-muted-current);
  opacity: 0.7;
}
.search-panel-body .search-panel-textarea.form-control-lg:focus {
  border-color: var(--primary-color-current);
  box-shadow: 0 0 0 0.25rem
    color-mix(in srgb, var(--primary-color-current) 25%, transparent);
  background-color: var(--card-bg-current);
}
.advanced-filters-panel-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s ease-in-out, opacity 0.3s ease-in-out 0.1s;
  opacity: 0;
}
.advanced-filters-panel-content.show {
  max-height: 1000px;
  opacity: 1;
}
.advanced-filters-panel-content .search-panel-divider {
  border-top-color: var(--border-color-current);
  opacity: 0.5;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}
.advanced-filters-panel-content .search-panel-adv-label.form-label {
  font-size: 0.85rem;
  color: var(--text-muted-current);
}
.advanced-filters-panel-content .search-panel-adv-input.form-control-sm,
.advanced-filters-panel-content .search-panel-adv-select.form-select-sm {
  background-color: var(--card-bg-current);
  color: var(--text-color-base-current);
  border-color: var(--border-color-current);
}
.advanced-filters-panel-content
  .search-panel-adv-input.form-control-sm::placeholder,
.advanced-filters-panel-content
  .search-panel-adv-select.form-select-sm
  option[value=""] {
  color: var(--text-muted-current);
  opacity: 0.7;
}
.advanced-filters-panel-content .search-panel-adv-input.form-control-sm:focus,
.advanced-filters-panel-content .search-panel-adv-select.form-select-sm:focus {
  border-color: var(--primary-color-current);
  box-shadow: 0 0 0 0.2rem
    color-mix(in srgb, var(--primary-color-current) 20%, transparent);
  background-color: var(--card-bg-current);
}
.search-panel-tag.tag-pill {
  background-color: var(--primary-light-current);
  color: var(--primary-color-current);
  border: 1px solid var(--primary-color-current);
  font-weight: 500;
}
.search-panel-tag.tag-pill .btn-close {
  --bs-btn-close-color: var(--primary-color-current);
}
.search-panel-alert.alert {
  border-width: 0px;
  border-left-width: 4px;
}
.tag-pill {
  display: inline-flex;
  align-items: center;
  background-color: var(--primary-light-current);
  color: var(--primary-dark-current);
  border-radius: 9999px;
  padding: 0.3rem 0.75rem;
  font-size: 0.875rem;
}
.tag-pill .btn-close-sm {
  font-size: 0.65rem;
  opacity: 0.6;
}
.tag-pill .btn-close-sm:hover {
  opacity: 1;
}

/* --- Table Styles --- */
.table-section-view {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: var(--card-bg-current);
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
  overflow: hidden;
  min-height: 0;
  border: 1px solid var(--border-color-current);
}
.table-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color-current);
  flex-shrink: 0;
  background-color: var(--card-bg-current);
  z-index: 30; 
  position: relative;
}
.table-content {
  flex-grow: 1;
  overflow: hidden; 
  position: relative;
  display: flex;
  flex-direction: column;
}
.loading-empty-state {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: var(--text-muted-current);
}
.table-wrapper {
  flex-grow: 1;
  overflow: auto; 
  position: relative;
}
.lead-table {
  width: 100%;
  border-collapse: separate; 
  border-spacing: 0;
  min-width: 2430px; 
}

.lead-table thead tr {
  position: sticky;
  top: 0;
  z-index: 25; 
}

.lead-table thead th {
  padding: 0.75rem 1rem;
  font-weight: 600;
  color: var(--text-color-base-current);
  text-align: left;
  vertical-align: middle; 
  background-color: var(--card-bg-current); 
  border-bottom: 2px solid var(--border-color-current); 
}

.lead-table thead th .sort-indicator {
  min-width: 1em;
  display: inline-block;
}
.lead-table thead th .sort-indicator .bi-sort-up,
.lead-table thead th .sort-indicator .bi-sort-down {
  color: var(--sort-indicator-active-color-current);
}
.lead-table thead th .sort-indicator .bi-filter {
  color: var(--sort-indicator-inactive-color-current);
  opacity: var(--sort-indicator-inactive-opacity-current);
}
.lead-table tbody td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-color-current);
  vertical-align: middle; 
  font-size: 0.875rem;
  color: var(--text-muted-current);
  background-color: var(--card-bg-current); 
}
.lead-table tbody tr:hover td {
  background-color: var(--table-row-hover-bg-current);
  color: var(--table-row-hover-text-current);
}
.lead-table tbody tr.table-active td {
  background-color: var(--primary-light-current);
  color: var(--primary-dark-current);
}

.lead-table tbody tr:hover td[style*="position: sticky"],
.lead-table tbody tr.table-active td[style*="position: sticky"] {
  background-color: inherit; 
}

.lead-table td[data-column-id="keywords"] > div,
.lead-table td[data-column-id="notes"] {
  white-space: normal !important;
  text-overflow: clip !important;
  overflow: visible !important;
}
.table-action-buttons .btn {
  padding: 0.25rem 0.5rem;
}
.table-action-buttons .btn:last-child {
  margin-right: 0;
}
.table-action-buttons .btn-outline-success {
  --bs-btn-color: var(--table-action-btn-success-color-current);
  --bs-btn-border-color: var(--table-action-btn-success-color-current);
  --bs-btn-hover-color: var(--table-action-btn-text-hover-current);
  --bs-btn-hover-bg: var(--table-action-btn-success-hover-bg-current);
  --bs-btn-hover-border-color: var(--table-action-btn-success-hover-bg-current);
}
.table-action-buttons .btn-outline-warning {
  --bs-btn-color: var(--table-action-btn-success-color-current);
  --bs-btn-border-color: var(--table-action-btn-success-color-current);
  --bs-btn-hover-color: #000;
  --bs-btn-hover-bg: var(--table-action-btn-warning-hover-bg-current);
  --bs-btn-hover-border-color: var(--table-action-btn-warning-hover-bg-current);
}
.table-action-buttons .btn-outline-secondary {
  --bs-btn-color: var(--table-action-btn-success-color-current);
  --bs-btn-border-color: var(--table-action-btn-success-color-current);
  --bs-btn-hover-color: var(--table-action-btn-text-hover-current);
  --bs-btn-hover-bg: var(--table-action-btn-secondary-hover-bg-current);
  --bs-btn-hover-border-color: var(
    --table-action-btn-secondary-hover-bg-current
  );
}
.table-footer {
  padding: 0.75rem 1.5rem;
  border-top: 1px solid var(--border-color-current);
  flex-shrink: 0;
  background-color: var(--card-bg-current);
  z-index: 5; 
  position: relative;
}

/* --- Utility & Animation Styles --- */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease; 
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.spin-animation {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.cursor-pointer {
  cursor: pointer;
}
.display-1.text-muted {
  opacity: 0.3;
  font-size: 3.5rem;
}
.lead-table td .form-check-input,
.lead-table th .form-check-input {
  vertical-align: middle;
}
.processing-row-disabled {
  opacity: 0.6;
  pointer-events: none;
}
.dropdown-item.disabled,
.dropdown-item:disabled {
  pointer-events: none;
  opacity: 0.65;
  background-color: transparent; 
  color: var(--bs-dropdown-link-disabled-color);
}
</style>