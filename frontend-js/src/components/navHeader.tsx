import React, { ReactElement, useContext } from 'react';
import { UserContext } from 'components/userContext';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import logo from 'assets/images/eosc-perf-logo.4.svg';
import { ModuleNavLink } from 'components/moduleNavLink';
import ResultSearchPage from 'pages/resultSearch';
import CodeGuidelinesPage from 'pages/codeGuidelines';
import ReportViewPage from 'pages/reportView';
import SiteSubmissionPage from 'pages/siteSubmission';
import BenchmarkSubmissionPage from 'pages/benchmarkSubmission';
import ResultSubmissionPage from 'pages/resultSubmission';
import SiteEditorPage from 'pages/siteEditor';
import { useAuth } from 'oidc-react';
import { Wrench } from 'react-bootstrap-icons';

export function NavHeader(props: { setCurrentTab: (tab: string) => void }): ReactElement {
    const auth = useContext(UserContext);
    const authentication = useAuth();

    return (
        <header>
            <Navbar bg="dark" expand="lg" variant="dark">
                <Navbar.Brand href={ResultSearchPage.path} className="ms-2">
                    <img src={logo} height="40" alt="EOSC-Performance" />
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <ModuleNavLink
                            reference={ResultSearchPage}
                            setCurrentTab={props.setCurrentTab}
                            className="nav-link"
                        />
                        <NavDropdown title="Submit" id="base-submit-dropdown">
                            <ModuleNavLink
                                reference={ResultSubmissionPage}
                                setCurrentTab={props.setCurrentTab}
                            />
                            <ModuleNavLink
                                reference={BenchmarkSubmissionPage}
                                setCurrentTab={props.setCurrentTab}
                            />
                            <ModuleNavLink
                                reference={SiteSubmissionPage}
                                setCurrentTab={props.setCurrentTab}
                            />
                        </NavDropdown>
                        <NavDropdown title="Instructions" id="base-instructions-dropdown">
                            <ModuleNavLink
                                reference={CodeGuidelinesPage}
                                setCurrentTab={props.setCurrentTab}
                            />
                        </NavDropdown>
                        {auth.admin && (
                            <NavDropdown title="Admin" id="base-admin-dropdown">
                                <ModuleNavLink
                                    reference={ReportViewPage}
                                    setCurrentTab={props.setCurrentTab}
                                />
                                <ModuleNavLink
                                    reference={SiteEditorPage}
                                    setCurrentTab={props.setCurrentTab}
                                />
                            </NavDropdown>
                        )}
                        <Nav.Link href="https://appsgrycap.i3m.upv.es:31443/im-dashboard/login">
                            Infrastructure Manager
                        </Nav.Link>
                    </Nav>
                    <Nav>
                        <NavDropdown
                            id="base-login-dropdown"
                            title={
                                <>
                                    {auth.name ?? 'Not logged in'}{' '}
                                    {auth.admin && (
                                        <div title="Administrator" style={{ display: 'inline' }}>
                                            <Wrench style={{ color: 'red' }} />
                                        </div>
                                    )}
                                </>
                            }
                            className="justify-content-end"
                        >
                            {auth.loggedIn ? (
                                <>
                                    <NavDropdown.Item onClick={() => authentication.signOut()}>
                                        Logout
                                    </NavDropdown.Item>
                                    {!auth.registered && (
                                        <NavDropdown.Item href="/register">
                                            Register
                                        </NavDropdown.Item>
                                    )}
                                </>
                            ) : (
                                <NavDropdown.Item onClick={() => authentication.signIn()}>
                                    Login
                                </NavDropdown.Item>
                            )}
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        </header>
    );
}
