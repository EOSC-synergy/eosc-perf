/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type User = {
    /**
     * String containing an OIDC subject
     */
    readonly sub: string;
    /**
     * String containing an OIDC issuer
     */
    readonly iss: string;
    /**
     * Email of user collected by the OIDC token
     */
    email: string;
    created_at: string;
}
