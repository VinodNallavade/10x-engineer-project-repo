export interface Prompt {
  id: string;
  title: string; // 1–200 characters
  content: string; // minimum 1 character, business validation >= 10 trimmed for quality checks
  description?: string | null; // maximum 500 characters
  collection_id?: string | null;
  tags: string[]; // maximum 20 tags, each tag <= 50 characters, normalized to lowercase and trimmed
  created_at: string;
  updated_at: string;
}