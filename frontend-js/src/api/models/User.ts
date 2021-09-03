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
    /**
     * ISO8601 Datatime of the resource upload
     */
    upload_datetime: string;
}
