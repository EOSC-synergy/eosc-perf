import React, { ReactElement } from 'react';
import { Container } from 'react-bootstrap';
import Head from 'next/head';

/**
 * Page containing the privacy policy.
 *
 * @returns {React.ReactElement}
 * @constructor
 */
function PrivacyPolicy(): ReactElement {
    return (
        <>
            <Head>
                <title>Privacy Policy</title>
            </Head>
            <Container>
                <h1>Privacy Policy</h1>
                This privacy policy for the EOSC benchmark collection service is valid as of
                September 2020.
                <h2>Service</h2>
                The EOSC benchmark collection service (in the following referred to as the Service)
                allows users to collect, share, compare and download benchmark results for the
                European Open Science Cloud (EOSC).
                <h2>Jurisdiction and supervisory authority</h2>
                <ul>
                    <li>
                        <p>
                            <a href="https://www.bfdi.bund.de/DE/Home/home_node.html">German DPA</a>
                            . Details for raising concerns for the German DPA can be found{' '}
                            <a href="https://www.bfdi.bund.de/DE/Service/Datenschutzerklaerung/datenschutzerklaerung-node.html">
                                here
                            </a>
                            .
                        </p>
                    </li>
                    <li>
                        <p>
                            <a href="https://www.baden-wuerttemberg.datenschutz.de/">
                                Baden-W&uuml;rttemberg DPA
                            </a>
                            .{' '}
                            <a href="https://www.baden-wuerttemberg.datenschutz.de/online-beschwerde/">
                                Link
                            </a>{' '}
                            to file a complaint.
                        </p>
                    </li>
                </ul>
                <h2>Personal data</h2>
                The Service collects three categories of personally identifiable data (in the
                following collectively the Personal Data):
                <br />
                A. Personal data retrieved from your Home Organisation:
                <ul>
                    <li>
                        Your unique user identifier (provided by the EGI Check-In system) if you
                        have signed in
                    </li>
                    <li>Your role in your Home Organisation (eduPersonAffiliation attribute)</li>
                    <li>Your full name</li>
                    <li>Your e-mail address</li>
                </ul>
                B. Personal data collected by the Service required for normal operation
                <ul>
                    <li>Logfiles on the Service activity</li>
                </ul>
                C. Personal data collected by the Service that you provide
                <ul>
                    <li>Benchmark results uploaded by you</li>
                    <li>Reports about you create inaccurate benchmark results</li>
                    <li>New sites and benchmark tools submitted by you</li>
                </ul>
                <h2>Purposes for processing data</h2>
                Logs are retained and processed for the purposes of error resolution as well as
                performance evaluation. Your mail address and full name are stored for the purpose
                of handling reports you file and attributing results you upload.
                <h2>Access, correction and deletion of data</h2>
                If you wish to have your Personal Data collected by the Service deleted or changed,
                please collect the Data Protection Officer at{' '}
                <a href="mailto:perf-support@lists.kit.edu" className="uri">
                    perf-support@lists.kit.edu
                </a>
                . If you wish to correct inaccurate data provided by your Home Organisation, please
                contact their IT help desk.
                <h2>Withdrawal of consent</h2>
                If you wish to withdraw your consent with regard to processing your user-provided
                Personal Data, please contact the Data Protection Officer at{' '}
                <a href="mailto:perf-support@lists.kit.edu" className="uri">
                    perf-support@lists.kit.edu
                </a>{' '}
                to have it deleted from the Service. Note that your results are still subject to the
                license you agreed to and as such may be retained and only have your personal
                information removed.
                <h2>Data retention</h2>
                Uploader information associated with user-provided content is retained indefinitely
                and only deleted at user request. Note that IP data is stored inside log files for
                indefinitely time in order to perform performance and security checks.
                <h2>Data Protection Code of Conduct</h2>
                Your Personal Data will be protected according to the Code of Conduct for Service
                Providers, a common standard for the research and higher education sector to protect
                your privacy.
                <h2 id="contact-information">Contact information</h2>
                <p>
                    Service managers:{' '}
                    <a href="mailto:perf-support@lists.kit.edu" className="uri">
                        perf-support@lists.kit.edu
                    </a>
                </p>
                <p>
                    Data controller:{' '}
                    <a href="mailto:perf-support@lists.kit.edu" className="uri">
                        perf-support@lists.kit.edu
                    </a>
                </p>
            </Container>
        </>
    );
}

export default PrivacyPolicy;
