import React, { ReactElement, ReactNode, useContext, useState } from 'react';
import { JsonSelection } from 'components/jsonSelection';
import { Alert, Button, Col, Form, Row } from 'react-bootstrap';
import { UserContext } from 'components/userContext';
import { useMutation } from 'react-query';
import { Benchmark, Flavor, Result, Site, Tag } from 'model';
import { postHelper } from 'components/api-helpers';
import { AxiosError } from 'axios';
import { SiteSearchPopover } from 'components/searchSelectors/siteSearchPopover';
import { BenchmarkSearchSelect } from 'components/searchSelectors/benchmarkSearchSelect';
import { FlavorSearchSelect } from 'components/searchSelectors/flavorSearchSelect';
import { getErrorMessage } from 'components/forms/getErrorMessage';

import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { RegistrationCheck } from 'components/registrationCheck';
import TagSelector from 'components/tagSelector';
import { LoginCheck } from '../loginCheck';
import { LoadingWrapper } from '../loadingOverlay';

export function ResultSubmitForm(props: {
    onSuccess: () => void;
    onError: () => void;
}): ReactElement {
    const auth = useContext(UserContext);

    const [benchmark, setBenchmark] = useState<Benchmark | undefined>(undefined);
    const [site, setSite] = useState<Site | undefined>(undefined);
    const [flavor, setFlavor] = useState<Flavor | undefined>(undefined);
    const [tags, setTags] = useState<Tag[]>([]);

    const [fileContents, setFileContents] = useState<string | undefined>(undefined);

    const [execDate, setExecDate] = useState<Date | null>(new Date());

    const [errorMessage, setErrorMessage] = useState<ReactNode | undefined>(undefined);

    const { mutate } = useMutation(
        (data: Result) =>
            postHelper<Result>('/results', data, auth.token, {
                execution_datetime: execDate?.toISOString(),
                benchmark_id: benchmark?.id,
                //site_id: site?.id,
                flavor_id: flavor?.id,
                tags_ids: tags.map((tag) => tag.id),
            }),
        {
            onSuccess: () => {
                props.onSuccess();
            },
            onError: (error: Error | AxiosError) => {
                setErrorMessage(getErrorMessage(error));
                props.onError();
            },
        }
    );

    function isFormValid() {
        return benchmark && site && flavor && fileContents && auth.token !== undefined;
    }

    function submit() {
        if (!isFormValid()) {
            return;
        }
        if (fileContents !== undefined) {
            mutate(JSON.parse(fileContents));
        }
    }

    function noFuture(d: Date) {
        return d < new Date();
    }

    return (
        <LoadingWrapper isLoading={auth.loading}>
            {errorMessage !== undefined && <Alert variant="danger">Error: {errorMessage}</Alert>}
            <LoginCheck message={'You must be logged in to submit new results!'} />
            <RegistrationCheck />
            <Form>
                <Row>
                    <Col lg={true}>
                        <Form.Group className="mb-3">
                            <JsonSelection
                                fileContents={fileContents}
                                setFileContents={setFileContents}
                            />{' '}
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <BenchmarkSearchSelect
                                benchmark={benchmark}
                                setBenchmark={setBenchmark}
                            />
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <SiteSearchPopover site={site} setSite={setSite} />
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <FlavorSearchSelect site={site} flavor={flavor} setFlavor={setFlavor} />
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Row>
                                <Col>Execution date:</Col>
                                <Col md="auto">
                                    <DatePicker
                                        selected={execDate}
                                        onChange={(date: Date | null) =>
                                            setExecDate(date as Date | null)
                                        }
                                        showTimeSelect
                                        timeIntervals={15}
                                        dateFormat="MMMM d, yyyy HH:mm"
                                        timeFormat="HH:mm"
                                        filterDate={noFuture}
                                        filterTime={noFuture}
                                    />
                                </Col>
                            </Row>
                            {/* dateFormat="Pp"*/}
                        </Form.Group>
                    </Col>

                    <Col lg="auto">
                        <div className="mb-1">
                            <TagSelector selected={tags} setSelected={setTags} />
                        </div>
                    </Col>
                </Row>

                <Row className="align-items-center">
                    <Col />
                    <Col md="auto">
                        <Button variant="success" disabled={!isFormValid()} onClick={submit}>
                            Submit
                        </Button>
                    </Col>
                </Row>
            </Form>
        </LoadingWrapper>
    );
}
