import React, { useEffect, useState } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import { SearchForm } from './searchForm';
import { Table } from './table';
import { LoadingOverlay } from '../loadingOverlay';
import { Benchmark } from '../../api';
import { getHelper } from '../../api-helpers';

function Page(props: { token: string }) {
    const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(0);

    let { status, isLoading, isError, data, isSuccess } = useQuery(
        'benchmarkSearch',
        () => {
            return getHelper<Benchmark[]>('/benchmarks', props.token);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );
    return (
        <div className="container">
            <h1>Benchmark Search</h1>
            <SearchForm />
            <div style={{ position: 'relative' }}>
                {isLoading && (
                    <>
                        <Table results={[]} /> <LoadingOverlay />
                    </>
                )}
                {isError && <div>Failed to fetch benchmarks!</div>}
                {isSuccess && (
                    <Table
                        results={data!.data.slice(
                            page * resultsPerPage,
                            (page + 1) * resultsPerPage
                        )}
                    />
                )}
            </div>
        </div>
    );
}

const BenchmarkSearchModule = {
    path: '/benchmark-search',
    element: Page,
    name: 'BenchmarkSearch',
    dropdownName: 'Benchmarks',
};

export default BenchmarkSearchModule;
