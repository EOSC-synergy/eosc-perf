import React from 'react';
import { act, render, screen, waitFor } from '@testing-library/react';
import { setupServer } from 'msw/node';
import { rest } from 'msw';
import { Tag, Tags } from 'model';
import { TagSelector } from 'components/tagSelector';
import { QueryClient, QueryClientProvider } from 'react-query';
import { API_BASE_ROUTE } from 'components/configuration';

const tag: Tag = { id: 'test', name: 'testTag', description: null };
const tags: Tags = {
    has_next: true,
    has_prev: false,
    next_num: 2,
    items: [tag],
    page: 1,
    pages: 2,
    per_page: 1,
    prev_num: 1,
    total: 2
};

const server = setupServer();

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

const queryClient = new QueryClient();

test('select', async () => {
    server.use(
        rest.get(API_BASE_ROUTE + '/tags:search', (req, res, ctx) => {
            return res(ctx.json<Tags>(tags));
        })
    );
    const setSelected = jest.fn();
    render(
        <QueryClientProvider client={queryClient}>
            <TagSelector selected={[]} setSelected={setSelected} />
        </QueryClientProvider>
    );

    await waitFor(() => expect(screen.getByText(tag.name)).toBeInTheDocument(), {});
    act(() => screen.getByText(tag.name).click());
    expect(setSelected).toHaveBeenCalledWith([tag]);
});

test('unselect', async () => {
    server.use(
        rest.get(API_BASE_ROUTE + '/tags:search', (req, res, ctx) => {
            return res(ctx.json<Tags>(tags));
        })
    );
    const setSelected = jest.fn();
    render(
        <QueryClientProvider client={queryClient}>
            <TagSelector selected={[tag]} setSelected={setSelected} />
        </QueryClientProvider>
    );

    await waitFor(() => expect(screen.getByText(tag.name)).toBeInTheDocument(), {});
    act(() => {
        (
            screen.getByText(tag.name).querySelector('div') as HTMLElement | null
        )?.click();
    });
    expect(setSelected).toHaveBeenCalledWith([]);
});

// TODO: search
// TODO: submit
