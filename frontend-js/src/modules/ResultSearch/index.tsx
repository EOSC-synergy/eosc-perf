import React from 'react';

type ResultSearchProps = {};

function ResultSearch(props: ResultSearchProps) {
    return <div>Result search!</div>;
}

const ResultSearchModule = {
    path: '/result-search',
    element: ResultSearch,
    name: 'ResultSearch',
    dropdownName: 'Results',
};

export default ResultSearchModule;
