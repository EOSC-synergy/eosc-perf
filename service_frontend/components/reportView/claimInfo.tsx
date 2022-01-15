import React, { ReactElement, useContext } from 'react';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { Claim } from 'model';
import { LoadingOverlay } from 'components/loadingOverlay';
import { ResultInfo } from 'components/reportView/resultInfo';
import { UserContext } from 'components/userContext';
import { truthyOrNoneTag } from 'components/utility';
import { Badge } from 'react-bootstrap';

export function ClaimInfo(props: { id?: string; claim?: Claim }): ReactElement {
    const auth = useContext(UserContext);

    const claim = useQuery(
        ['claim', props.id],
        () => {
            return getHelper<Claim>('/reports/claims/' + props.id, auth.token);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
            enabled: props.claim === undefined,
        }
    );

    // use local copy if available
    let claimData: Claim | undefined = props.claim;
    if (props.claim === undefined) {
        if (props.id !== undefined && claim.isSuccess && claim.data) {
            claimData = claim.data.data;
        }
    }

    return (
        <>
            {props.id === undefined && props.claim === undefined && (
                <Badge bg="danger">No claim data available</Badge>
            )}
            {claim.isLoading && <LoadingOverlay />}
            {claim.isSuccess && claimData && (
                <>
                    Message: {truthyOrNoneTag(claimData.message)} <br />
                    Claimant: {claimData.uploader.email} <br />
                    {claimData.resource_type === 'result' && (
                        <ResultInfo id={claimData.resource_id} />
                    )}
                </>
            )}
        </>
    );
}
