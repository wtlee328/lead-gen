// src/types/tanstack-table.d.ts
import '@tanstack/vue-table'; // Important to ensure this is treated as an augmentation

declare module "@tanstack/vue-table" {
  interface ColumnMeta<TData, TValue> {
    style?: Record<string, string>;
  }
}