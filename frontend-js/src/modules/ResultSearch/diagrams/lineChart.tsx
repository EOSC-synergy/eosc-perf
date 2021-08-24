import { Benchmark, Result } from '../../../api';
import { useState } from 'react';
import { Form } from 'react-bootstrap';

enum Mode {
    Simple,
    Linear,
    Logarithmic,
}

function LineChart(props: { results: Result[]; benchmark?: Benchmark }) {
    const [mode, setMode] = useState(Mode.Simple);

    return (
        <>
            <Form.Control
                as="select"
                onChange={(e) => {
                    setMode(parseInt(e.target.value));
                }}
            >
                <option value={Mode.Simple}>Simple</option>
                <option value={Mode.Linear}>Linear</option>
                <option value={Mode.Logarithmic}>Logarithmic</option>
            </Form.Control>
            {/* TODO */}
            <div className="form-check">
                <input
                    className="form-check-input"
                    type="checkbox"
                    value=""
                    id="speedupDiagramGroupedMode"
                    onChange={() => {} /*search_page.update_diagram_configuration()}*/}
                />
                <label className="form-check-label" htmlFor="speedupDiagramGroupedMode">
                    Group values by site (only in linear & logarithmic mode)
                </label>
            </div>
            <div id="diagramSection" className="d-flex flex-column lead" />
        </>
    );
}

const LineChartMeta = {
    element: LineChart,
    name: 'Line Chart',
    id: '0',
};

export default LineChartMeta;
