import React, { useState } from 'react';
import './App.css';

// styling
import 'bootstrap/dist/css/bootstrap.min.css';
import './main.css';

// app-switching
import { Redirect } from 'react-router';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import modules from './modules'; // All the parent knows is that it has modules ...
import { ModuleBase } from './modules/module-base';
import Switch from 'react-bootstrap/Switch';

// html
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';

// data fetch
import axios from 'axios';
import { QueryClient, QueryClientProvider, useQuery } from 'react-query';

const queryClient = new QueryClient();

type UserInfo = {
    token: string;
    email: string;
    name: string;
    admin: boolean;
};

function App() {
    // state
    const [currentTab, setCurrentTab] = useState('BenchmarkSearch');

    const { status, isLoading, isError, data, isSuccess } = useQuery(
        'userInfo',
        () => axios.get<UserInfo>('https://localhost/auth/whoami'),
        {
            retry: false,
        }
    );

    // const auth = useAuth();

    /**
     * Create navbar-dropdown button for a subpage
     * @param props { reference: reference to module to link to }
     * @constructor
     *
     * Notes: cannot use <NavDropdown.Item> due to <Link>, dropdown-item class added manually
     */
    function LinkTo(props: { reference: ModuleBase; className?: string }) {
        return (
            <Link
                to={props.reference.path}
                onClick={() => setCurrentTab(props.reference.name)}
                className={props.className ? props.className : 'dropdown-item'}
            >
                {props.reference.dropdownName}
            </Link>
        );
    }

    return (
        <Router>
            <header>
                <Navbar bg="dark" expand={'lg'} variant={'dark'}>
                    <Navbar.Brand href={modules.BenchmarkSearch.path}>
                        <img src="/images/eosc-perf-logo.svg" height="40" alt="EOSC-Performance" />
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className={'mr-auto'}>
                            <NavDropdown title={'Search'} id={'base-search-dropdown'}>
                                <LinkTo reference={modules.BenchmarkSearch} />
                                <LinkTo reference={modules.ResultSearch} />
                            </NavDropdown>
                            <NavDropdown title={'Submit'} id={'base-submit-dropdown'}>
                                <LinkTo reference={modules.ResultSubmission} />
                                <LinkTo reference={modules.BenchmarkSubmission} />
                            </NavDropdown>
                            <NavDropdown title={'Instructions'} id={'base-instructions-dropdown'}>
                                <LinkTo reference={modules.CodeGuidelines} />
                            </NavDropdown>
                            {data && data.data.admin && (
                                <NavDropdown title={'Admin'} id={'base-admin-dropdown'}>
                                    <LinkTo reference={modules.ReportViewModule} />
                                    <LinkTo reference={modules.SiteEditorModule} />
                                </NavDropdown>
                            )}
                            <Nav.Link
                                href={'https://appsgrycap.i3m.upv.es:31443/im-dashboard/login'}
                            >
                                Infrastructure Manager
                            </Nav.Link>
                        </Nav>
                        <Nav>
                            <NavDropdown
                                id={'base-login-dropdown'}
                                title={isSuccess ? data?.data.name : 'Not logged in.'}
                                className="justify-content-end"
                            >
                                {isSuccess ? (
                                    <NavDropdown.Item href={'/auth/logout'}>
                                        Logout
                                    </NavDropdown.Item>
                                ) : (
                                    <NavDropdown.Item href={'/auth/login'}>Login</NavDropdown.Item>
                                )}
                            </NavDropdown>
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
            </header>
            <div className="App">
                <div className="App-content">
                    <Switch>
                        <Route exact path="/">
                            <Redirect to={modules.BenchmarkSearch.path} />
                        </Route>
                        {modules.all.map((module) => (
                            <Route
                                path={module.path}
                                render={(props) => (
                                    // @ts-ignore
                                    <module.element
                                        {...props}
                                        {...{
                                            token: data?.data.token,
                                            admin: data?.data.admin,
                                        }}
                                    />
                                )}
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
        </Router>
    );
}

const hof = (WrappedComponent: any) => {
    // Its job is to return a react component warpping the baby component
    return (props: {}) => (
        <QueryClientProvider client={queryClient}>
            <WrappedComponent {...props} />
        </QueryClientProvider>
    );
};
export default hof(App);
