import axios from 'axios';
import { API_BASE_PATH } from './configuration';

export function getHelper<Type>(endpoint: string, accessToken?: string) {
    if (accessToken !== undefined) {
        return axios.get<Type>(API_BASE_PATH + endpoint, {
            headers: {
                Authorization: 'Bearer ' + accessToken,
            },
        });
    }
    return axios.get<Type>(API_BASE_PATH + endpoint);
}
