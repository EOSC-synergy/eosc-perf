import React, { FormEvent, useState } from 'react';

type BenchmarkSearchResponse = {};

export function SearchForm() {
    const [message, setMessage] = useState('');

    function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        // @ts-ignore
        setMessage(event.target.query);
    }

    return (
        <form onSubmit={handleSubmit} className="flexbox">
            <label htmlFor={'query'} className={'sr-only'}>
                Query
            </label>
            <input
                type={'text'}
                name={'query'}
                className={'form-control'}
                style={{ flex: '10 1 0' }}
                placeholder={'Enter your query here, keywords separated by spaces'}
            />
            <input type={'submit'} className={'btn btn-info'} name={'submit'} value={'Search'} />
        </form>
    );
}
