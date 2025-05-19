export interface FilterTag {
    id: string;
    type: 'jobTitle' | 'industry' | 'location' | 'companySize' | 'keywords' | 'custom';
    value: string;
    displayValue: string;
    label: string;
}
export interface LeadDataForSupabase {
    user_id?: string;
    baserow_row_id?: string | null;
    contact_name?: string | null;
    company_name?: string | null;
    email?: string | null;
    phone?: string | null;
    status?: string | null;
    notes?: string | null;
    job_title?: string | null;
    industry?: string | null;
    location?: string | null;
    company_size?: string | null;
    source_keywords?: string[] | null;
}
export interface ProspectFormState {
    mainQuery: string;
    jobTitle: string;
    industry: string;
    location: string;
    companySize: string;
    keywords: string;
    baserowRowId?: string;
    contactName?: string;
    companyName?: string;
    email?: string;
    phone?: string;
    status?: string;
    customNotes?: string;
}
