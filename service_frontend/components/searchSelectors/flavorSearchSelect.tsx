import { Flavor, Site } from 'model';
import React, { ReactElement, useState } from 'react';
import { FlavorSubmissionModal } from 'components/submissionModals/flavorSubmissionModal';
import { SearchingSelector } from 'components/searchSelectors/index';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { truthyOrNoneTag } from '../utility';

export function FlavorSearchSelect(props: {
    site?: Site;
    flavor?: Flavor;
    initFlavor?: (flavor?: Flavor) => void;
    setFlavor: (flavor?: Flavor) => void;
    initialFlavorId?: string;
}): ReactElement {
    useQuery(
        ['initial-flavor', props.initialFlavorId],
        () => {
            return getHelper<Flavor>('/flavors/' + props.initialFlavorId);
        },
        {
            enabled: props.initialFlavorId !== undefined,
            refetchOnWindowFocus: false, // do not spam queries
            onSuccess: (data) => {
                if (props.initFlavor) {
                    props.initFlavor(data.data);
                } else {
                    props.setFlavor(data.data);
                }
            },
        }
    );

    function display(flavor?: Flavor) {
        return (
            <>
                Flavor:{' '}
                {truthyOrNoneTag(
                    flavor?.name,
                    props.site === undefined ? 'Select a site first!' : 'None'
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
            <SearchingSelector<Flavor>
                queryKeyPrefix={'flavor-for-' + props.site?.id}
                tableName="Flavor"
                endpoint={'/sites/' + props.site?.id + '/flavors:search'}
                item={props.flavor}
                setItem={props.setFlavor}
                display={display}
                displayRow={displayRow}
                submitNew={() => setShowSubmitModal(true)}
                disabled={props.site === undefined}
            />
            {props.site !== undefined && (
                <FlavorSubmissionModal
                    show={showSubmitModal}
                    onHide={() => setShowSubmitModal(false)}
                    site={props.site}
                />
            )}
        </>
    );
}
