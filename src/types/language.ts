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
    formDescription: string; // Used in LeadGenFormView and EngagementCenterView

    // --- App Navigation Sidebar ---
    sidebarLeadSearchLink: string;
    sidebarLeadSearchTitle: string;
    sidebarEngagementLink: string;
    sidebarEngagementTitle: string;
    sidebarSettingsLink: string;
    sidebarSettingsTitle: string;
    languageDropdownHeader: string;
    themeDropdownHeader: string;
    userActionsDropdownTitle: string;
    userSettingsPageLink: string;
    signOutButton: string;

    // --- Filter Panel Sidebar (shared by LeadGenFormView) ---
    filtersTitle: string;
    tabsTitle: string;
    tabNew: string;
    tabSaved: string;
    tabArchived: string;
    addFilterPlaceholder: string;
    selectFilterPlaceholder: string;
    clearAllFiltersButton: string;
    clearFilterSectionTooltip: string;

    // --- Search Criteria Section (Main Form - LeadGenFormView) ---
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

    // --- Leads List / Grid Section (LeadGenFormView) ---
    leadsListTitle: string;
    refreshButton: string;
    loadingLeads: string; // General loading text for leads
    noNewLeadsYet: string;
    noSavedLeads: string;
    noArchivedLeads: string;
    noLeadsFound: string; // General "no results" for leads list

    // --- Table Columns (Shared by LeadGenFormView & EngagementCenterView potentially) ---
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

    // --- Table Actions (Single & Batch - LeadGenFormView) ---
    actionSaveTooltip: string;
    actionArchiveTooltip: string;
    actionRestoreTooltip: string;
    actionDeleteTooltip: string;
    actionMoveToSavedTooltip: string;
    tooltipSave: string;
    tooltipArchive: string;
    tooltipRestore: string;
    tooltipMoveToSaved: string;
    tooltipDelete: string;
    selectAllPageButton: string;
    selectAllPageTooltip: string;
    deselectAllButton: string;
    deselectAllPageTooltip: string;
    batchActionsDropdownTitle: string;
    batchSaveButton: string;
    batchArchiveButton: string;
    batchRestoreButton: string;
    batchDeleteButton: string;
    batchMoveToSavedButton: string;
    showLessButton: string;
    showMoreButtonText: (count: number) => string; // Function type for dynamic text

    // --- Pagination (Shared) ---
    previousPage: string;
    nextPage: string;
    pageText: string;
    ofText: string;
    showNum: string;

    // --- Feedback, Alerts & Confirmation Messages (Shared) ---
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
    confirmBatchMoveToSaved: (count: number) => string;
    noLeadsEligibleForAction: (action: string) => string;
    batchActionResult: (action: string, success: number, failed: number) => string;

    // --- Engagement Center View Specific ---
    engagementCenterTitle: string;
    searchLeadsPlaceholder: string; // Search within the hub
    filterByStatusAll: string;
    filterStatusPendingIcebreaker: string;
    filterStatusIcebreakerSent: string;
    filterStatusReplied: string; // Could be distinct from lead_status 'Replied' for engagement
    filterStatusFollowUpDue: string;
    loading: string; // General loading text, e.g., for the hub itself
    noLeadsInHub: string;
    addLeadsFromProspects: string;
    followUpOn: string;
    selectLeadPrompt: string;
    viewLinkedIn: string;
    removeFromHub: string;
    icebreakerSectionTitle: string;
    craftIcebreakerPlaceholder: string;
    getAISuggestion: string;
    sendIcebreakerButton: string;
    sentOn: string;
    activityAndFollowUpsTitle: string;
    logOrSchedule: string;
    logEmailReply: string;
    logCall: string;
    logMeeting: string;
    scheduleFollowUpEmail: string;
    scheduleFollowUpCall: string;
    notesPlaceholder: string; // General notes placeholder in engagement
    addActivityButton: string;
    historyLog: string;
    followUpDue: string; // e.g., "Follow-up Due:" (for an activity item)
    noActivityYet: string;
    generalNotesTitle: string;
    addNotesPlaceholder: string; // Placeholder for general notes in engagement
    saveNotesButton: string;
    statusNotSent: string; // For icebreaker status display
    statusSent: string;
    statusOpened: string;
    statusRepliedEngagement: string; // Specific for engagement reply status if needed
    statusBounced: string;
    statusError: string; // General error status display for icebreaker

    // --- Login/Signup Page Specific & Shared Form Fields ---
    productName?: string;
    landingHeadline?: string;
    landingSubheadline?: string;
    landingFeaturesTitle?: string;
    landingFeature1Title?: string;
    landingFeature1Desc?: string;
    landingFeature2Title?: string;
    landingFeature2Desc?: string;
    landingFeature3Title?: string;
    landingFeature3Desc?: string;
    landingFeature4Title?: string;
    landingFeature4Desc?: string;
    signUpNowButton?: string;
    loginTitle?: string;
    emailLabel?: string; // Shared for login, signup, etc.
    passwordLabel?: string;
    loginButton?: string;
    signInWithGoogleButton?: string;
    signInWithLinkedInButton?: string; // NEW
    orDivider?: string;
    noAccountPrompt?: string;
    signUpLink?: string;
    emailPlaceholder?: string; // Shared
    passwordPlaceholder?: string;
    loginErrorDefault?: string;

    // --- Other/Future Use ---
    formTitle?: string;
    searchSectionTitle?: string;
    leadIcebreakerColumn?: string;
    sendIcebreakerTooltip?: string;
    viewDetailsTooltip?: string;
    contactNameLabel?: string;
    companyNameLabel?: string;
    // phoneLabel?: string; // Covered by colPhone if same
    statusLabel?: string;
    selectStatusPlaceholder?: string;
    statusNew?: string; // Display text for lead status "New"
    statusContacted?: string;
    statusFollowUp?: string;
    statusClosed?: string;
    statusNewProspect?: string; // Filter option text for "New Prospect"
    statusReplied?: string;     // Filter option text for "Replied"
    customNotesLabel?: string;
    errorMinLength?: (fieldName: string, min: number) => string;
    contactOrCompanyRequiredError?: string;
}

export const industriesData: Industry[] = [
    { value: "information technology", zh: "資訊科技與服務", en: "Information Technology" },
    { value: "construction", zh: "建築業", en: "Construction" },
    { value: "marketing & advertising", zh: "行銷與廣告", en: "Marketing & Advertising" },
    { value: "real estate", zh: "房地產", en: "Real Estate" },
    { value: "health, wellness & fitness", zh: "健康、養生與健身", en: "Health, Wellness & Fitness" },
    { value: "pharmaceuticals", zh: "製藥業", en: "pharmaceuticals" },
    { value: "biotechnology", zh: "生物科技", en: "biotechnology" },
    { value: "management consulting", zh: "管理顧問", en: "Management Consulting" },
    { value: "computer software", zh: "電腦軟體", en: "Computer Software" },
    { value: "internet", zh: "網際網路", en: "Internet" },
    { value: "semiconductors", zh: "半導體", en: "semiconductors" },
    { value: "retail", zh: "零售業", en: "Retail" },
    { value: "financial services", zh: "金融服務", en: "Financial Services" },
    { value: "consumer services", zh: "消費者服務", en: "Consumer Services" },
    { value: "hospital & health care", zh: "醫療與健康照護", en: "Hospital & Health Care" },
    { value: "automotive", zh: "汽車產業", en: "Automotive" },
    { value: "restaurants", zh: "餐飲業", en: "Restaurants" },
    { value: "education management", zh: "教育管理", en: "Education Management" },
    { value: "food & beverages", zh: "食品與飲料", en: "Food & Beverages" },
    { value: "design", zh: "設計", en: "Design" },
    { value: "apparel & fashion", zh: "服飾與時尚", en: "apparel & fashion" },
    { value: "import & export", zh: "進出口", en: "import & export" },
    { value: "hospitality", zh: "旅宿與款待業", en: "Hospitality" },
    { value: "accounting", zh: "會計", en: "Accounting" },
    { value: "events services", zh: "活動服務", en: "Events Services" },
    { value: "luxury goods & jewelry", zh: "奢侈品與珠寶", en: "Luxury Goods & Jewelry" },
    { value: "cosmetics", zh: "美妝", en: "cosmetics" },
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
        // --- Existing Chinese translations from your file ---
        dashboardTitle: '潛在客戶搜尋儀表板',
        formDescription: '定義您的潛在客戶搜尋輪廓',
        filtersTitle: '篩選條件',
        tabsTitle: '潛在客戶搜尋類別',
        tabNew: '新獲取',
        tabSaved: '已儲存',
        tabArchived: '已封存',
        addFilterPlaceholder: '新增',
        selectFilterPlaceholder: '請選擇',
        clearAllFiltersButton: '清除所有篩選',
        clearFilterSectionTooltip: '清除此區篩選',
        mainQueryLabel: '描述您想找的潛在客戶搜尋類型：',
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
        searchLeadsButton: '尋找潛在客戶搜尋',
        searchFormToggleShowTooltip: '顯示搜尋表單',
        searchFormToggleHideTooltip: '隱藏搜尋表單',
        leadsListTitle: '潛在客戶搜尋列表',
        refreshButton: '重新整理',
        loadingLeads: '載入中...',
        noNewLeadsYet: '開始搜尋以發掘新的潛在客戶搜尋，或查看其他分類。',
        noSavedLeads: '尚無已儲存的潛在客戶搜尋。您可以從「新獲取」分類中儲存客戶。',
        noArchivedLeads: '尚無已封存的潛在客戶搜尋。',
        noLeadsFound: '找不到符合條件的潛在客戶搜尋。',
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
        actionSaveTooltip: '儲存此潛在客戶搜尋',
        actionArchiveTooltip: '封存此潛在客戶搜尋',
        actionRestoreTooltip: '移至新獲取',
        actionDeleteTooltip: '刪除此潛在客戶搜尋',
        actionMoveToSavedTooltip: '移至已儲存',
        tooltipSave: '儲存',
        tooltipArchive: '封存',
        tooltipRestore: '還原',
        tooltipMoveToSaved: '移至已儲存',
        tooltipDelete: '刪除',
        selectAllPageButton: '全選本頁',
        selectAllPageTooltip: '全選本頁所有潛在客戶搜尋',
        deselectAllButton: '取消全選',
        deselectAllPageTooltip: '取消選取本頁所有潛在客戶搜尋',
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
        confirmArchiveUnsaved: '您有未儲存的「新獲取」潛在客戶搜尋。開始新的搜尋將會封存這些客戶，確定要繼續嗎？',
        unsavedLeadsArchived: '未儲存的「新獲取」潛在客戶搜尋已移至「已封存」。',
        searchLeadsSuccess: '搜尋請求已送出，結果將顯示於「新獲取」分頁。',
        leadSavedSuccess: '潛在客戶搜尋已成功儲存。',
        leadArchivedSuccess: '潛在客戶搜尋已成功封存。',
        leadRestoredSuccess: '潛在客戶搜尋已成功移至「新獲取」。',
        leadDeletedSuccess: '潛在客戶搜尋已成功刪除。',
        leadUpdateError: '更新潛在客戶搜尋狀態失敗。',
        leadDeleteError: '刪除潛在客戶搜尋失敗。',
        autoArchiveError: '自動封存未儲存潛在客戶搜尋失敗。',
        confirmBatchSave: (count: number) => `確定要儲存 ${count} 個選取的潛在客戶搜尋嗎？`,
        confirmBatchArchive: (count: number) => `確定要封存 ${count} 個選取的潛在客戶搜尋嗎？`,
        confirmBatchRestore: (count: number) => `確定要將 ${count} 個選取的潛在客戶搜尋還原至「新獲取」嗎？`,
        confirmBatchDelete: (count: number) => `確定要永久刪除 ${count} 個選取的潛在客戶搜尋嗎？此操作無法復原。`,
        confirmBatchMoveToSaved: (count: number) => `確定要將 ${count} 個選取的潛在客戶搜尋移至「已儲存」嗎？`,
        noLeadsEligibleForAction: (action: string) => `沒有選取的潛在客戶搜尋符合「${action}」操作的條件。`,
        batchActionResult: (action: string, success: number, failed: number) => `${action}：${success} 個成功，${failed} 個失敗。`,
        formTitle: '潛在客戶搜尋發掘中心',
        statusNew: '新開發',
        statusContacted: '已聯繫',
        statusFollowUp: '追蹤中',
        statusClosed: '已結案',
        statusNewProspect: '新開發客戶',
        statusReplied: '已回覆',
        // --- Sidebar ---
        sidebarLeadSearchLink: '潛在客戶搜尋',
        sidebarLeadSearchTitle: '潛在客戶搜尋搜尋',
        sidebarEngagementLink: '客戶拓展中心',
        sidebarEngagementTitle: '客戶拓展中心',
        sidebarSettingsLink: '設定',
        sidebarSettingsTitle: '設定',
        languageDropdownHeader: '語言',
        themeDropdownHeader: '主題',
        userActionsDropdownTitle: '使用者操作',
        userSettingsPageLink: '使用者設定',
        signOutButton: '登出',
        // --- Engagement Center ---
        engagementCenterTitle: '客戶拓展中心',
        searchLeadsPlaceholder: '搜尋客戶拓展中心內的潛在客戶搜尋...',
        filterByStatusAll: '所有狀態',
        filterStatusPendingIcebreaker: '待傳送破冰訊息',
        filterStatusIcebreakerSent: '已傳送破冰訊息',
        filterStatusReplied: '已回覆 (互動)',
        filterStatusFollowUpDue: '待追蹤',
        loading: '載入中...',
        noLeadsInHub: '客戶拓展中心內無符合條件的潛在客戶搜尋。',
        addLeadsFromProspects: '請從「潛在客戶搜尋」視圖新增客戶。',
        followUpOn: '追蹤於：',
        selectLeadPrompt: '請從左側列表中選取潛在客戶搜尋以開始管理。',
        viewLinkedIn: '查看 LinkedIn',
        removeFromHub: '從客戶拓展中心移除',
        icebreakerSectionTitle: '破冰訊息',
        craftIcebreakerPlaceholder: '在此撰寫您的個人化破冰訊息...',
        getAISuggestion: 'AI 建議',
        sendIcebreakerButton: '傳送破冰訊息',
        sentOn: '傳送於：',
        activityAndFollowUpsTitle: '活動與追蹤',
        logOrSchedule: '記錄互動 / 安排追蹤',
        logEmailReply: '記錄郵件回覆',
        logCall: '記錄通話',
        logMeeting: '記錄會議',
        scheduleFollowUpEmail: '安排郵件追蹤',
        scheduleFollowUpCall: '安排通話追蹤',
        notesPlaceholder: '備註...',
        addActivityButton: '新增活動',
        historyLog: '歷史記錄：',
        followUpDue: '待追蹤：',
        noActivityYet: '尚無活動記錄。',
        generalNotesTitle: '一般備註',
        addNotesPlaceholder: '新增關於互動的特定備註...',
        saveNotesButton: '儲存備註',
        statusNotSent: '待傳送',
        statusSent: '已傳送',
        statusOpened: '已開啟',
        statusRepliedEngagement: '已回覆',
        statusBounced: '退回',
        statusError: '錯誤',
        // --- Login/Signup ---
        productName: 'Prospec',
        landingHeadline: '用 AI 強化您的業務拓展',
        landingSubheadline: '以前所未有的方式發現、篩選並與潛在客戶搜尋互動。Prospec 使用頂尖 AI 技術找到您的理想客戶並個性化溝通，為您節省時間、提高轉換率。',
        landingFeaturesTitle: '為何選擇 Prospec？',
        landingFeature1Title: 'AI 驅動潛客開發：',
        landingFeature1Desc: '發掘隱藏的潛力客戶和高意向線索。',
        landingFeature2Title: '智能資格篩選：',
        landingFeature2Desc: '透過智能評分，專注於真正重要的潛在客戶搜尋。',
        landingFeature3Title: '個性化互動：',
        landingFeature3Desc: '打造引人入勝且能引起共鳴的溝通內容。',
        landingFeature4Title: '提升轉換率：',
        landingFeature4Desc: '將更多潛在客戶搜尋轉化為忠實顧客。',
        signUpNowButton: '免費開始',
        loginTitle: '歡迎回來！',
        emailLabel: '電子郵件地址',
        passwordLabel: '密碼',
        loginButton: '登入',
        signInWithGoogleButton: '使用 Google 帳戶登入',
        signInWithLinkedInButton: '使用 LinkedIn 帳戶登入',
        orDivider: '或',
        noAccountPrompt: '還沒有帳戶？',
        signUpLink: '在此註冊',
        emailPlaceholder: 'you@example.com',
        passwordPlaceholder: '輸入您的密碼',
        loginErrorDefault: '登入時發生未知錯誤。',
        showLessButton: '顯示較少',
        showMoreButtonText: (count: number) => `還有 (${count} 個)`,
    },
    en: {
        // --- Existing English translations from your file ---
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
        keywordsLabel: "Company Keywords",
        advKeywordsPlaceholder: "e.g., Google, Walmart, AWS (comma-separated)",
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
        statusNew: 'New',
        statusContacted: 'Contacted',
        statusFollowUp: 'Follow-up',
        statusClosed: 'Closed',
        statusNewProspect: 'New Prospect',
        statusReplied: 'Replied',
        // --- Sidebar ---
        sidebarLeadSearchLink: 'Lead Search',
        sidebarLeadSearchTitle: 'Lead Search',
        sidebarEngagementLink: 'Engagement Hub',
        sidebarEngagementTitle: 'Engagement Hub',
        sidebarSettingsLink: 'Settings',
        sidebarSettingsTitle: 'Settings',
        languageDropdownHeader: 'Language',
        themeDropdownHeader: 'Theme',
        userActionsDropdownTitle: 'User Actions',
        userSettingsPageLink: 'User Settings',
        signOutButton: 'Sign Out',
        // --- Engagement Center ---
        engagementCenterTitle: 'Engagement Hub',
        searchLeadsPlaceholder: 'Search leads in hub...',
        filterByStatusAll: 'All Statuses',
        filterStatusPendingIcebreaker: 'Pending Icebreaker',
        filterStatusIcebreakerSent: 'Icebreaker Sent',
        filterStatusReplied: 'Replied', // Engagement context
        filterStatusFollowUpDue: 'Follow-up Due',
        loading: 'Loading...',
        noLeadsInHub: 'No leads in the hub matching your criteria.',
        addLeadsFromProspects: 'Add leads from the Prospects view.',
        followUpOn: 'Follow-up:',
        selectLeadPrompt: 'Select a lead from the list to start managing engagement.',
        viewLinkedIn: 'View LinkedIn',
        removeFromHub: 'Remove from Hub',
        icebreakerSectionTitle: 'Icebreaker Message',
        craftIcebreakerPlaceholder: 'Craft your personalized icebreaker here...',
        getAISuggestion: 'AI Suggestion',
        sendIcebreakerButton: 'Send Icebreaker',
        sentOn: 'Sent:',
        activityAndFollowUpsTitle: 'Activity & Follow-ups',
        logOrSchedule: 'Log Interaction / Schedule Follow-up',
        logEmailReply: 'Log Email Reply',
        logCall: 'Log Call',
        logMeeting: 'Log Meeting',
        scheduleFollowUpEmail: 'Schedule Follow-up Email',
        scheduleFollowUpCall: 'Schedule Follow-up Call',
        notesPlaceholder: 'Notes...',
        addActivityButton: 'Add Activity',
        historyLog: 'History:',
        followUpDue: 'Follow-up Due:',
        noActivityYet: 'No activity logged yet.',
        generalNotesTitle: 'General Notes',
        addNotesPlaceholder: 'Add notes specific to your engagement...',
        saveNotesButton: 'Save Notes',
        statusNotSent: 'To Send',
        statusSent: 'Sent',
        statusOpened: 'Opened',
        statusRepliedEngagement: 'Replied', // Engagement context
        statusBounced: 'Bounced',
        statusError: 'Error',
        // --- Login/Signup ---
        productName: 'Prospec',
        landingHeadline: 'Supercharge Your Outreach with AI',
        landingSubheadline: 'Discover, qualify, and engage prospects like never before. Prospec uses cutting-edge AI to find your ideal customers and personalize communication, saving you time and boosting conversions.',
        landingFeaturesTitle: 'Why Choose Prospec?',
        landingFeature1Title: 'AI-Powered Prospecting:',
        landingFeature1Desc: 'Uncover hidden gems and high-intent leads.',
        landingFeature2Title: 'Intelligent Qualification:',
        landingFeature2Desc: 'Focus on leads that matter with smart scoring.',
        landingFeature3Title: 'Personalized Engagement:',
        landingFeature3Desc: 'Craft compelling outreach that resonates.',
        landingFeature4Title: 'Boost Conversions:',
        landingFeature4Desc: 'Turn more prospects into loyal customers.',
        signUpNowButton: 'Get Started Free',
        loginTitle: 'Welcome Back!',
        emailLabel: 'Email Address',
        passwordLabel: 'Password',
        loginButton: 'Log In',
        signInWithGoogleButton: 'Sign in with Google',
        signInWithLinkedInButton: 'Sign in with LinkedIn',
        orDivider: 'OR',
        noAccountPrompt: "Don't have an account?",
        signUpLink: 'Sign up here',
        emailPlaceholder: 'you@example.com',
        passwordPlaceholder: 'Enter your password',
        loginErrorDefault: 'An error occurred during login.',
        showLessButton: 'Show less',
        showMoreButtonText: (count: number) => `... (${count} more)`,
    }
};