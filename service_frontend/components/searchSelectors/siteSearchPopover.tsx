import { Site } from 'model';
import React, { ReactElement, useState } from 'react';
import { SiteSubmissionModal } from 'components/submissionModals/siteSubmissionModal';
import { SearchingSelector } from 'components/searchSelectors/index';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';

export function SiteSearchPopover(props: {
    site?: Site;
    initSite?: (site?: Site) => void;
    setSite: (site?: Site) => void;
    initialSiteId?: string;
}): ReactElement {
    useQuery(
        ['initial-site', props.initialSiteId],
        () => {
            return getHelper<Site>('/sites/' + props.initialSiteId);
        },
        {
            enabled: props.initialSiteId !== undefined,
            refetchOnWindowFocus: false, // do not spam queries
            onSuccess: (data) => {
                if (props.initSite) {
                    props.initSite(data.data);
                } else {
                    props.setSite(data.data);
                }
            },
        }
    );

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
                {site.name}
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
