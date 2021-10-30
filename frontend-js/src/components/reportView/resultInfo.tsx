import React, { ReactElement, useState } from 'react';
import { Result } from 'api';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { Button } from 'react-bootstrap';
import { JsonPreviewModal } from 'components/jsonPreviewModal';
import { benchmarkLinkDisplay, truthyOrNoneTag } from 'utility';

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
                <>
                    {/* TODO: *reporter* info */}
                    {/* Reported by: {{ reporter_name }} ({{ reporter_mail }})<br /> */}
                    {/* Uploader: {{ uploader_name }} ({{ uploader_mail }})<br /> */}
                    Site: {data.data.site.name}
                    <br />
                    Benchmark: {benchmarkLinkDisplay(data.data.benchmark)}
                    <br />
                    Tags: {truthyOrNoneTag(data.data.tags.map((tag) => tag.name).join(', '))}
                    <br />
                    <Button onClick={() => setShowPreview(true)} size="sm" className="mb-1">
                        View JSON
                    </Button>
                    <br />
                    {showPreview && (
                        <JsonPreviewModal
                            result={data.data}
                            show={showPreview}
                            closeModal={() => setShowPreview(false)}
                        />
                    )}
                </>
            )}
        </>
    );
}
