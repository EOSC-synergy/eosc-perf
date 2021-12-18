import React, { ReactElement, useContext } from 'react';
import { useQuery } from 'react-query';
import { getHelper } from 'components/api-helpers';
import { Claim } from 'model';
import { LoadingOverlay } from 'components/loadingOverlay';
import { ResultInfo } from 'components/reportView/resultInfo';
import { UserContext } from 'components/userContext';
import { truthyOrNoneTag } from 'components/utility';

export function ClaimInfo(props: { id: string }): ReactElement {
    const auth = useContext(UserContext);

    const claim = useQuery(
        ['claim', props.id],
        () => {
            return getHelper<Claim>('/reports/claims/' + props.id, auth.token);
        },
        {
            refetchOnWindowFocus: false // do not spam queries
        }
    );

    return (
        <>
            {claim.isLoading && <LoadingOverlay />}
            {claim.isSuccess && claim.data && (
                <>
                    Message: {truthyOrNoneTag(claim.data.data.message)} <br />
                    {claim.data.data.resource_type === 'result' && (
                        <ResultInfo id={claim.data.data.resource_id} />
                    )}
                </>
            )}
        </>
    );
}
