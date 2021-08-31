import { useState } from 'react';
import { useQuery } from 'react-query';
import { SearchForm } from './searchForm';
import { Table } from './table';
import { LoadingOverlay } from '../../components/loadingOverlay';
import { Benchmarks } from '../../api';
import { getHelper } from '../../api-helpers';
import { Paginator } from '../../components/pagination';

function BenchmarkSearch() {
    //const [resultsPerPage, setResultsPerPage] = useState(10);
    const [page, setPage] = useState(0);

    const [searchString, setSearchString] = useState<string>('');

    let benchmarks = useQuery(
        'benchmarks-page-' + page + '-' + searchString,
        () => {
            return getHelper<Benchmarks>('/benchmarks/search', undefined, {
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
                {benchmarks.isLoading && (
                    <>
                        <Table results={[]} /> <LoadingOverlay />
                    </>
                )}
                {benchmarks.isError && <div>Failed to fetch benchmarks!</div>}
                {benchmarks.isSuccess && <Table results={benchmarks.data.data.items!} />}
            </div>
            {benchmarks.isSuccess && (
                <Paginator pagination={benchmarks.data.data} navigateTo={setPage} />
            )}
        </div>
    );
}

const BenchmarkSearchModule = {
    path: '/benchmark-search',
    element: BenchmarkSearch,
    name: 'BenchmarkSearch',
    dropdownName: 'Benchmarks',
};

export default BenchmarkSearchModule;
