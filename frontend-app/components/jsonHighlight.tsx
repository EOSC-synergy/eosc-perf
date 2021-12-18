import React, { ReactElement, useEffect } from 'react';

import prism from 'prismjs';
import 'prismjs/components/prism-json';

export function JsonHighlight(props: { children: React.ReactNode }): ReactElement {
    useEffect(() => {
        prism.highlightAll();
    }, []);
    return (<pre><code className='language-json'>{props.children}</code></pre>);
}