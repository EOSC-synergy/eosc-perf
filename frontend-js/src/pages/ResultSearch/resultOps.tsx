import { Result } from 'api';
import { Ordered } from 'components/ordered';

export interface ResultOps {
    select: (result: Ordered<Result>) => void;
    unselect: (result: Ordered<Result>) => void;
    isSelected: (result: Ordered<Result>) => boolean;

    // show pop up with result info & json
    display: (result: Ordered<Result>) => void;
    report: (result: Ordered<Result>) => void;
}
