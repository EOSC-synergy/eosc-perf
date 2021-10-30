import React, { ReactElement } from 'react';
import { Site } from 'api';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { truthyOrNoneTag } from 'utility';

export function SiteInfo(props: { id: string }): ReactElement {
    const { isLoading, data, isSuccess } = useQuery(
        'site-' + props.id,
        () => {
            return getHelper<Site>('/sites/' + props.id);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <>
            {isLoading && <LoadingOverlay />}
            {isSuccess && data && (
                <>
                    New site: {data.data.name}
                    <br />
                    Address: {data.data.address}
                    <br />
                    Description: {truthyOrNoneTag(data.data.description)}
                    <br />
                    {/* Uploader: {{ uploader_name }} ({{ uploader_mail }})<br/> */}
                    <br />
                </>
            )}
        </>
    );
}
