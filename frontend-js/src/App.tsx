import React from 'react';
import { useState } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import './App.css';
import modules from './modules'; // All the parent knows is that it has modules ...
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { ModuleBase } from './modules/module-base';

function App() {
    const [currentTab, setCurrentTab] = useState('dashboard');

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
                to={page.routeProps.path}
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
                    <Navbar.Brand href={modules.BenchmarkSearch.routeProps.path}>
                        EOSC-Perf
                    </Navbar.Brand>
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
                            <NavDropdown id={'base-login-dropdown'} title={'Not logged in'}>
                                <NavDropdown.Item href={'/login'}>Login</NavDropdown.Item>
                            </NavDropdown>
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
            </header>
            <div className="App">
                <div className="App-content">
                    {modules.all.map((module) => (
                        <Route {...module.routeProps} key={module.name} />
                    ))}
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

/*
<header className="App-header">
                    <img src={logo} className="App-logo" alt="logo" />
                    <ul className="App-nav">
                        {modules.all.map(module => ( // with a name, and routes
                        <li key={module.name} className={currentTab === module.name ? 'active' : ''}>
                        <Link to={module.routeProps.path} onClick={() => setCurrentTab(module.name)}>{module.name}</Link>
                        </li>
                    ))}
                    </ul>
              </header>
              <div className="App-content">
                  {modules.all.map(module => (
                      <Route {...module.routeProps} key={module.name} />
                  ))}

              </div>
 */

export default App;
