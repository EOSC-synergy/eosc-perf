import axios from 'axios';
import { API_BASE_PATH } from './configuration';

const qs = require('qs');

const defaultOptions = {
    paramsSerializer: (params: any) => qs.stringify(params, { arrayFormat: 'repeat' }),
};

export function getHelper<Type>(endpoint: string, accessToken?: string, params?: object) {
    return axios.get<Type>(API_BASE_PATH + endpoint, {
        headers:
            accessToken !== undefined
                ? {
                      Authorization: 'Bearer ' + accessToken,
                  }
                : undefined,
        params: params,
        ...defaultOptions,
    });
}

export function postHelper<Type>(
    endpoint: string,
    data: Type,
    accessToken?: string,
    params?: object
) {
    return axios.post<Type>(API_BASE_PATH + endpoint, data, {
        headers:
            accessToken !== undefined
                ? {
                      Authorization: 'Bearer ' + accessToken,
                  }
                : undefined,
        params: params,
        ...defaultOptions,
    });
}

export function putHelper<Type>(
    endpoint: string,
    data: Type,
    accessToken?: string,
    params?: object
) {
    return axios.put<Type>(API_BASE_PATH + endpoint, data, {
        headers:
            accessToken !== undefined
                ? {
                      Authorization: 'Bearer ' + accessToken,
                  }
                : undefined,
        params: params,
        ...defaultOptions,
    });
}

export function patchHelper<Type>(
    endpoint: string,
    { data, accessToken, params }: { data?: Type; accessToken?: string; params?: object }
) {
    return axios.patch<Type>(API_BASE_PATH + endpoint, data, {
        headers:
            accessToken !== undefined
                ? {
                      Authorization: 'Bearer ' + accessToken,
                  }
                : undefined,
        params: params,
        ...defaultOptions,
    });
}
