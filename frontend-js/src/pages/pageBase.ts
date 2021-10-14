import { ReactElement } from 'react';

export interface PageBase {
    path: string;
    element: () => ReactElement;
    name: string;
    displayName: string;
}
