import React, { ReactElement } from 'react';
import { Flavor } from 'api';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { LoadingOverlay } from 'components/loadingOverlay';
import { SiteInfo } from 'components/reportView/siteInfo';
import { truthyOrNoneTag } from 'utility';

export function FlavorInfo(props: { id: string }): ReactElement {
    const flavor = useQuery(
        'flavor-' + props.id,
        () => {
            return getHelper<Flavor>('/flavors/' + props.id);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    const site = useQuery(
        'site-for-' + props.id,
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
                    New flavor: {flavor.data.data.name}
                    <br />
                    Description: {truthyOrNoneTag(flavor.data.data.description)}
                    <br />
                    Site:
                    {site.isSuccess && site.data && <SiteInfo id={site.data.data.id} />}
                    <br />
                </>
            )}
        </>
    );
}
