import axios from 'axios';

export function getHelper<Type>(endpoint: string, accessToken?: string) {
    if (accessToken !== undefined) {
        return axios.get<Type>(endpoint, {
            headers: {
                Authorization: 'Bearer ' + accessToken,
            },
        });
    }
    return axios.get<Type>(endpoint);
}
