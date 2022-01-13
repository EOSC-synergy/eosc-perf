import { ReactElement } from 'react';

/**
 * Dummy page for oidc-redirect route.
 *
 * Once react-oidc-context is done, the user is redirected to the home page.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function OidcRedirect(): ReactElement {
    return <>Logging you in...</>;
}

export default OidcRedirect;
