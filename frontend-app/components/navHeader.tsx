import React, { ReactElement, useContext } from 'react';
import { UserContext } from 'components/userContext';
import { Nav, Navbar, NavDropdown } from 'react-bootstrap';
import logo from '../public/images/eosc-perf-logo.4.svg';
import { useAuth } from 'react-oidc-context';
import { Wrench } from 'react-bootstrap-icons';
import Link from 'next/link';
import Image from 'next/image';

export function NavHeader(props: {}): ReactElement {
    const auth = useContext(UserContext);
    const authentication = useAuth();

    return (
        <header>
            <Navbar bg='dark' expand='lg' variant='dark'>
                <Navbar.Brand href='/' className='ms-2'>
                    <Image src={logo} height='40' alt='EOSC-Performance' />
                </Navbar.Brand>
                <Navbar.Toggle aria-controls='basic-navbar-nav' />
                <Navbar.Collapse id='basic-navbar-nav'>
                    <Nav className='me-auto'>
                        <Link href='/resultSearch' passHref>
                            <Nav.Link>
                                Search
                            </Nav.Link>
                        </Link>
                        <NavDropdown title='Submit' id='base-submit-dropdown'>
                            <Link href='/resultSubmission' passHref>
                                <NavDropdown.Item>
                                    Results
                                </NavDropdown.Item>
                            </Link>
                            <Link href='/benchmarkSubmission' passHref>
                                <NavDropdown.Item>
                                    Benchmarks
                                </NavDropdown.Item>
                            </Link>
                            <Link href='/siteSubmission' passHref>
                                <NavDropdown.Item>
                                    Sites
                                </NavDropdown.Item>
                            </Link>
                        </NavDropdown>
                        <NavDropdown title='Instructions' id='base-instructions-dropdown'>
                            <Link href='/codeGuidelines' passHref>
                                <NavDropdown.Item>
                                    Code guidelines
                                </NavDropdown.Item>
                            </Link>
                        </NavDropdown>
                        {auth.admin && (
                            <NavDropdown title='Admin' id='base-admin-dropdown'>
                                <Link href='/reportView' passHref>
                                    <NavDropdown.Item>
                                        Report view
                                    </NavDropdown.Item>
                                </Link>
                                <Link href='/siteEditor' passHref>
                                    <NavDropdown.Item>
                                        Site editor
                                    </NavDropdown.Item>
                                </Link>
                            </NavDropdown>
                        )}
                        <Link href='https://appsgrycap.i3m.upv.es:31443/im-dashboard/login' passHref>
                            <Nav.Link>
                                Infrastructure Manager
                            </Nav.Link>
                        </Link>
                    </Nav>
                    <Nav>
                        <NavDropdown
                            id='base-login-dropdown'
                            title={
                                <>
                                    {auth.email ?? 'Not logged in'}{' '}
                                    {auth.admin && (
                                        <div title='Administrator' style={{ display: 'inline' }}>
                                            <Wrench style={{ color: 'red' }} />
                                        </div>
                                    )}
                                </>
                            }
                            className='justify-content-end'
                        >
                            {auth.loggedIn ? (
                                <>
                                    <NavDropdown.Item onClick={() => authentication.removeUser()}>
                                        Logout
                                    </NavDropdown.Item>
                                    {!auth.registered && (
                                        <NavDropdown.Item href='/register'>
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
