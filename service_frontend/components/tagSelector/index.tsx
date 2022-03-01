import React, { ReactElement, useState } from 'react';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { Tag, Tags } from 'model';
import { Card, Col, Form, Row } from 'react-bootstrap';
import { PlaceholderTag } from './placeholderTag';
import { UnselectedTag } from './unselectedTag';
import { SelectedTag } from './selectedTag';
import { NewTag } from './newTag';

function Index(props: { selected: Tag[]; setSelected: (tags: Tag[]) => void }): ReactElement {
    const [searchString, setSearchString] = useState<string>('');
    const tags = useQuery(
        ['tags', searchString],
        () => {
            return getHelper<Tags>('/tags:search', undefined, {
                terms: searchString.split(' '),
            });
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
                        <small className="text-muted">Selected</small>
                        <div className="d-flex">
                            {props.selected.map((tag) => (
                                <SelectedTag tag={tag} unselect={unselect} key={tag.id} />
                            ))}
                        </div>
                        {props.selected.length === 0 && (
                            <div className="text-muted" style={{ display: 'inline' }}>
                                No tags selected
                            </div>
                        )}
                        <hr />
                        <small className="text-muted">Available</small>
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
                                {tags.data.data.total === 0 && searchString.length > 0 && (
                                    <div className="text-muted" style={{ display: 'inline' }}>
                                        No tags match the keywords
                                    </div>
                                )}
                                {tags.data.data.total === 0 && searchString.length === 0 && (
                                    <div className="text-muted" style={{ display: 'inline' }}>
                                        No tags available
                                    </div>
                                )}
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

export default Index;
