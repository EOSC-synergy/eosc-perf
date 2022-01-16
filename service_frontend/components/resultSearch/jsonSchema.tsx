import { Benchmark } from 'model';

export interface SchemaField {
    type?: string;
    suggestToUser?: boolean;
    description?: string;
}

export interface SchemaObject extends SchemaField {
    properties: { [key: string]: SchemaField };
}

export type Suggestion = {
    field: string;
    description?: string;
};

export function parseSuggestions(benchmark: Benchmark): Suggestion[] {
    function recurser([key, field]: [string, SchemaField]): Suggestion[] {
        if (field.suggestToUser && field.type !== 'object') {
            return [{ field: key, description: field.description }];
        }

        if (field.type === 'object') {
            return Object.entries((field as SchemaObject).properties)
                .map(recurser) // get all interesting children
                .reduce((acc: Suggestion[], arr: Suggestion[]) => [...acc, ...arr]) // make one array
                .map((suggestion: Suggestion) => {
                    return { ...suggestion, field: key + '.' + suggestion.field };
                }); // prefix current key
        }
        return [];
    }

    const schema = benchmark.json_schema as SchemaObject;

    if (schema === undefined || schema.properties === undefined) {
        return [];
    }

    return Object.entries(schema.properties)
        .map(recurser)
        .reduce((acc: Suggestion[], arr: Suggestion[]) => [...acc, ...arr]);
}
