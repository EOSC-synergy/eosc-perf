import React, { ReactNode, useEffect, useState } from 'react';
import CookieConsent, { getCookieConsentValue } from 'react-cookie-consent';
import ReactGA from 'react-ga';

export function AnalyticsWrapper(props: { children: ReactNode }) {
    const [cookieConsent, setCookieConsent] = useState(getCookieConsentValue());

    useEffect(() => {
        if (cookieConsent === 'true' && process.env.REACT_APP_GOOGLE_ANALYTICS) {
            ReactGA.pageview(window.location.pathname + window.location.search);
        }
    });

    function initializeGA() {
        if (process.env.REACT_APP_GOOGLE_ANALYTICS) {
            ReactGA.initialize(process.env.REACT_APP_GOOGLE_ANALYTICS);
        }
    }

    if (cookieConsent === 'true') {
        initializeGA();
    }

    return (
        <>
            <CookieConsent
                enableDeclineButton
                onAccept={() => {
                    initializeGA();
                    setCookieConsent('true');
                }}
                onDecline={() => setCookieConsent('false')}
            >
                This website optionally uses cookies to collect anonymized statistics.
            </CookieConsent>
            {props.children}
        </>
    );
}
