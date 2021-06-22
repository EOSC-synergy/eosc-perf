import React, { useState } from 'react';
import './App.css';

// styling
import 'bootstrap/dist/css/bootstrap.min.css';
import './main.css';

// app-switching
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import modules from './modules'; // All the parent knows is that it has modules ...
import { ModuleBase } from './modules/module-base';
import Switch from 'react-bootstrap/Switch';

// html
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';

// data fetch
import axios from 'axios';
import { QueryClient, QueryClientProvider, useQuery } from 'react-query';

const queryClient = new QueryClient();

type UserInfo = {
    token: string;
    email: string;
    name: string;
};

function App() {
    // state
    const [currentTab, setCurrentTab] = useState('BenchmarkSearch');

    const { status, isLoading, isError, data, isSuccess } = useQuery('userInfo', () =>
        axios.get<UserInfo>('https://localhost/auth/whoami')
    );

    // const auth = useAuth();

    /**
     * Create navbar-dropdown button for a subpage
     * @param page target page
     * @returns {JSX.Element} JSX Element to display
     * @constructor
     *
     * Notes: cannot use <NavDropdown.Item> due to <Link>, dropdown-item class added manually
     */
    function LinkTo(page: ModuleBase) {
        return (
            <Link
                to={page.path}
                onClick={() => setCurrentTab(page.name)}
                className={'dropdown-item'}
            >
                {page.dropdownName}
            </Link>
        );
    }

    return (
        <Router>
            <header>
                <Navbar bg="dark" expand={'lg'} variant={'dark'}>
                    <Navbar.Brand href={modules.BenchmarkSearch.path}>EOSC-Perf</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className={'mr-auto'}>
                            <NavDropdown title={'Search'} id={'base-search-dropdown'}>
                                {LinkTo(modules.BenchmarkSearch)}
                                {LinkTo(modules.ResultSearch)}
                            </NavDropdown>
                            <NavDropdown title={'Submit'} id={'base-submit-dropdown'}>
                                {LinkTo(modules.ResultSubmission)}
                                {LinkTo(modules.BenchmarkSubmission)}
                            </NavDropdown>
                            <NavDropdown title={'Instructions'} id={'base-instructions-dropdown'}>
                                {LinkTo(modules.CodeGuidelines)}
                            </NavDropdown>
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
                        {modules.all.map((module) => (
                            <Route
                                path={module.path}
                                render={(props) => (
                                    // @ts-ignore
                                    <module.element {...props} {...{ token: data?.data.token }} />
                                )}
                                key={module.name}
                            />
                        ))}
                    </Switch>
                </div>
            </div>
            <footer className="footer mt-auto py-3 bg-light">
                <div className="container text-center text-md-center">
                    <ul className="list-unstyled list-inline my-0">
                        <li className="list-inline-item mx-5">
                            <a href="/privacy_policy" className="text-muted">
                                Privacy Policy
                            </a>
                        </li>
                        <li className="list-inline-item mx-5">
                            <a href="mailto:perf-support@lists.kit.edu" className="text-muted">
                                Email Support
                            </a>
                        </li>
                    </ul>
                </div>
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
