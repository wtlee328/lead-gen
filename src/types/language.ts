// src/types/language.ts

export interface Industry {
    value: string;
    zh: string;
    en: string;
}

export type LanguageCode = 'zh' | 'en';

export interface Translations {
    // --- General App/Page Titles & Descriptions ---
    dashboardTitle: string;
    formDescription: string;

    // --- Filter Panel Sidebar ---
    filtersTitle: string;
    tabsTitle: string;
    tabNew: string;
    tabSaved: string;
    tabArchived: string;
    addFilterPlaceholder: string;
    selectFilterPlaceholder: string;
    clearAllFiltersButton: string;
    clearFilterSectionTooltip: string;

    // --- Search Criteria Section (Main Form) ---
    mainQueryLabel: string;
    mainQueryPlaceholder: string;
    advancedBtnTextShow: string;
    advancedBtnTextHide: string;
    jobTitleLabel: string;
    industryLabel: string;
    industryPlaceholder: string;
    locationLabel: string;
    companySizeLabel: string;
    companySizePlaceholder: string;
    keywordsLabel: string;
    advKeywordsPlaceholder: string;
    addFiltersBtnText: string;
    tagAreaLabel: string;
    removeFilterTooltip: string;
    searchLeadsButton: string;
    searchFormToggleShowTooltip: string;
    searchFormToggleHideTooltip: string;

    // --- Leads List / Grid Section ---
    leadsListTitle: string;
    refreshButton: string;
    loadingLeads: string;
    noNewLeadsYet: string;
    noSavedLeads: string;
    noArchivedLeads: string;
    noLeadsFound: string;

    // --- Table Columns ---
    colName: string;
    colJobTitle: string;
    colIndustry: string;
    colLocation: string;
    colCompanyName: string;
    colCompanySize: string;
    colPhone: string;
    colLinkedIn: string;
    colKeywords: string;
    colEmail: string;
    colNotes: string;
    colCreatedAt: string;
    colStatus: string;
    colActions: string;

    // --- Table Actions (Single & Batch) ---
    actionSaveTooltip: string;         // Descriptive: "Save Lead"
    actionArchiveTooltip: string;      // Descriptive: "Archive Lead"
    actionRestoreTooltip: string;      // Descriptive: "Move to New"
    actionDeleteTooltip: string;       // Descriptive: "Delete Lead"
    actionMoveToSavedTooltip: string;  // Descriptive: "Move to Saved"

    // ---- NEW SIMPLE TOOLTIPS for hover ----
    tooltipSave: string;               // Simple: "Save"
    tooltipArchive: string;            // Simple: "Archive"
    tooltipRestore: string;            // Simple: "Restore"
    tooltipMoveToSaved: string;        // Simple: "Move to Saved"
    tooltipDelete: string;             // Simple: "Delete"
    // ---- END OF NEW SIMPLE TOOLTIPS ----

    selectAllPageButton: string;
    selectAllPageTooltip: string;
    deselectAllButton: string;
    deselectAllPageTooltip: string;
    batchActionsDropdownTitle: string;
    batchSaveButton: string;
    batchArchiveButton: string;
    batchRestoreButton: string;
    batchDeleteButton: string;
    batchMoveToSavedButton: string; // Key for "Move Selected to Saved" button text

    // --- Pagination ---
    previousPage: string;
    nextPage: string;
    pageText: string;
    ofText: string;
    showNum: string;

    // --- Feedback, Alerts & Confirmation Messages ---
    alertError: string;
    alertSuccess: string;
    alertWarning: string;
    errorRequired: (fieldName: string) => string;
    noSearchCriteria: string;
    userNotAuthMessage: string;
    n8nConfigError: string;
    accessDeniedMessage: string;
    confirmArchiveUnsaved: string;
    unsavedLeadsArchived: string;
    searchLeadsSuccess: string;
    leadSavedSuccess: string;
    leadArchivedSuccess: string;
    leadRestoredSuccess: string;
    leadDeletedSuccess: string;
    leadUpdateError: string;
    leadDeleteError: string;
    autoArchiveError: string;
    confirmBatchSave: (count: number) => string;
    confirmBatchArchive: (count: number) => string;
    confirmBatchRestore: (count: number) => string;
    confirmBatchDelete: (count: number) => string;
    confirmBatchMoveToSaved: (count: number) => string; // Key for "Move Selected to Saved" confirmation
    noLeadsEligibleForAction: (action: string) => string;
    batchActionResult: (action: string, success: number, failed: number) => string;

    // --- Fields for potential future use ---
    formTitle?: string;
    searchSectionTitle?: string;
    leadIcebreakerColumn?: string;
    sendIcebreakerTooltip?: string;
    viewDetailsTooltip?: string;
    contactNameLabel?: string;
    companyNameLabel?: string;
    emailLabel?: string;
    phoneLabel?: string;
    statusLabel?: string;
    selectStatusPlaceholder?: string;
    statusNew?: string; // For lead status display text, e.g., "New Prospect"
    statusContacted?: string;
    statusFollowUp?: string;
    statusClosed?: string;
    statusNewProspect?: string; // For filter options, if different from statusNew
    statusReplied?: string;     // For filter options
    customNotesLabel?: string;
    errorMinLength?: (fieldName: string, min: number) => string;
    contactOrCompanyRequiredError?: string;
}

// ... (industriesData remains the same) ...
export const industriesData: Industry[] = [
    { value: "information technology & services", zh: "資訊科技與服務", en: "Information Technology & Services" },
    { value: "construction", zh: "建築業", en: "Construction" },
    { value: "marketing & advertising", zh: "行銷與廣告", en: "Marketing & Advertising" },
    { value: "real estate", zh: "房地產", en: "Real Estate" },
    { value: "health, wellness & fitness", zh: "健康、養生與健身", en: "Health, Wellness & Fitness" },
    { value: "management consulting", zh: "管理顧問", en: "Management Consulting" },
    { value: "computer software", zh: "電腦軟體", en: "Computer Software" },
    { value: "internet", zh: "網際網路", en: "Internet" },
    { value: "retail", zh: "零售業", en: "Retail" },
    { value: "financial services", zh: "金融服務", en: "Financial Services" },
    { value: "consumer services", zh: "消費者服務", en: "Consumer Services" },
    { value: "hospital & health care", zh: "醫療與健康照護", en: "Hospital & Health Care" },
    { value: "automotive", zh: "汽車產業", en: "Automotive" },
    { value: "restaurants", zh: "餐飲業", en: "Restaurants" },
    { value: "education management", zh: "教育管理", en: "Education Management" },
    { value: "food & beverages", zh: "食品與飲料", en: "Food & Beverages" },
    { value: "design", zh: "設計", en: "Design" },
    { value: "hospitality", zh: "旅宿與款待業", en: "Hospitality" },
    { value: "accounting", zh: "會計", en: "Accounting" },
    { value: "events services", zh: "活動服務", en: "Events Services" },
    { value: "luxury goods & jewelry", zh: "奢侈品與珠寶", en: "Luxury Goods & Jewelry" },
    { value: "logistics & supply chain", zh: "物流與供應鏈", en: "Logistics & Supply Chain" },
    { value: "warehousing", zh: "倉儲", en: "Warehousing" },
    { value: "package/freight delivery", zh: "包裹/貨運配送", en: "Package/Freight Delivery" }
];


export interface LeadStatusOption {
    value: string;
    textKey: 'statusNewProspect' | 'statusContacted' | 'statusFollowUp' | 'statusReplied';
}


// UI Texts for each language
export const uiTexts: Record<LanguageCode, Translations> = {
    zh: {
        dashboardTitle: '潛在客戶儀表板',
        formDescription: '定義您的潛在客戶輪廓',
        filtersTitle: '篩選條件',
        tabsTitle: '潛在客戶類別',
        tabNew: '新獲取',
        tabSaved: '已儲存',
        tabArchived: '已封存',
        addFilterPlaceholder: '新增',
        selectFilterPlaceholder: '請選擇',
        clearAllFiltersButton: '清除所有篩選',
        clearFilterSectionTooltip: '清除此區篩選',
        mainQueryLabel: '描述您想找的潛在客戶類型：',
        mainQueryPlaceholder: '例如：倫敦金融科技新創公司的軟體工程師',
        advancedBtnTextShow: '進階篩選',
        advancedBtnTextHide: '隱藏進階篩選',
        jobTitleLabel: '職稱',
        industryLabel: '產業別',
        industryPlaceholder: '請選擇產業',
        locationLabel: '國家/城市',
        companySizeLabel: '公司規模',
        companySizePlaceholder: '請選擇公司規模',
        keywordsLabel: '其他關鍵字',
        advKeywordsPlaceholder: '例如：創新, 人工智慧, B2B (以逗號分隔)',
        addFiltersBtnText: '加入條件標籤',
        tagAreaLabel: '已選條件：',
        removeFilterTooltip: '移除此條件',
        searchLeadsButton: '尋找潛在客戶',
        searchFormToggleShowTooltip: '顯示搜尋表單',
        searchFormToggleHideTooltip: '隱藏搜尋表單',
        leadsListTitle: '潛在客戶列表',
        refreshButton: '重新整理',
        loadingLeads: '載入中...',
        noNewLeadsYet: '開始搜尋以發掘新的潛在客戶，或查看其他分類。',
        noSavedLeads: '尚無已儲存的潛在客戶。您可以從「新獲取」分類中儲存客戶。',
        noArchivedLeads: '尚無已封存的潛在客戶。',
        noLeadsFound: '找不到符合條件的潛在客戶。',
        colName: '姓名',
        colJobTitle: '職稱',
        colIndustry: '產業別',
        colLocation: '地點',
        colCompanyName: '公司名稱',
        colCompanySize: '公司規模',
        colPhone: '電話',
        colLinkedIn: 'LinkedIn',
        colKeywords: '關鍵字',
        colEmail: '電子郵件',
        colNotes: '備註',
        colCreatedAt: '加入日期',
        colStatus: '狀態',
        colActions: '操作',
        actionSaveTooltip: '儲存此潛在客戶',
        actionArchiveTooltip: '封存此潛在客戶',
        actionRestoreTooltip: '移至新獲取',
        actionDeleteTooltip: '刪除此潛在客戶',
        actionMoveToSavedTooltip: '移至已儲存',
        tooltipSave: '儲存',
        tooltipArchive: '封存',
        tooltipRestore: '還原',
        tooltipMoveToSaved: '移至已儲存',
        tooltipDelete: '刪除',
        selectAllPageButton: '全選本頁',
        selectAllPageTooltip: '全選本頁所有潛在客戶',
        deselectAllButton: '取消全選',
        deselectAllPageTooltip: '取消選取本頁所有潛在客戶',
        batchActionsDropdownTitle: '批次操作',
        batchSaveButton: '儲存選取項目',
        batchArchiveButton: '封存選取項目',
        batchRestoreButton: '還原選取項目至新獲取',
        batchDeleteButton: '刪除選取項目',
        batchMoveToSavedButton: '移動選取項目至已儲存',
        previousPage: "上一頁",
        nextPage: "下一頁",
        pageText: "第",
        ofText: "頁，共",
        showNum: "每頁顯示",
        alertError: "錯誤：",
        alertSuccess: "成功：",
        alertWarning: "提醒：",
        errorRequired: (fieldName: string) => `「${fieldName}」為必填欄位。`,
        noSearchCriteria: "請輸入搜尋條件。",
        userNotAuthMessage: '使用者未驗證，請重新登入。',
        n8nConfigError: '系統整合設定錯誤，請聯絡管理員。',
        accessDeniedMessage: '存取被拒，請重新登入或確認您的權限。',
        confirmArchiveUnsaved: '您有未儲存的「新獲取」潛在客戶。開始新的搜尋將會封存這些客戶，確定要繼續嗎？',
        unsavedLeadsArchived: '未儲存的「新獲取」潛在客戶已移至「已封存」。',
        searchLeadsSuccess: '搜尋請求已送出，結果將顯示於「新獲取」分頁。',
        leadSavedSuccess: '潛在客戶已成功儲存。',
        leadArchivedSuccess: '潛在客戶已成功封存。',
        leadRestoredSuccess: '潛在客戶已成功移至「新獲取」。',
        leadDeletedSuccess: '潛在客戶已成功刪除。',
        leadUpdateError: '更新潛在客戶狀態失敗。',
        leadDeleteError: '刪除潛在客戶失敗。',
        autoArchiveError: '自動封存未儲存潛在客戶失敗。',
        confirmBatchSave: (count: number) => `確定要儲存 ${count} 個選取的潛在客戶嗎？`,
        confirmBatchArchive: (count: number) => `確定要封存 ${count} 個選取的潛在客戶嗎？`,
        confirmBatchRestore: (count: number) => `確定要將 ${count} 個選取的潛在客戶還原至「新獲取」嗎？`,
        confirmBatchDelete: (count: number) => `確定要永久刪除 ${count} 個選取的潛在客戶嗎？此操作無法復原。`,
        confirmBatchMoveToSaved: (count: number) => `確定要將 ${count} 個選取的潛在客戶移至「已儲存」嗎？`,
        noLeadsEligibleForAction: (action: string) => `沒有選取的潛在客戶符合「${action}」操作的條件。`,
        batchActionResult: (action: string, success: number, failed: number) => `${action}：${success} 個成功，${failed} 個失敗。`,
        formTitle: '潛在客戶發掘中心',
        statusNew: '新開發',
        statusContacted: '已聯繫',
        statusFollowUp: '追蹤中',
        statusClosed: '已結案',
        statusNewProspect: '新開發客戶',
        statusReplied: '已回覆',
    },
    en: {
        dashboardTitle: 'Prospects Dashboard',
        formDescription: 'Define Your Prospect Persona',
        filtersTitle: 'Filters',
        tabsTitle: 'Lead Categories',
        tabNew: 'New',
        tabSaved: 'Saved',
        tabArchived: 'Archived',
        addFilterPlaceholder: 'Add',
        selectFilterPlaceholder: 'Select',
        clearAllFiltersButton: 'Clear All Filters',
        clearFilterSectionTooltip: 'Clear section',
        mainQueryLabel: "Briefly describe the type of prospects you're looking for:",
        mainQueryPlaceholder: "e.g., 'Software engineers in fintech startups in London'",
        advancedBtnTextShow: "Advanced Filters",
        advancedBtnTextHide: "Hide Advanced Filters",
        jobTitleLabel: "Job Title",
        industryLabel: "Industry",
        industryPlaceholder: "Select Industry",
        locationLabel: "Country/City",
        companySizeLabel: "Company Size",
        companySizePlaceholder: "Select Company Size",
        keywordsLabel: "Other Keywords",
        advKeywordsPlaceholder: "e.g., innovative, AI, B2B (comma-separated)",
        addFiltersBtnText: "Add Filter Tags",
        tagAreaLabel: "Selected Filters:",
        removeFilterTooltip: "Remove this filter",
        searchLeadsButton: "Find Prospects",
        searchFormToggleShowTooltip: "Show Search Form",
        searchFormToggleHideTooltip: "Hide Search Form",
        leadsListTitle: "Prospects",
        refreshButton: "Refresh",
        loadingLeads: "Loading...",
        noNewLeadsYet: "Submit a search to find new prospects or check other tabs.",
        noSavedLeads: "No leads saved yet. Save leads from the 'New' tab.",
        noArchivedLeads: "No leads have been archived.",
        noLeadsFound: "No prospects found for this tab.",
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
        selectAllPageButton: "Select Page",
        selectAllPageTooltip: "Select all leads on current page",
        deselectAllButton: "Deselect All",
        deselectAllPageTooltip: "Deselect all leads on current page",
        batchActionsDropdownTitle: "Actions for Selected",
        batchSaveButton: "Save Selected",
        batchArchiveButton: "Archive Selected",
        batchRestoreButton: "Restore Selected to New",
        batchDeleteButton: "Delete Selected",
        batchMoveToSavedButton: "Move Selected to Saved",
        previousPage: "Previous",
        nextPage: "Next",
        pageText: "Page",
        ofText: "of",
        showNum: "Show",
        alertError: "Error: ",
        alertSuccess: "Success: ",
        alertWarning: "Warning: ",
        errorRequired: (fieldName: string) => `${fieldName} is required.`,
        noSearchCriteria: "Please enter search criteria.",
        userNotAuthMessage: 'User not authenticated. Please log in.',
        n8nConfigError: 'N8N configuration error. Contact admin.',
        accessDeniedMessage: 'Access Denied.',
        confirmArchiveUnsaved: "You have unsaved leads. Starting a new search will archive them. Proceed?",
        unsavedLeadsArchived: "Unsaved leads moved to 'Archived'.",
        searchLeadsSuccess: "Search submitted successfully. Results are in the 'New' tab.",
        leadSavedSuccess: "Lead saved successfully.",
        leadArchivedSuccess: "Lead archived successfully.",
        leadRestoredSuccess: "Lead moved to 'New' successfully.",
        leadDeletedSuccess: "Lead deleted successfully.",
        leadUpdateError: "Failed to update lead status.",
        leadDeleteError: "Failed to delete lead.",
        autoArchiveError: "Failed to auto-archive unsaved leads.",
        confirmBatchSave: (count: number) => `Are you sure you want to save ${count} selected lead(s)?`,
        confirmBatchArchive: (count: number) => `Are you sure you want to archive ${count} selected lead(s)?`,
        confirmBatchRestore: (count: number) => `Are you sure you want to restore ${count} selected lead(s) to 'New'?`,
        confirmBatchDelete: (count: number) => `Are you sure you want to permanently delete ${count} selected lead(s)? This action cannot be undone.`,
        confirmBatchMoveToSaved: (count: number) => `Are you sure you want to move ${count} selected lead(s) to 'Saved'?`,
        noLeadsEligibleForAction: (action: string) => `No selected leads are eligible for ${action}.`,
        batchActionResult: (action: string, success: number, failed: number) => `${action}: ${success} succeeded, ${failed} failed.`,
        formTitle: 'Lead Prospecting Center',
        statusNew: 'New', // This is for display of the status, distinct from the filter option.
        statusContacted: 'Contacted',
        statusFollowUp: 'Follow-up',
        statusClosed: 'Closed',
        statusNewProspect: 'New Prospect', // This is for the filter panel's select options
        statusReplied: 'Replied',     // This is for the filter panel's select options
    }
};