import { createClient } from '@supabase/supabase-js';

// Retrieve environment variables
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string;

// Check if the environment variables are loaded
if (!supabaseUrl || !supabaseAnonKey) {
    const errorMessage = "Supabase URL or Anon Key is missing. " +
                         "Ensure VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY " +
                         "are defined in your .env.local file.";
    console.error(errorMessage);
    throw new Error(errorMessage);
}

// Create and export the Supabase client instance
export const supabase = createClient(supabaseUrl, supabaseAnonKey);