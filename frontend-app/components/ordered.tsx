export type Ordered<T> = T & {
    orderIndex: number;
};

export function orderedComparator<T>(a: Ordered<T>, b: Ordered<T>): number {
    return a.orderIndex - b.orderIndex;
}
