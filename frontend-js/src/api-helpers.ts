import axios from 'axios';
import { API_BASE_PATH } from './configuration';

export function getHelper<Type>(endpoint: string, accessToken?: string, params?: object) {
    if (accessToken !== undefined) {
        return axios.get<Type>(API_BASE_PATH + endpoint, {
            headers: {
                Authorization: 'Bearer ' + accessToken,
            },
            params: params,
        });
    }
    return axios.get<Type>(API_BASE_PATH + endpoint, {
        params: params,
    });
}

export function postHelper<Type>(
    endpoint: string,
    data: Type,
    accessToken?: string,
    params?: object
) {
    if (accessToken !== undefined) {
        return axios.post<Type>(API_BASE_PATH + endpoint, data, {
            headers: {
                Authorization: 'Bearer ' + accessToken,
            },
            params: params,
        });
    }
    return axios.post<Type>(API_BASE_PATH + endpoint, data, {
        params: params,
    });
}

export function putHelper<Type>(
    endpoint: string,
    data: Type,
    accessToken?: string,
    params?: object
) {
    if (accessToken !== undefined) {
        return axios.put<Type>(API_BASE_PATH + endpoint, data, {
            headers: {
                Authorization: 'Bearer ' + accessToken,
            },
            params: params,
        });
    }
    return axios.put<Type>(API_BASE_PATH + endpoint, data, { params: params });
}
