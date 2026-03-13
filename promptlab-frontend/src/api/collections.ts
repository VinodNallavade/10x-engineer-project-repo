import { apiClient } from './client';
import { Collection } from '../types/collection';

export const fetchCollections = async (): Promise<{ collections: Collection[]; total: number }> => {
    const response = await apiClient.get('/collections');
    return response.data;
};

export const fetchCollectionById = async (collectionId: string): Promise<Collection> => {
    const response = await apiClient.get(`/collections/${collectionId}`);
    return response.data;
};

export const createCollection = async (collection: Omit<Collection, 'id' | 'created_at'>): Promise<Collection> => {
    const response = await apiClient.post('/collections', collection);
    return response.data;
};

export const updateCollection = async (collectionId: string, collection: Partial<Omit<Collection, 'id' | 'created_at'>>): Promise<Collection> => {
    const response = await apiClient.patch(`/collections/${collectionId}`, collection);
    return response.data;
};

export const deleteCollection = async (collectionId: string): Promise<void> => {
    await apiClient.delete(`/collections/${collectionId}`);
};