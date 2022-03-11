import React, { ReactElement } from 'react';
import { Site } from 'model';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { truthyOrNoneTag } from 'components/utility';

export function SiteInfo(props: { id: string }): ReactElement {
    const site = useQuery(
        ['site', props.id],
        () => {
            return getHelper<Site>('/sites/' + props.id);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <>
            {site.isLoading && <LoadingOverlay />}
            {site.isSuccess && site.data && (
                <>
                    Name: {site.data.data.name}
                    <br />
                    Address: {site.data.data.address}
                    <br />
                    Description: {truthyOrNoneTag(site.data.data.description)}
                    <br />
                    Submitted on: {new Date(site.data.data.upload_datetime).toLocaleString()}
                </>
            )}
        </>
    );
}
