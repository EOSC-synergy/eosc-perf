import React, { ReactNode } from 'react';

function Flex(props: { className?: string; children?: ReactNode }) {
    return <div className={'d-flex ' + (props.className ?? '')}>{props.children}</div>;
}

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
