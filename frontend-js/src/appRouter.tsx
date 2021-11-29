import React, { useState } from 'react';

// styling
import 'bootstrap/dist/css/bootstrap.min.css';
import './main.css';

// app-switching
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Switch from 'react-bootstrap/Switch';

// data fetch
import { Footer } from 'components/footer';
import { NavHeader } from 'components/navHeader';
import { QueryClientWrapper } from 'components/queryClientWrapper';
import BenchmarkSubmissionPage from 'pages/benchmarkSubmission';
import CodeGuidelinesPage from 'pages/codeGuidelines';
import ResultSearchPage from 'pages/resultSearch';
import PrivacyPolicyPage from 'pages/privacyPolicy';
import RegistrationPage from 'pages/registration';
import ReportViewPage from 'pages/reportView';
import ResultSubmissionPage from 'pages/resultSubmission';
import SiteEditorPage from 'pages/siteEditor';
import SiteSubmissionPage from 'pages/siteSubmission';
import TermsOfServicePage from 'pages/termsOfService';

import { AuthProvider } from 'oidc-react';
import { UserContextWrapper } from 'components/userContextWrapper';
import { AuthProviderProps } from 'oidc-react/build/src/AuthContextInterface';

const oidcConfig: AuthProviderProps = {
    authority:
        process.env.NODE_ENV === 'development'
            ? 'https://aai-dev.egi.eu/oidc/'
            : 'https://aai.egi.eu/oidc/',
    onSignIn: async () => {
        // TODO: can we do this with react-router to avoid reload?
        window.location.href = '/';
    },
    clientId: process.env.REACT_APP_OIDC_CLIENT_ID,
    redirectUri: window.location.protocol + '//' + window.location.host + '/oidc-redirect',
    scope: 'openid email profile eduperson_entitlement offline_access',
    autoSignIn: false,
    responseType: 'code',
};

function AppRouter() {
    // state
    const [currentTab, setCurrentTab] = useState('BenchmarkSearch');

    return (
        <Router>
            <NavHeader setCurrentTab={setCurrentTab} />
            <div className="my-3">
                <Switch>
                    <Route exact path="/" component={ResultSearchPage.component} />
                    <Route
                        path={BenchmarkSubmissionPage.path}
                        component={BenchmarkSubmissionPage.component}
                    />
                    <Route
                        path={CodeGuidelinesPage.path}
                        component={CodeGuidelinesPage.component}
                    />
                    <Route path={PrivacyPolicyPage.path} component={PrivacyPolicyPage.component} />
                    <Route path={RegistrationPage.path} component={RegistrationPage.component} />
                    <Route path={ReportViewPage.path} component={ReportViewPage.component} />
                    <Route path={ResultSearchPage.path} component={ResultSearchPage.component} />
                    <Route
                        path={ResultSubmissionPage.path}
                        component={ResultSubmissionPage.component}
                    />
                    <Route path={SiteEditorPage.path} component={SiteEditorPage.component} />
                    <Route
                        path={SiteSubmissionPage.path}
                        component={SiteSubmissionPage.component}
                    />
                    <Route
                        path={TermsOfServicePage.path}
                        component={TermsOfServicePage.component}
                    />
                </Switch>
            </div>
            <Footer setCurrentTab={setCurrentTab} />
        </Router>
    );
}

export default (
    <QueryClientWrapper>
        <AuthProvider {...oidcConfig}>
            <UserContextWrapper>
                <AppRouter />
            </UserContextWrapper>
        </AuthProvider>
    </QueryClientWrapper>
);
