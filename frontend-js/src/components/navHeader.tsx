import React, { useContext } from 'react';
import { UserContext } from 'userContext';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import modules from 'pages';
import logo from 'assets/images/eosc-perf-logo.4.svg';
import { ModuleNavLink } from 'components/moduleNavLink';

export function NavHeader(props: { setCurrentTab: (tab: string) => void }) {
    const auth = useContext(UserContext);

    return (
        <header>
            <Navbar bg="dark" expand="lg" variant="dark">
                <Navbar.Brand href={modules.ResultSearchModule.path} className="ms-2">
                    <img src={logo} height="40" alt="EOSC-Performance" />
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <ModuleNavLink
                            reference={modules.ResultSearchModule}
                            setCurrentTab={props.setCurrentTab}
                            className="nav-link"
                        />
                        <NavDropdown title="Submit" id="base-submit-dropdown">
                            <ModuleNavLink
                                reference={modules.ResultSubmissionModule}
                                setCurrentTab={props.setCurrentTab}
                            />
                            <ModuleNavLink
                                reference={modules.BenchmarkSubmissionModule}
                                setCurrentTab={props.setCurrentTab}
                            />
                            <ModuleNavLink
                                reference={modules.SiteSubmissionModule}
                                setCurrentTab={props.setCurrentTab}
                            />
                        </NavDropdown>
                        <NavDropdown title="Instructions" id="base-instructions-dropdown">
                            <ModuleNavLink
                                reference={modules.CodeGuidelinesModule}
                                setCurrentTab={props.setCurrentTab}
                            />
                        </NavDropdown>
                        {auth.admin && (
                            <NavDropdown title="Admin" id="base-admin-dropdown">
                                <ModuleNavLink
                                    reference={modules.ReportViewModule}
                                    setCurrentTab={props.setCurrentTab}
                                />
                                <ModuleNavLink
                                    reference={modules.SiteEditorModule}
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
                            title={auth.name ?? 'Not logged in'}
                            className="justify-content-end"
                        >
                            {auth.token ? (
                                <>
                                    <NavDropdown.Item href="/auth/logout">Logout</NavDropdown.Item>
                                    {!auth.registered && (
                                        <NavDropdown.Item href="/register">
                                            Register
                                        </NavDropdown.Item>
                                    )}
                                </>
                            ) : (
                                <NavDropdown.Item href="/auth/login">Login</NavDropdown.Item>
                            )}
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        </header>
    );
}
