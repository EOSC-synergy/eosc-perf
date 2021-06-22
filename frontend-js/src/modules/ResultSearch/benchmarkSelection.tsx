import React, { ChangeEvent } from 'react';

export function BenchmarkSelection(props: {
    onChange: (benchmark: string) => void;
    benchmark: string;
}) {
    function handleSelect(e: ChangeEvent<HTMLSelectElement>) {
        e.preventDefault();

        const newSelection = e.target.value;
        props.onChange(newSelection);
    }

    return (
        <div className="form-inline">
            <label htmlFor="benchmark_selection">Benchmark:</label>
            <select className="custom-select" id="benchmark_selection" onChange={handleSelect}>
                <option>{/* TODO: useQuery, get benchmarks, mark selected */}</option>
            </select>
            <button
                className="btn btn-outline-secondary"
                type="button"
                id="dockerhubLinkButton"
                {...(props.benchmark.length > 0 && 'disabled')}
            >
                View on Docker Hub
            </button>
        </div>
    );
}
