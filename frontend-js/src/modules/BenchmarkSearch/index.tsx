import { useState } from 'react';
import { useQuery } from 'react-query';
import { SearchForm } from './searchForm';
import { Table } from './table';
import { LoadingOverlay } from '../loadingOverlay';
import { Benchmarks } from '../../api';
import { getHelper } from '../../api-helpers';
import { Paginator } from '../pagination';

function Page(props: { token: string }) {
    //const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(0);

    const [searchString, setSearchString] = useState<string>('');

    let { isLoading, isError, data, isSuccess } = useQuery(
        'benchmarkSearch-page-' + page + searchString,
        () => {
            return getHelper<Benchmarks>('/benchmarks/search', props.token, {
                // split here so we can add searchString to key to fetch automatically
                terms: searchString.split(' '),
            });
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <div className="container">
            <h1>Benchmark Search</h1>
            <SearchForm setSearchString={setSearchString} />
            <div style={{ position: 'relative' }}>
                {isLoading && (
                    <>
                        <Table results={[]} /> <LoadingOverlay />
                    </>
                )}
                {isError && <div>Failed to fetch benchmarks!</div>}
                {isSuccess && <Table results={data!.data.items!} />}
            </div>
            {isSuccess && <Paginator pagination={data!.data} navigateTo={setPage} />}
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
