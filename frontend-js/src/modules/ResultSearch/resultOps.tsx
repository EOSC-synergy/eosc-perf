import { Result } from '../../api';

export interface ResultOps {
    select: (result: Result) => void;
    unselect: (result: Result) => void;
    isSelected: (result: Result) => boolean;

    // show pop up with result info & json
    display: (result: Result) => void;
    report: (result: Result) => void;
}
