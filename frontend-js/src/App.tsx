import React, { ReactElement, useContext, useState } from 'react';
import './App.css';

// styling
import 'bootstrap/dist/css/bootstrap.min.css';
import './main.css';

// app-switching
import { Redirect } from 'react-router';
import { BrowserRouter as Router, NavLink, Route } from 'react-router-dom';
import modules from './pages'; // All the parent knows is that it has modules ...
import { PageBase } from 'pages/pageBase';
import Switch from 'react-bootstrap/Switch';

// html
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';

// data fetch
import axios from 'axios';
import { QueryClient, QueryClientProvider, useQuery } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { emptyUser, UserContext, UserInfo } from 'userContext';

import logo from './assets/images/eosc-perf-logo.svg';

const queryClient = new QueryClient();

/**
 * Create navbar-dropdown button for a subpage
 * @param props { reference: reference to module to link to }
 * @constructor
 *
 * Notes: cannot use <NavDropdown.Item> due to <Link>, dropdown-item class added manually
 */
function LinkTo(props: {
    reference: PageBase;
    className?: string;
    setCurrentTab: (tab: string) => void;
}) {
    return (
        <NavLink
            to={props.reference.path}
            onClick={() => props.setCurrentTab(props.reference.name)}
            className={props.className ? props.className : 'dropdown-item'}
        >
            {props.reference.displayName}
        </NavLink>
    );
}

function NavHeader(props: { setCurrentTab: (tab: string) => void }) {
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
                        <LinkTo
                            reference={modules.ResultSearchModule}
                            setCurrentTab={props.setCurrentTab}
                            className="nav-link"
                        />
                        <NavDropdown title="Submit" id="base-submit-dropdown">
                            <LinkTo
                                reference={modules.ResultSubmissionModule}
                                setCurrentTab={props.setCurrentTab}
                            />
                            <LinkTo
                                reference={modules.BenchmarkSubmissionModule}
                                setCurrentTab={props.setCurrentTab}
                            />
                            <LinkTo
                                reference={modules.SiteSubmissionModule}
                                setCurrentTab={props.setCurrentTab}
                            />
                        </NavDropdown>
                        <NavDropdown title="Instructions" id="base-instructions-dropdown">
                            <LinkTo
                                reference={modules.CodeGuidelinesModule}
                                setCurrentTab={props.setCurrentTab}
                            />
                        </NavDropdown>
                        {auth.admin && (
                            <NavDropdown title="Admin" id="base-admin-dropdown">
                                <LinkTo
                                    reference={modules.ReportViewModule}
                                    setCurrentTab={props.setCurrentTab}
                                />
                                <LinkTo
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
                            title={auth.name || 'Not logged in.'}
                            className="justify-content-end"
                        >
                            {auth.token ? (
                                <NavDropdown.Item href="/auth/logout">Logout</NavDropdown.Item>
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

function App() {
    // state
    const [currentTab, setCurrentTab] = useState('BenchmarkSearch');

    const whoAmI = useQuery('userInfo', () => axios.get<UserInfo>('/auth/whoami'), {
        retry: false,
    });

    return (
        <UserContext.Provider value={whoAmI.isSuccess ? whoAmI.data.data : emptyUser}>
            <Router>
                <NavHeader setCurrentTab={setCurrentTab} />
                <div className="App">
                    <div className="App-content">
                        <Switch>
                            <Route exact path="/">
                                <Redirect to={modules.ResultSearchModule.path} />
                            </Route>
                            {modules.all.map((module) => (
                                <Route
                                    path={module.path}
                                    render={(props) => <module.element />}
                                    key={module.name}
                                />
                            ))}
                        </Switch>
                    </div>
                </div>
                <footer className="footer mt-auto py-3 bg-light">
                    <Container>
                        <div className="text-center text-md-center">
                            <ul className="list-unstyled list-inline my-0">
                                <li className="list-inline-item mx-5">
                                    <LinkTo
                                        reference={modules.PrivacyPolicyModule}
                                        className="text-muted"
                                        setCurrentTab={setCurrentTab}
                                    />
                                </li>
                                <li className="list-inline-item mx-5">
                                    <a
                                        href="mailto:perf-support@lists.kit.edu"
                                        className="text-muted"
                                    >
                                        Email Support
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </Container>
                </footer>
            </Router>
        </UserContext.Provider>
    );
}

const hof = (WrappedComponent: (props: Record<string, unknown>) => ReactElement) => {
    return function WrappedApp(props: Record<string, unknown>) {
        return (
            <QueryClientProvider client={queryClient}>
                <WrappedComponent {...props} />
                <ReactQueryDevtools />
            </QueryClientProvider>
        );
    };
};
export default hof(App);
