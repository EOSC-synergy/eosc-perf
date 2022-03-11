import React, { ReactElement } from 'react';
import { Flavor } from 'model';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { SiteInfo } from 'components/reportView/siteInfo';
import { truthyOrNoneTag } from 'components/utility';

export function FlavorInfo(props: { id: string }): ReactElement {
    const flavor = useQuery(
        ['flavor', props.id],
        () => {
            return getHelper<Flavor>('/flavors/' + props.id);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const site = useQuery(
        ['site-for', props.id],
        () => {
            return getHelper<Flavor>('/flavors/' + props.id + '/site');
        },
        {
            refetchOnWindowFocus: false, // do not spam queries,
            enabled: flavor.isSuccess,
        }
    );

    return (
        <>
            {flavor.isLoading && <LoadingOverlay />}
            {flavor.isSuccess && flavor.data && (
                <>
                    Name: {flavor.data.data.name}
                    <br />
                    Description: {truthyOrNoneTag(flavor.data.data.description)}
                    <br />
                    Submitted on: {new Date(flavor.data.data.upload_datetime).toLocaleString()}
                    <hr />
                    Site:
                    <br />
                    {site.isSuccess && site.data && <SiteInfo id={site.data.data.id} />}
                </>
            )}
        </>
    );
}
