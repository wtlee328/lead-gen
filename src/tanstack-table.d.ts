// src/tanstack-table.d.ts (or src/env.d.ts, etc.)
import '@tanstack/vue-table'; // Ensures TS knows which module to augment

declare module '@tanstack/vue-table' {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  interface ColumnMeta<TData, TValue> {
    style?: Record<string, string>;
    // Add any other custom meta properties
  }
}