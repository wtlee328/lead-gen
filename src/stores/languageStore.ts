// src/stores/languageStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {
    industriesData, // Import the actual data
    uiTexts      // Import the actual translations
} from '@/types/language'; // Use '@' for alias to src directory (Vite default)
import type {
    LanguageCode,
    Industry,  // Import the actual translations
    Translations
} from '@/types/language'; 

// Define the store
export const useLanguageStore = defineStore('language', () => {
    // --- STATE ---
    const currentLang = ref<LanguageCode>('en'); // Default language (e.g., Chinese)

    // --- ACTIONS ---
    const setLanguage = (lang: LanguageCode) => {
        currentLang.value = lang;
        // You could also save this preference to localStorage here
        // localStorage.setItem('preferredLang', lang);
    };

    const toggleLanguage = () => {
        currentLang.value = currentLang.value === 'zh' ? 'en' : 'zh';
        // localStorage.setItem('preferredLang', currentLang.value);
    };

    // --- GETTERS (Computed properties) ---
    // Provides the list of industries in the currently selected language
    const industries = computed((): { value: string; text: string }[] => {
        return industriesData.map((industry: Industry) => ({
            value: industry.value,
            text: industry[currentLang.value] // Access 'zh' or 'en' property of industry object
        }));
    });

    // Provides all UI texts in the currently selected language
    const texts = computed((): Translations => {
        return uiTexts[currentLang.value];
    });

    // Provides the text for the language toggle button itself
    const langToggleText = computed((): string => {
        return currentLang.value === 'zh' ? 'EN' : '中文';
    });

    // Optional: Initialize language from localStorage on store creation
    // const preferredLang = localStorage.getItem('preferredLang');
    // if (preferredLang && (preferredLang === 'zh' || preferredLang === 'en')) {
    //   currentLang.value = preferredLang;
    // }

    return {
        // State
        currentLang,
        // Actions
        setLanguage,
        toggleLanguage,
        // Getters
        industries,
        texts,
        langToggleText
    };
});