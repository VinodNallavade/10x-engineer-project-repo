export type Prompt = {
  id: string;
  title: string;
  content: string;
  description?: string | null;
  collection_id?: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
};

export type Collection = {
  id: string;
  name: string;
  description?: string | null;
  created_at: string;
};

export type ListResponse<T> = {
  items: T[];
  total: number;
};