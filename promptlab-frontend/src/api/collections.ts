import { apiClient } from './client';
import { Collection } from '../types/collection';

export const fetchCollections = async (): Promise<{ collections: Collection[]; total: number }> => {
    return apiClient('/collections');
};

export const fetchCollectionById = async (collectionId: string): Promise<Collection> => {
    return apiClient(`/collections/${collectionId}`);
};

export const createCollection = async (collection: Omit<Collection, 'id' | 'created_at'>): Promise<Collection> => {
    return apiClient('/collections', {
        method: 'POST',
        body: JSON.stringify(collection),
    });
};

export const updateCollection = async (collectionId: string, collection: Partial<Omit<Collection, 'id' | 'created_at'>>): Promise<Collection> => {
    return apiClient(`/collections/${collectionId}`, {
        method: 'PATCH',
        body: JSON.stringify(collection),
    });
};

export const deleteCollection = async (collectionId: string): Promise<void> => {
    await apiClient(`/collections/${collectionId}`, { method: 'DELETE' });
};