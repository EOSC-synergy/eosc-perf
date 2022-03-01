import React from 'react';
import Link from 'next/link';

/**
 * Static footer component rendered at the bottom of every page
 * @constructor
 */
export function Footer() {
    return (
        <footer className="footer mt-auto py-3 bg-light">
            <div className="text-center">
                <ul className="list-unstyled list-inline my-0">
                    <li className="list-inline-item mx-5">
                        <Link href="/terms-of-service" passHref>
                            <a className="text-muted">Terms of service</a>
                        </Link>
                    </li>
                    <li className="list-inline-item mx-5">
                        <Link href="/privacy-policy" passHref>
                            <a className="text-muted">Privacy policy</a>
                        </Link>
                    </li>
                    <li className="list-inline-item mx-5">
                        <a href="mailto:perf-support@lists.kit.edu" className="text-muted">
                            Email Support
                        </a>
                    </li>
                </ul>
            </div>
        </footer>
    );
}
