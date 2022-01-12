/* This script transforms the npm audit json output into another json ready for
   the Jenkins Warnings Next Generation plugin.
   = Very much based on = :
   [1] https://github.com/Uko/NPM-Audit-to-Warnings-NG
   READ (Update [1] with [2] as the output format changed!!!):
   [2] https://uko.codes/dealing-with-npm-v7-audit-changes
   [3] https://uko.codes/npm-audit-jenkins-warnings-next-generation-native-json-format (FYI)
   
   Within Jenkins use as e.g.:
   npm audit --json | node transform-audit.js > issues.json
*/

let data = '';
process.stdin.setEncoding('utf8');
process.stdin.on('readable', () => {
    let chunk = process.stdin.read();
    if (chunk !== null) {
        data += chunk;
    }
});

function warningsNGSeverity(string) {
    switch (string) {
        case 'low': return 'LOW';
        case 'moderate': return 'NORMAL';
        case 'high': return 'HIGH';
        case 'critical': return 'ERROR';

        default: return 'NORMAL';
    }
}

process.stdin.on('end', () => {

    const auditJSON = JSON.parse(data);
    

    const issues = Object.values(auditJSON.vulnerabilities).map((vulnerability) => {
        const advisories = vulnerability.via.filter((item) => typeof item === 'object');
        const isAdvisory = advisories.length > 0;

        return {
            fileName: vulnerability.name,
            packageName: isAdvisory ? 'advisory' : 'derived',
            type: vulnerability.fixAvailable ? 'autofixable' : 'non-autofixable',
            message: isAdvisory ? advisories.map((adv) => adv.title).join(' and ') : '',
            description: isAdvisory ? `nodes: ${vulnerability.nodes.join(', ')} <br> See: ${advisories.map((adv) => adv.url).join(' and ')}` : `nodes: ${vulnerability.nodes.join(', ')}`,
            severity: warningsNGSeverity(vulnerability.severity)
        };
    });

    console.log(JSON.stringify({ issues: issues }));
});
