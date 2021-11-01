import React, { ReactElement, useContext, useState } from 'react';
import { useMutation, useQuery } from 'react-query';
import { getHelper, postHelper } from 'api-helpers';
import { CreateTag, Tag, Tags } from 'api';
import { Button, Card, Col, Form, InputGroup, Placeholder, Row } from 'react-bootstrap';

import 'components/actionable.css';
import 'components/tagSelector.css';
import { UserContext } from 'components/userContext';
import { InlineCloseButton } from 'components/inlineCloseButton';

function PlaceholderTag() {
    return (
        <div className="tagBadge p-1">
            <Placeholder xs={12} style={{ width: '2em' }} />
        </div>
    );
}

function UnselectedTag(props: { tag: Tag; select: (tag: Tag) => void }) {
    return (
        <div className="tagBadge p-1 actionable" onClick={() => props.select(props.tag)}>
            {props.tag.name}
        </div>
    );
}

function SelectedTag(props: { tag: Tag; unselect: (tag: Tag) => void }) {
    return (
        <div className="tagBadge p-1">
            {props.tag.name}
            <InlineCloseButton onClose={() => props.unselect(props.tag)} />
        </div>
    );
}

function NewTag(props: { onSubmit: () => void }) {
    const [customTagName, setCustomTagName] = useState('');
    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: CreateTag) => postHelper<CreateTag>('/tags', data, auth.token),
        {
            onSuccess: () => {
                props.onSubmit();
            },
        }
    );

    function addTag() {
        mutate({
            name: customTagName,
            description: '',
        });
    }

    return (
        <Form.Group>
            <InputGroup>
                <Form.Control
                    id="custom-tag"
                    placeholder="tensor"
                    onChange={(e) => setCustomTagName(e.target.value)}
                />
                <Button
                    variant="success"
                    disabled={!auth.token || customTagName.length < 1}
                    onClick={() => addTag()}
                    className="reset-z-index"
                >
                    Add Tag
                </Button>
            </InputGroup>
        </Form.Group>
    );
}

export function TagSelector(props: {
    selected: Tag[];
    setSelected: (tags: Tag[]) => void;
}): ReactElement {
    const [searchString, setSearchString] = useState<string>('');
    const tags = useQuery(
        ['tags', searchString],
        () => {
            return getHelper<Tags>('/tags:search', undefined, { terms: searchString.split(' ') });
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
            keepPreviousData: true,
        }
    );

    function select(newTag: Tag) {
        if (props.selected.some((tag) => tag.id === newTag.id)) {
            return;
        }
        props.setSelected([...props.selected, newTag]);
    }

    function unselect(oldTag: Tag) {
        props.setSelected(props.selected.filter((tag) => tag.id !== oldTag.id));
    }

    return (
        <Card className="d-inline-block">
            <Card.Body>
                <Form.Group className="mb-1" as={Row}>
                    <Form.Label column sm={3}>
                        Search
                    </Form.Label>
                    <Col sm={9}>
                        <Form.Control
                            type="text"
                            placeholder="Keywords..."
                            onChange={(search) => setSearchString(search.target.value)}
                        />
                    </Col>
                </Form.Group>
                <Card className="mb-1">
                    <Card.Body>
                        <div className="d-flex">
                            {props.selected.map((tag) => (
                                <SelectedTag tag={tag} unselect={unselect} key={tag.id} />
                            ))}
                        </div>
                        <hr />
                        {tags.isPreviousData && tags.data && (
                            <>
                                <div className="d-flex">
                                    {tags.data.data.items
                                        .filter(
                                            (tag) =>
                                                !props.selected.some(
                                                    (selected) => selected.id === tag.id
                                                )
                                        )
                                        .map((tag) => (
                                            <PlaceholderTag key={tag.id} />
                                        ))}
                                </div>
                            </>
                        )}
                        {tags.isSuccess && !tags.isPreviousData && tags.data && (
                            <>
                                <div className="d-flex">
                                    {tags.data.data.items
                                        .filter(
                                            (tag) =>
                                                !props.selected.some(
                                                    (selected) => selected.id === tag.id
                                                )
                                        )
                                        .map((tag) => (
                                            <UnselectedTag tag={tag} select={select} key={tag.id} />
                                        ))}
                                </div>
                                {tags.data.data.has_next && (
                                    <div className="text-muted">
                                        <small>More tags hidden, use search terms</small>
                                    </div>
                                )}
                            </>
                        )}
                    </Card.Body>
                </Card>
                <NewTag onSubmit={() => tags.refetch().then(() => undefined)} />
            </Card.Body>
        </Card>
    );
}
