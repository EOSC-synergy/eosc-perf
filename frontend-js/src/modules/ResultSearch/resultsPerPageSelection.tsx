import React from 'react';

export function ResultsPerPageSelection(props: {
    onChange: (resultsPerPage: number) => void;
    currentSelection: number;
}) {
    const options = [10, 15, 20, 50, 100];

    return (
        <div className="form-inline">
            <label htmlFor="results_on_page">Results on page:</label>
            <select
                id="results_on_page"
                className="custom-select"
                onChange={(e) => props.onChange(parseInt(e.target.value))}
            >
                {options.map((n: number) => (
                    <option value={n.toString()} {...(n === props.currentSelection && 'selected')}>
                        {n.toString()}
                    </option>
                ))}
            </select>
        </div>
    );
}
