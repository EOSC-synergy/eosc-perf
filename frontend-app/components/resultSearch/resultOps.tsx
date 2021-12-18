import { Result } from 'model';
import { Ordered } from 'components/ordered';

export interface ResultOps {
    select: (result: Ordered<Result>) => void;
    selectMultiple: (result: Ordered<Result>[]) => void;
    unselect: (result: Result) => void;
    unselectMultiple: (result: Result[]) => void;
    isSelected: (result: Result) => boolean;

    // show pop up with result info & json
    display: (result: Result) => void;
    report: (result: Result) => void;
}
