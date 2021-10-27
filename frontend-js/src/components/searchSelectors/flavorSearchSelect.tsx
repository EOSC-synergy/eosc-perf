import { Flavor, Site } from 'api';
import React, { ReactElement, useEffect, useState } from 'react';
import { FlavorSubmissionModal } from 'components/submissionModals/flavorSubmissionModal';
import { SearchingSelector } from 'components/searchSelectors/index';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';

export function FlavorSearchSelect(props: {
    site?: Site;
    flavor?: Flavor;
    setFlavor: (flavor?: Flavor) => void;
    initialFlavorId?: string;
}): ReactElement {
    // TODO: reset value if site is undefined?

    useQuery(
        'initial-flavor-' + props.initialFlavorId,
        () => {
            return getHelper<Flavor>('/flavors/' + props.initialFlavorId);
        },
        {
            enabled: props.initialFlavorId !== undefined,
            refetchOnWindowFocus: false, // do not spam queries
            onSuccess: (data) => {
                props.setFlavor(data.data);
            },
        }
    );

    useEffect(() => props.setFlavor(undefined), [props.site]);

    function display(flavor?: Flavor) {
        return (
            <>
                Flavor:{' '}
                {flavor ? (
                    <>{flavor.name}</>
                ) : (
                    <div className="text-muted" style={{ display: 'inline-block' }}>
                        None
                    </div>
                )}
            </>
        );
    }

    function displayRow(flavor: Flavor) {
        return (
            <>
                {flavor.name}
                <div>
                    {flavor.description}
                    <br />
                </div>
            </>
        );
    }

    const [showSubmitModal, setShowSubmitModal] = useState(false);

    return (
        <>
            {props.site ? (
                <>
                    <SearchingSelector<Flavor>
                        queryKeyPrefix={'flavor-for-' + props.site.id}
                        tableName="Flavor"
                        endpoint={'/sites/' + props.site.id + '/flavors:search'}
                        item={props.flavor}
                        setItem={props.setFlavor}
                        display={display}
                        displayRow={displayRow}
                        submitNew={() => setShowSubmitModal(true)}
                    />
                    <FlavorSubmissionModal
                        show={showSubmitModal}
                        onHide={() => setShowSubmitModal(false)}
                        site={props.site}
                    />
                </>
            ) : (
                <></>
            )}
        </>
    );
}
