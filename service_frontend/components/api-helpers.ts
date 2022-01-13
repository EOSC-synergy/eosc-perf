import axios, { AxiosResponse } from 'axios';
import { API_BASE_PATH } from 'components/configuration';

import qs from 'qs';

const defaultOptions = {
    paramsSerializer: (params: unknown) => qs.stringify(params, { arrayFormat: 'repeat' }),
};

export function getHelper<Type>(
    endpoint: string,
    accessToken?: string,
    params?: Record<string, unknown>
): Promise<AxiosResponse<Type>> {
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
    data?: Type,
    accessToken?: string,
    params?: Record<string, unknown>
): Promise<AxiosResponse<Type>> {
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
    params?: Record<string, unknown>
): Promise<AxiosResponse<Type>> {
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
    {
        data,
        accessToken,
        params,
    }: { data?: Type; accessToken?: string; params?: Record<string, unknown> }
): Promise<AxiosResponse<Type>> {
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

export function deleteHelper(endpoint: string, accessToken?: string): Promise<AxiosResponse> {
    return axios.delete(API_BASE_PATH + endpoint, {
        headers:
            accessToken !== undefined
                ? {
                      Authorization: 'Bearer ' + accessToken,
                  }
                : undefined,
        ...defaultOptions,
    });
}
