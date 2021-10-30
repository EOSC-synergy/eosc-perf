import React, { ReactElement, useState } from 'react';
import { Result } from 'api';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { Button } from 'react-bootstrap';
import { JsonPreviewModal } from 'components/jsonPreviewModal';
import { truthyOrNoneTag } from 'utility';

export function ResultInfo(props: { id: string }): ReactElement {
    const { isLoading, data, isSuccess } = useQuery(
        'result-' + props.id,
        () => {
            return getHelper<Result>('/results/' + props.id);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const [showPreview, setShowPreview] = useState(false);

    return (
        <>
            {isLoading && <LoadingOverlay />}
            {isSuccess && data && (
                <p>
                    {/* TODO: *reporter* info */}
                    {/* Reported by: {{ reporter_name }} ({{ reporter_mail }})<br /> */}
                    {/*Message: {props.claim.message}*/}
                    <br />
                    Site: {data.data.site.name}
                    <br />
                    Benchmark: {data.data.benchmark.docker_image + data.data.benchmark.docker_tag}
                    <br />
                    {/* Uploader: {{ uploader_name }} ({{ uploader_mail }})<br /> */}
                    Tags: {truthyOrNoneTag(data.data.tags.map((tag) => tag.name).join(', '))}
                    <br />
                    <Button onClick={() => setShowPreview(true)} size="sm">
                        View JSON
                    </Button>
                    {showPreview && (
                        <JsonPreviewModal
                            result={data.data}
                            show={showPreview}
                            closeModal={() => setShowPreview(false)}
                        />
                    )}
                </p>
            )}
        </>
    );
}
