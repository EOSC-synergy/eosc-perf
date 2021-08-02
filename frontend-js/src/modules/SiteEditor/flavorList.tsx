import { Flavor, Site } from '../../api';
import { useQuery } from 'react-query';
import { getHelper } from '../../api-helpers';
import { Card } from 'react-bootstrap';
import { LoadingOverlay } from '../loadingOverlay';
import { FlavorEdit } from './flavorEdit';
import React from 'react';

export function FlavorList(props: { site: Site; token: string }) {
    let { status, isLoading, isError, data, isSuccess, refetch } = useQuery(
        'flavors-' + props.site.id,
        () => {
            return getHelper<Flavor[]>('/sites/' + props.site.id + '/flavors', props.token);
        },
        {
            enabled: !!props.token,
            refetchOnWindowFocus: false, // do not spam queries
            refetchOnMount: 'always',
        }
    );

    return (
        <Card style={{ maxHeight: '16rem' }} className="overflow-auto">
            {isLoading && <LoadingOverlay />}
            {isSuccess &&
                data!.data.map((flavor: Flavor) => (
                    <FlavorEdit
                        flavor={flavor}
                        token={props.token}
                        key={flavor.id}
                        refetch={refetch}
                    />
                ))}
        </Card>
    );
}
