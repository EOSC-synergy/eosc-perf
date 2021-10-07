import React, { ReactElement, useContext } from 'react';
import { useQuery } from 'react-query';
import { getHelper } from 'api-helpers';
import { Claim } from 'api';
import { LoadingOverlay } from 'components/loadingOverlay';
import { ResultInfo } from 'pages/ReportView/resultInfo';
import { UserContext } from 'userContext';

export function ClaimInfo(props: { id: string }): ReactElement {
    const auth = useContext(UserContext);

    const claim = useQuery(
        'claim-' + props.id,
        () => {
            return getHelper<Claim>('/reports/claims/' + props.id, auth.token);
        },
        {
            refetchOnWindowFocus: false, // do not spam queries
        }
    );

    return (
        <>
            {claim.isLoading && <LoadingOverlay />}
            {claim.isSuccess && claim.data && (
                <>
                    Message: {claim.data.data.message} <br />
                    {claim.data.data.resource_type === 'result' && (
                        <ResultInfo id={claim.data.data.resource_id} />
                    )}
                </>
            )}
        </>
    );
}
