import type { PropType } from 'vue';
import type { LeadTab } from '@/types/tabs';
export interface TabCounts {
    new: number;
    saved: number;
    archived: number;
}
export type FilterKey = 'job_title' | 'industry' | 'location' | 'company_name' | 'company_size' | 'keywords' | 'lead_status';
export interface ClientFilterItem {
    key: FilterKey;
    label: string;
    type: 'text' | 'select' | 'keywords';
    options?: {
        value: string;
        text: string;
    }[];
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
declare const _default: import("vue").DefineComponent<import("vue").ExtractPropTypes<{
    currentTab: {
        type: PropType<LeadTab>;
        required: true;
    };
    tabCounts: {
        type: PropType<TabCounts>;
        required: true;
        default: () => {
            new: number;
            saved: number;
            archived: number;
        };
    };
    languageStore: {
        type: ObjectConstructor;
        required: true;
    };
    isLoading: {
        type: BooleanConstructor;
        default: boolean;
    };
    industryOptions: {
        type: PropType<{
            value: string;
            text: string;
        }[]>;
        default: () => never[];
    };
    companySizeOptions: {
        type: PropType<{
            value: string;
            text: string;
        }[]>;
        default: () => {
            value: string;
            text: string;
        }[];
    };
    leadStatusOptions: {
        type: PropType<{
            value: string;
            text: string;
        }[]>;
        default: () => {
            value: string;
            text: string;
        }[];
    };
}>, {}, {}, {}, {}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {
    "update:currentTab": (...args: any[]) => void;
    "update:filters": (...args: any[]) => void;
}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    currentTab: {
        type: PropType<LeadTab>;
        required: true;
    };
    tabCounts: {
        type: PropType<TabCounts>;
        required: true;
        default: () => {
            new: number;
            saved: number;
            archived: number;
        };
    };
    languageStore: {
        type: ObjectConstructor;
        required: true;
    };
    isLoading: {
        type: BooleanConstructor;
        default: boolean;
    };
    industryOptions: {
        type: PropType<{
            value: string;
            text: string;
        }[]>;
        default: () => never[];
    };
    companySizeOptions: {
        type: PropType<{
            value: string;
            text: string;
        }[]>;
        default: () => {
            value: string;
            text: string;
        }[];
    };
    leadStatusOptions: {
        type: PropType<{
            value: string;
            text: string;
        }[]>;
        default: () => {
            value: string;
            text: string;
        }[];
    };
}>> & Readonly<{
    "onUpdate:currentTab"?: ((...args: any[]) => any) | undefined;
    "onUpdate:filters"?: ((...args: any[]) => any) | undefined;
}>, {
    tabCounts: TabCounts;
    isLoading: boolean;
    industryOptions: {
        value: string;
        text: string;
    }[];
    companySizeOptions: {
        value: string;
        text: string;
    }[];
    leadStatusOptions: {
        value: string;
        text: string;
    }[];
}, {}, {}, {}, string, import("vue").ComponentProvideOptions, true, {}, any>;
export default _default;
