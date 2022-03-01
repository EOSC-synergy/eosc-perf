import { Result } from 'model';
import { Ordered } from 'components/ordered';

export interface ResultCallbacks {
    select: (result: Ordered<Result>) => void;
    selectMultiple: (result: Ordered<Result>[]) => void;
    unselect: (result: Result) => void;
    unselectMultiple: (result: Result[]) => void;
    isSelected: (result: Result) => boolean;

    reload: () => void;

    // show pop up with result info & json
    display: (result: Result) => void;
    report: (result: Result) => void;
    edit: (result: Result) => void;
}
