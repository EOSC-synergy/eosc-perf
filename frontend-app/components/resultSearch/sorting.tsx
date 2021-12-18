export type Sorting = {
    mode: SortMode;
    key: string;
};

export enum SortMode {
    Disabled = 0,
    Ascending,
    Descending,
}
