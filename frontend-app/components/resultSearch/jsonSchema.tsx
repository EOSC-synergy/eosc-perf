import { Benchmark } from 'model';

export interface SchemaField {
    type?: string;
    suggestToUser?: boolean;
}

export interface SchemaObject extends SchemaField {
    properties: { [key: string]: SchemaField };
}

export function determineNotableKeys(benchmark: Benchmark): string[] {
    function recurser([key, field]: [string, SchemaField]): string[] {
        if (field.suggestToUser && field.type !== 'object') {
            return [key];
        }

        if (field.type === 'object') {
            return Object.entries((field as SchemaObject).properties)
                .map(recurser) // get all interesting children
                .reduce((acc: string[], arr: string[]) => [...acc, ...arr]) // make one array
                .map((path: string) => key + '.' + path); // prefix current key
        }
        return [];
    }

    const schema = benchmark.json_schema as SchemaObject;

    if (schema === undefined || schema.properties === undefined) {
        return [];
    }

    return Object.entries(schema.properties)
        .map(recurser)
        .reduce((acc: string[], arr: string[]) => [...acc, ...arr]);
}
