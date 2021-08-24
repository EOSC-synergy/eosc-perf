import axios from 'axios';
import { API_BASE_PATH } from './configuration';

const qs = require('qs');

export function getHelper<Type>(endpoint: string, accessToken?: string, params?: object) {
    if (accessToken !== undefined) {
        return axios.get<Type>(API_BASE_PATH + endpoint, {
            headers: {
                Authorization: 'Bearer ' + accessToken,
            },
            params: params,
            paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' }),
        });
    }
    return axios.get<Type>(API_BASE_PATH + endpoint, {
        params: params,
        paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' }),
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
            paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' }),
        });
    }
    return axios.post<Type>(API_BASE_PATH + endpoint, data, {
        params: params,
        paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' }),
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
            paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' }),
        });
    }
    return axios.put<Type>(API_BASE_PATH + endpoint, data, {
        params: params,
        paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' }),
    });
}

export function patchHelper<Type>(
    endpoint: string,
    { data, accessToken, params }: { data?: Type; accessToken?: string; params?: object }
) {
    if (accessToken !== undefined) {
        return axios.patch<Type>(API_BASE_PATH + endpoint, data, {
            headers: {
                Authorization: 'Bearer ' + accessToken,
            },
            params: params,
            paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' }),
        });
    }
    return axios.patch<Type>(API_BASE_PATH + endpoint, data, {
        params: params,
        paramsSerializer: (params) => qs.stringify(params, { arrayFormat: 'repeat' }),
    });
}
