export interface ModuleBase {
    routeProps: {
        path: string;
        component: () => JSX.Element;
    };
    name: string;
    dropdownName: string;
}
