/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type User = {
    /**
     * String containing an OIDC subject
     */
    sub: string;
    /**
     * String containing an OIDC issuer
     */
    iss: string;
    /**
     * Email of user collected by the OIDC token
     */
    email: string;
    /**
     * Time when the user was registered
     */
    registration_datetime: string;
};
