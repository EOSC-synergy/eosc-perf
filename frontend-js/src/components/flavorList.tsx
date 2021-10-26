import { Flavor, Flavors, Site } from 'api';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { Card } from 'react-bootstrap';
import { LoadingOverlay } from 'components/loadingOverlay';
import { FlavorEditor } from 'components/flavorEditor';
import React, { ReactElement } from 'react';

export function FlavorList(props: { site: Site }): ReactElement {
    const { isLoading, data, isSuccess, refetch } = useQuery(
        'flavors-' + props.site.id,
        () => {
            return getHelper<Flavors>('/sites/' + props.site.id + '/flavors');
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
            refetchOnMount: 'always',
        }
    );

    return (
        <Card style={{ maxHeight: '16rem' }} className="overflow-auto">
            {isLoading && <LoadingOverlay />}
            {isSuccess &&
                data &&
                data.data.items.map((flavor: Flavor) => (
                    <FlavorEditor flavor={flavor} key={flavor.id} refetch={refetch} />
                ))}
        </Card>
    );
}
