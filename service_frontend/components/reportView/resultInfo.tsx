import React, { ReactElement, useState } from 'react';
import { Result } from 'model';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { Button } from 'react-bootstrap';
import { JsonPreviewModal } from 'components/jsonPreviewModal';
import { benchmarkLinkDisplay, truthyOrNoneTag } from 'components/utility';

export function ResultInfo(props: { id: string }): ReactElement {
    const result = useQuery(
        ['result', props.id],
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
            {result.isLoading && <LoadingOverlay />}
            {result.isSuccess && result.data && (
                <>
                    Site: {result.data.data.site.name}
                    <br />
                    Benchmark: {benchmarkLinkDisplay(result.data.data.benchmark)}
                    <br />
                    Tags: {truthyOrNoneTag(result.data.data.tags.map((tag) => tag.name).join(', '))}
                    <br />
                    <Button onClick={() => setShowPreview(true)} size="sm" className="mb-1">
                        View JSON
                    </Button>
                    <br />
                    {showPreview && (
                        <JsonPreviewModal
                            result={result.data.data}
                            show={showPreview}
                            closeModal={() => setShowPreview(false)}
                        />
                    )}
                </>
            )}
        </>
    );
}
