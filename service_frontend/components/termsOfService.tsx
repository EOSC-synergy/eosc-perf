import Link from 'next/link';
import React from 'react';

export function TermsOfService() {
    return (
        <>
            <h1>Acceptable Use Policy and Conditions of Use</h1>
            <p>
                This policy for the EOSC benchmark collection service is valid as of October 2021.
            </p>
            <p>
                This Acceptable Use Policy and Conditions of Use (“AUP”) defines the rules and
                conditions that govern your access to and use (including transmission, processing,
                and storage of data) of the resources and services (“Services”) as granted by the
                department{' '}
                <a href="https://www.scc.kit.edu/en/aboutus/d3a.php">
                    Data Analytics, Access and Applications
                </a>{' '}
                (D3A) from the{' '}
                <a href="https://www.scc.kit.edu/en/">Steinbuch Centre for Computing</a> (SCC) of{' '}
                <a href="https://www.kit.edu/english/index.php">
                    Karlsruhe Institute of Technology
                </a>{' '}
                (KIT), located at Hermann-von-Helmholtz-Platz 1, 76344 Eggenstein-Leopoldshafen (the
                “Provider”) for the purpose of uploading, retrieving and comparing results from
                benchmarks for diverse computing resources.
            </p>

            <ol>
                <li>
                    You shall only use the Services in a manner consistent with the purposes and
                    limitations described above; you shall show consideration towards other users
                    including by not causing harm to the Services; you have an obligation to
                    collaborate in the resolution of issues arising from your use of the Services.
                </li>
                <li>
                    You shall only use the Services for lawful purposes and not breach, attempt to
                    breach, nor circumvent administrative or security controls.
                </li>
                <li>
                    You shall respect intellectual property and confidentiality agreements, e.g.:
                </li>
                <ol type="a">
                    <li>
                        You are solely responsible for the content of, and for any harm resulting
                        from, any content created or uploaded by you (&quot;Content&quot;) to the
                        Services.
                    </li>
                    <li>
                        You agree that you will only submit Content that you have the right to post;
                        and that you will fully comply with any third party licenses relating to
                        Content you post.
                    </li>
                    <li>Any Content you post publicly may be viewed by others.</li>
                    <li>
                        You grant us and our legal successors the right to store, archive, parse,
                        and display Your Content, and make incidental copies, as necessary to
                        provide the Service, including improving the Service over time.
                    </li>
                    <li>
                        We have the right to refuse or remove any Content that, in our sole
                        discretion, violates any laws or our Privacy policy.
                    </li>
                </ol>
                <li>
                    You shall protect your access credentials (e.g. passwords, private keys or
                    multi-factor tokens); no intentional sharing is permitted.
                </li>
                <li>You shall keep your registered information correct and up to date.</li>
                <li>
                    You shall promptly report known or suspected security breaches, credential
                    compromise, or misuse to the security contact stated below; and report any
                    compromised credentials to the relevant issuing authorities.
                </li>
                <li>
                    Reliance on the Services shall only be to the extent specified by any applicable
                    service level agreements listed below. Use without such agreements is at your
                    own risk.
                </li>
                <li>
                    Your personal data will be processed in accordance with the privacy statements
                    referenced below.
                </li>
                <li>
                    Your use of the Services may be restricted or suspended, for administrative,
                    operational, or security reasons, without prior notice and without compensation.
                </li>
                <li>
                    If you violate these rules, you may be liable for the consequences, which may
                    include your account being suspended and a report being made to your home
                    organisation or to law enforcement.
                </li>
            </ol>

            <h2>Contact information</h2>
            <p>
                The administrative contact for this AUP is:{' '}
                <a href="mailto:perf-support@lists.kit.edu">perf-support@lists.kit.edu</a>
            </p>
            <p>
                The security contact for this AUP is:{' '}
                <a href="mailto:scc-secteam@lists.kit.edu">scc-secteam@lists.kit.edu</a>
            </p>
            <p>
                The privacy statements (e.g. Privacy Notices) are located at:{' '}
                <Link href="/privacy-policy">Privacy Policy</Link>
            </p>
            <p>
                The KIT Impressum is found here: <a href="https://www.kit.edu/legals.php">Legals</a>
            </p>
        </>
    );
}
