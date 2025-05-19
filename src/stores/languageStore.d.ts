import type { LanguageCode, // Import the actual translations
Translations } from '@/types/language';
export declare const useLanguageStore: import("pinia").StoreDefinition<"language", Pick<{
    currentLang: import("vue").Ref<LanguageCode, LanguageCode>;
    setLanguage: (lang: LanguageCode) => void;
    toggleLanguage: () => void;
    industries: import("vue").ComputedRef<{
        value: string;
        text: string;
    }[]>;
    texts: import("vue").ComputedRef<Translations>;
    langToggleText: import("vue").ComputedRef<string>;
}, "currentLang">, Pick<{
    currentLang: import("vue").Ref<LanguageCode, LanguageCode>;
    setLanguage: (lang: LanguageCode) => void;
    toggleLanguage: () => void;
    industries: import("vue").ComputedRef<{
        value: string;
        text: string;
    }[]>;
    texts: import("vue").ComputedRef<Translations>;
    langToggleText: import("vue").ComputedRef<string>;
}, "texts" | "industries" | "langToggleText">, Pick<{
    currentLang: import("vue").Ref<LanguageCode, LanguageCode>;
    setLanguage: (lang: LanguageCode) => void;
    toggleLanguage: () => void;
    industries: import("vue").ComputedRef<{
        value: string;
        text: string;
    }[]>;
    texts: import("vue").ComputedRef<Translations>;
    langToggleText: import("vue").ComputedRef<string>;
}, "setLanguage" | "toggleLanguage">>;
