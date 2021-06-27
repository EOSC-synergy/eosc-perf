import React, { ReactNode } from 'react';
import { Button, ButtonGroup, Form } from 'react-bootstrap';
import { SelectableResult } from './selectableResult';

export class Column {
    public readonly stock: boolean;
    public readonly name: string;

    constructor(stock: boolean, name: string) {
        this.stock = false;
        this.name = name;
    }

    generateView(result: SelectableResult): ReactNode {
        return <div />;
    }
}

/**
 * Fetch a sub-key from an object, as noted by the filter JSON syntax.
 * @param obj The object to get the value from.
 * @param keyPath The path to the value.
 * @returns {*} Anything, or SUBKEY_NOT_FOUND_HINT if not found.
 * @private
 */
function fetchSubkey(obj: any, keyPath: string) {
    const keys = keyPath.split('.');
    let sub_item = obj;
    for (let sub_key of keys) {
        if (typeof sub_item === 'undefined') {
            return undefined;
        }
        sub_item = sub_item[sub_key];
    }
    return sub_item;
}

export class CustomColumn extends Column {
    private readonly key: string;

    constructor(key: string) {
        super(false, key);
        this.key = key;
    }

    generateView(result: SelectableResult): ReactNode {
        const value = fetchSubkey(result.json, this.key);
        return value ? value.toString() : 'Not found!';
    }
}

export class CheckboxColumn extends Column {
    constructor() {
        super(true, '');
    }

    generateView(result: SelectableResult): ReactNode {
        return (
            <Form>
                <Form.Check
                    custom
                    onClick={() => {
                        result.selected = !result.selected;
                    }}
                    checked={result.selected}
                />
            </Form>
        );
    }
}

export class BenchmarkColumn extends Column {
    constructor() {
        super(true, 'Benchmark');
    }

    generateView(result: SelectableResult): React.ReactNode {
        return result.benchmark_image + ':' + result.benchmark_tag;
    }
}

export class SiteColumn extends Column {
    constructor() {
        super(true, 'Site');
    }

    generateView(result: SelectableResult): React.ReactNode {
        return result.site_name;
    }
}

export class SiteFlavorColumn extends Column {
    constructor() {
        super(true, 'Site flavor');
    }

    generateView(result: SelectableResult): React.ReactNode {
        return result.flavor_name;
    }
}

export class TagsColumn extends Column {
    constructor() {
        super(true, 'Tags');
    }

    generateView(result: SelectableResult): React.ReactNode {
        if (result.tag_names.length) {
            return result.tag_names.reduce((a: string, b: string) => a + ', ' + b);
        }
        return <div className="text-muted">None</div>;
    }
}

export class ActionColumn extends Column {
    private readonly displayResult: (result: SelectableResult) => void;
    private readonly admin: boolean;

    constructor(displayResult: (result: SelectableResult) => void, admin: boolean) {
        super(true, 'Actions');

        this.displayResult = displayResult;
        this.admin = admin;
    }

    generateView(result: SelectableResult): React.ReactNode {
        return (
            <ButtonGroup size="sm">
                <Button
                    variant="primary"
                    onClick={() => {
                        this.displayResult(result);
                    }}
                />
                <Button variant="warning" onClick={() => {} /* TODO: report button */} />
                {this.admin && (
                    <>
                        <Button variant="secondary" onClick={() => {} /* TODO: mail button */} />{' '}
                        <Button variant="danger" onClick={() => {} /* TODO: delete button */} />{' '}
                    </>
                )}
            </ButtonGroup>
        );
    }
}
