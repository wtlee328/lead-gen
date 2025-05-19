// src/stores/languageStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {
    industriesData,
    uiTexts // Import the actual translations
} from '@/types/language';
import type {
    LanguageCode,
    Industry,
    Translations
} from '@/types/language';

// Log uiTexts immediately after import to see if it's loaded correctly
console.log('[languageStore] Imported uiTexts:', JSON.parse(JSON.stringify(uiTexts || { note: "uiTexts was undefined/null upon import" })));
console.log('[languageStore] Type of uiTexts:', typeof uiTexts);


export const useLanguageStore = defineStore('language', () => {
    console.log('[languageStore] Initializing store setup function...');
    const currentLang = ref<LanguageCode>('en');

    const setLanguage = (lang: LanguageCode) => {
        console.log('[languageStore] setLanguage called with:', lang);
        currentLang.value = lang;
    };

    const toggleLanguage = () => {
        const newLang = currentLang.value === 'zh' ? 'en' : 'zh';
        console.log('[languageStore] toggleLanguage. Old:', currentLang.value, 'New:', newLang);
        currentLang.value = newLang;
    };

    const industries = computed((): { value: string; text: string }[] => {
        // ... (your industries logic)
        return industriesData.map((industry: Industry) => ({
            value: industry.value,
            text: industry[currentLang.value]
        }));
    });

    const texts = computed((): Translations => {
        console.log(`[languageStore] 'texts' computed triggered. currentLang: ${currentLang.value}`);
        if (!uiTexts || !uiTexts[currentLang.value]) {
            console.error(`[languageStore] CRITICAL: uiTexts OR uiTexts[${currentLang.value}] is undefined/null!`);
            // Return a minimal fallback to prevent "cannot read properties of undefined"
            return {
                updateAvailableMessage: 'Error: Lang texts missing!',
                refreshNowButton: 'Error Refresh',
                // Add other critical keys your app might immediately access from texts
            } as unknown as Translations; // Cast if your minimal fallback isn't a full Translations
        }
        const resolvedTexts = uiTexts[currentLang.value];
        console.log('[languageStore] "texts" computed resolved to:', JSON.parse(JSON.stringify(resolvedTexts)));
        return resolvedTexts;
    });

    const langToggleText = computed((): string => {
        return currentLang.value === 'zh' ? 'EN' : '中文';
    });

    console.log('[languageStore] Store setup function complete. Default lang:', currentLang.value);

    return {
        currentLang,
        setLanguage,
        toggleLanguage,
        industries,
        texts,
        langToggleText
    };
});