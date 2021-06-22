import React, { ReactNode, useState } from 'react';
import { useAccordionToggle } from 'react-bootstrap';
import { DropdownArrow } from './dropdownArrow';

/**
 * Custom accordion toggle to not provide special highlighting and be similar to old look
 * @param props { children: JSX child elements, eventKey: accordion event key}
 * @constructor
 */
export function CardAccordionToggle(props: { children: ReactNode; eventKey: string }) {
    const [toggled, setToggled] = useState(true);
    const decoratedOnClick = useAccordionToggle(props.eventKey, () => {
        setToggled(!toggled);
    });

    return (
        <div role="button" onClick={decoratedOnClick}>
            {props.children}
            <DropdownArrow toggled={toggled} />
        </div>
    );
}
