import { Site } from 'api';
import React, { ReactElement, useState } from 'react';
import { SiteSubmissionModal } from 'components/submissionModals/siteSubmissionModal';
import { SearchingSelector } from 'components/searchSelectors/index';

export function SiteSearchPopover(props: {
    site?: Site;
    setSite: (site?: Site) => void;
}): ReactElement {
    function display(site?: Site) {
        return (
            <>
                Site:{' '}
                {site ? (
                    <>{site.name}</>
                ) : (
                    <div className="text-muted" style={{ display: 'inline-block' }}>
                        None
                    </div>
                )}
            </>
        );
    }

    function displayRow(site: Site) {
        return (
            <>
                <a title={site.name} href="#" onClick={() => props.setSite(site)}>
                    {site.name}
                </a>
                <div>
                    {site.description}
                    <br />
                </div>
            </>
        );
    }

    const [showSubmitModal, setShowSubmitModal] = useState(false);

    return (
        <>
            <SearchingSelector<Site>
                queryKeyPrefix="site"
                tableName="Site"
                endpoint="/sites:search"
                item={props.site}
                setItem={props.setSite}
                display={display}
                displayRow={displayRow}
                submitNew={() => setShowSubmitModal(true)}
            />
            <SiteSubmissionModal show={showSubmitModal} onHide={() => setShowSubmitModal(false)} />
        </>
    );
}
