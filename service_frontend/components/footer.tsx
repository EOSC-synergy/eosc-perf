import { Container } from 'react-bootstrap';
import React from 'react';
import Link from 'next/link';

export function Footer() {
    return (
        <footer className='footer mt-auto py-3 bg-light'>
            <Container>
                <div className='text-center text-md-center'>
                    <ul className='list-unstyled list-inline my-0'>
                        <li className='list-inline-item mx-5'>
                            <div className='text-muted'><Link href='/terms-of-service'>Terms of service</Link></div>
                        </li>
                        <li className='list-inline-item mx-5'>
                            <div className='text-muted'><Link href='/privacy-policy'>Privacy policy</Link></div>
                        </li>
                        <li className='list-inline-item mx-5'>
                            <a
                                href='mailto:perf-support@lists.kit.edu'
                                className='text-muted'
                            >
                                Email Support
                            </a>
                        </li>
                    </ul>
                </div>
            </Container>
        </footer>
    );
}
