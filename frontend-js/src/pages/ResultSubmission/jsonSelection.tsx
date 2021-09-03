import React, { ChangeEvent, useState } from 'react';
import { Form, ProgressBar } from 'react-bootstrap';

export function JsonSelection(props: {
    fileContents?: string;
    setFileContents: (file?: string) => void;
}) {
    const [progress, setProgress] = useState(100.0);

    function loadFile(file?: File) {
        if (file === undefined) {
            props.setFileContents(undefined);
            return;
        }

        const reader = new FileReader();
        reader.addEventListener('load', (e) => {
            if (e.target && e.target.result) {
                // readAsText guarantees string
                props.setFileContents(e.target.result as string);
            } else {
                props.setFileContents(undefined);
            }
            setProgress(100.0);
        });
        reader.addEventListener('progress', (e) => {
            setProgress((e.loaded / e.total) * 100);
        });

        reader.readAsText(file);
    }

    return (
        <div>
            <Form.Group>
                <Form.Label>Please select result JSON file</Form.Label>
                <Form.Control
                    type="file"
                    onChange={(e: ChangeEvent<HTMLInputElement>) =>
                        loadFile(e.target.files ? e.target.files[0] : undefined)
                    }
                />
            </Form.Group>
            {progress !== 100.0 && <ProgressBar now={progress} label={`${progress}%`} />}
            {/* TODO: display result with formatting etc? */}
            {/*props.fileContents !== undefined ? props.fileContents : <div className="text-muted">No file loaded.</div>*/}
        </div>
    );
}
