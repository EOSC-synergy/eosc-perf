import { Flavor, Site } from 'api';
import React, { ReactElement, useState } from 'react';
import { FlavorSubmissionModal } from 'components/submissionModals/flavorSubmissionModal';
import { SearchingSelector } from 'components/searchSelectors/index';

export function FlavorSearchSelect(props: {
    site?: Site;
    flavor?: Flavor;
    setFlavor: (flavor?: Flavor) => void;
}): ReactElement {
    // TODO: reset value if site is undefined?

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
                <a title={flavor.name} href="#" onClick={() => props.setFlavor(flavor)}>
                    {flavor.name}
                </a>
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
