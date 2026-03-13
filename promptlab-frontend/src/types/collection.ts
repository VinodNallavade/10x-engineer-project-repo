export interface Collection {
  id: string;
  name: string; // 1–100 characters
  description?: string | null; // max 500 characters
  created_at: string;
}