import { ReactElement } from 'react';

export interface Page {
    path: string;
    component: () => ReactElement;
    name: string;
    displayName: string;
}
