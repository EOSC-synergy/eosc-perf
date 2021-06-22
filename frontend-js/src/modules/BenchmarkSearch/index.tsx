import React, { useEffect, useState } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import { Result } from './types';
import { SearchForm } from './searchForm';
import { Table } from './table';
import { LoadingOverlay } from '../loadingOverlay';

type PageState = {
    results: Result[];
    page: number;
    resultsPerPage: number;
};

function Page(props: { token: string }) {
    const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(0);

    // put token in state
    const [token, setToken] = useState(props.token);
    // propagate props to state for token update
    useEffect(() => {
        setToken(props.token);
    }, [props.token]);

    let { status, isLoading, isError, data, isSuccess } = useQuery(
        'benchmarkSearch',
        () => {
            const endpoint = 'https://localhost/api/benchmarks';
            if (token !== undefined) {
                return axios.get<Result[]>(endpoint, {
                    headers: {
                        Authorization: 'Bearer ' + token,
                    },
                });
            }
            return axios.get<Result[]>(endpoint);
        },
        {
            enabled: !!token,
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <div className="container">
            <h1>Benchmark Search</h1>
            <SearchForm />
            <div style={{ position: 'relative' }}>
                {isLoading && <LoadingOverlay />}
                <Table
                    results={
                        data
                            ? data.data.slice(page * resultsPerPage, page * (resultsPerPage + 1))
                            : []
                    }
                />
            </div>
        </div>
    );
}

export default {
    path: '/benchmark-search',
    element: Page,
    name: 'BenchmarkSearch',
    dropdownName: 'Benchmarks',
};
