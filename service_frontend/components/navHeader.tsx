import React, { ReactElement, useContext } from 'react';
import { UserContext } from 'components/userContext';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import logo from '../public/images/eosc-perf-logo.4.svg';
import { useAuth } from 'react-oidc-context';
import { Wrench } from 'react-bootstrap-icons';
import Link from 'next/link';
import Image from 'next/image';

/**
 * Navigation header rendered at the top of every page
 * @constructor
 */
export function NavHeader(): ReactElement {
    const auth = useContext(UserContext);
    const authentication = useAuth();

    return (
        <header>
            <Navbar bg="dark" expand="lg" variant="dark">
                <Navbar.Brand href="/" className="ms-4">
                    <Image src={logo} height={36} width={66} alt="EOSC-Performance" />
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Link href="/search/result" passHref>
                            <Nav.Link>Search</Nav.Link>
                        </Link>
                        <NavDropdown title="Submit" id="base-submit-dropdown">
                            <Link href="/submit/result" passHref>
                                <NavDropdown.Item>Results</NavDropdown.Item>
                            </Link>
                            <Link href="/submit/benchmark" passHref>
                                <NavDropdown.Item>Benchmarks</NavDropdown.Item>
                            </Link>
                            <Link href="/submit/site" passHref>
                                <NavDropdown.Item>Sites</NavDropdown.Item>
                            </Link>
                        </NavDropdown>
                        <NavDropdown title="Instructions" id="base-instructions-dropdown">
                            <Link href="/code-guidelines" passHref>
                                <NavDropdown.Item>Code guidelines</NavDropdown.Item>
                            </Link>
                        </NavDropdown>
                        <Link
                            href="https://appsgrycap.i3m.upv.es:31443/im-dashboard/login"
                            passHref
                        >
                            <Nav.Link>Infrastructure Manager</Nav.Link>
                        </Link>
                        {auth.admin && (
                            <NavDropdown title="Admin" id="base-admin-dropdown">
                                <Link href="/report-view" passHref>
                                    <NavDropdown.Item>Report view</NavDropdown.Item>
                                </Link>
                                <Link href="/site-editor" passHref>
                                    <NavDropdown.Item>Site editor</NavDropdown.Item>
                                </Link>
                            </NavDropdown>
                        )}
                    </Nav>
                    <Nav>
                        <NavDropdown
                            id="base-login-dropdown"
                            title={
                                <>
                                    {auth.email ?? 'Not logged in'}{' '}
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
                                    <NavDropdown.Item onClick={() => authentication.removeUser()}>
                                        Logout
                                    </NavDropdown.Item>
                                    {!auth.registered && (
                                        <NavDropdown.Item href="/register">
                                            Register
                                        </NavDropdown.Item>
                                    )}
                                </>
                            ) : (
                                <NavDropdown.Item onClick={() => authentication.signinRedirect()}>
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
