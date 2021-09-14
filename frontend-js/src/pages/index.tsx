import ResultSearchModule from './ResultSearch';
import ResultSubmissionModule from './ResultSubmission';
import BenchmarkSubmissionModule from './BenchmarkSubmission';
import CodeGuidelinesModule from './CodeGuidelines';
import PrivacyPolicyModule from './PrivacyPolicy';
import ReportViewModule from './ReportView';
import SiteEditorModule from './SiteEditor';
import SiteSubmissionModule from 'pages/SiteSubmit';

export default {
    all: [
        ResultSearchModule,
        ResultSubmissionModule,
        BenchmarkSubmissionModule,
        SiteSubmissionModule,
        CodeGuidelinesModule,
        PrivacyPolicyModule,
        ReportViewModule,
        SiteEditorModule,
    ],
    ResultSearchModule,
    ResultSubmissionModule,
    BenchmarkSubmissionModule,
    SiteSubmissionModule,
    CodeGuidelinesModule,
    PrivacyPolicyModule,
    ReportViewModule,
    SiteEditorModule,
};
