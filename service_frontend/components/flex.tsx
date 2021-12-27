import React, { ReactNode } from 'react';

/**
 * Flex container component
 * @param props
 * @constructor
 */
function Flex(props: { className?: string; children?: ReactNode }) {
    return <div className={'d-flex ' + (props.className ?? '')}>{props.children}</div>;
}

/**
 * Flex float-left component
 * @param props
 * @constructor
 */
function FloatLeft(props: { className?: string; children?: ReactNode }) {
    return (
        <div
            className={'justify-content-start ' + (props.className ?? '')}
            style={{ flex: 1, marginRight: 'auto' }}
        >
            {props.children}
        </div>
    );
}

/**
 * Flex float center component
 * @param props
 * @constructor
 */
function Center(props: { className?: string; children?: ReactNode }) {
    return (
        <div
            className={'d-flex justify-content-center ' + (props.className ?? '')}
            style={{ flex: 1 }}
        >
            {props.children}
        </div>
    );
}

/**
 * Flex float right component
 * @param props
 * @constructor
 */
function FloatRight(props: { className?: string; children?: ReactNode }) {
    return (
        <div
            className={'d-flex justify-content-end ' + (props.className ?? '')}
            style={{ flex: 1, marginLeft: 'auto' }}
        >
            {props.children}
        </div>
    );
}

export default Object.assign(Flex, {
    FloatLeft,
    Center,
    FloatRight
});
