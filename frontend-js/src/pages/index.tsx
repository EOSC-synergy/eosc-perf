import ResultSearchModule from './ResultSearch';
import ResultSubmissionModule from './ResultSubmission';
import BenchmarkSubmissionModule from './BenchmarkSubmission';
import CodeGuidelinesModule from './CodeGuidelines';
import PrivacyPolicyModule from './PrivacyPolicy';
import ReportViewModule from './ReportView';
import SiteEditorModule from './SiteEditor';
import SiteSubmissionModule from 'pages/SiteSubmit';
import TermsOfServiceModule from 'pages/TermsOfService';
import RegistrationModule from 'pages/Registration';

const modules = {
    all: [
        ResultSearchModule,
        ResultSubmissionModule,
        BenchmarkSubmissionModule,
        SiteSubmissionModule,
        CodeGuidelinesModule,
        PrivacyPolicyModule,
        ReportViewModule,
        SiteEditorModule,
        TermsOfServiceModule,
        RegistrationModule,
    ],
    ResultSearchModule,
    ResultSubmissionModule,
    BenchmarkSubmissionModule,
    SiteSubmissionModule,
    CodeGuidelinesModule,
    PrivacyPolicyModule,
    ReportViewModule,
    SiteEditorModule,
    TermsOfServiceModule,
    RegistrationModule,
};

export default modules;
