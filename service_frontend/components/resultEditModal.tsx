import React, { useContext, useEffect, useState } from 'react';
import { Result, Tag, TagsIds } from 'model';
import { Button, Modal } from 'react-bootstrap';
import { useMutation } from 'react-query';
import { putHelper } from 'components/api-helpers';
import { UserContext } from 'components/userContext';
import { JsonHighlight } from 'components/jsonHighlight';
import TagSelector from './tagSelector';

export function ResultEditModal({
    result,
    show,
    closeModal,
}: {
    result: Result | null;
    show: boolean;
    closeModal: () => void;
}) {
    const [selectedTags, setSelectedTags] = useState<Tag[]>([]);

    useEffect(() => {
        setSelectedTags(result?.tags ?? []);
    }, [result]);

    const auth = useContext(UserContext);

    const { mutate } = useMutation(
        (data: TagsIds) => putHelper<TagsIds>('/results/' + result?.id + '/tags', data, auth.token),
        {
            onSuccess: () => {
                closeModal();
            },
        }
    );

    function submitEdit() {
        mutate({ tags_ids: selectedTags.map((tag) => tag.id) });
    }

    return (
        <Modal show={show} scrollable={true} size="lg" onHide={closeModal}>
            <Modal.Header>
                <Modal.Title>Edit result</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <h4>Tags</h4>
                <TagSelector selected={selectedTags} setSelected={setSelectedTags} />
                {result !== null && (
                    <>
                        <h4>Data</h4>
                        <JsonHighlight>{JSON.stringify(result.json, null, 4)}</JsonHighlight>
                    </>
                )}
                {result == null && <div className="text-muted">Loading...</div>}
            </Modal.Body>
            <Modal.Footer>
                <Button variant="success" onClick={submitEdit}>
                    Edit
                </Button>
                <Button variant="secondary" onClick={closeModal}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
