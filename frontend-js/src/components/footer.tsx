import { Container } from 'react-bootstrap';
import { ModuleNavLink } from 'components/moduleNavLink';
import React from 'react';
import TermsOfServicePage from 'pages/termsOfService';
import PrivacyPolicyPage from 'pages/privacyPolicy';

export function Footer(props: { setCurrentTab: (tab: string) => void }) {
    return (
        <footer className="footer mt-auto py-3 bg-light">
            <Container>
                <div className="text-center text-md-center">
                    <ul className="list-unstyled list-inline my-0">
                        <li className="list-inline-item mx-5">
                            <ModuleNavLink
                                reference={TermsOfServicePage}
                                className="text-muted"
                                setCurrentTab={props.setCurrentTab}
                            />
                        </li>
                        <li className="list-inline-item mx-5">
                            <ModuleNavLink
                                reference={PrivacyPolicyPage}
                                className="text-muted"
                                setCurrentTab={props.setCurrentTab}
                            />
                        </li>
                        <li className="list-inline-item mx-5">
                            <a href="mailto:perf-support@lists.kit.edu" className="text-muted">
                                Email Support
                            </a>
                        </li>
                    </ul>
                </div>
            </Container>
        </footer>
    );
}
