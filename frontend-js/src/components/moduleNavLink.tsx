import { Page } from 'pages/page';
import { NavLink } from 'react-router-dom';
import React from 'react';

/**
 * Create navbar-dropdown button for a subpage
 * @param props { reference: reference to module to link to }
 * @constructor
 *
 * Notes: cannot use <NavDropdown.Item> due to <Link>, dropdown-item class added manually
 */
export function ModuleNavLink(props: {
    reference: Page;
    className?: string;
    setCurrentTab: (tab: string) => void;
}) {
    return (
        <NavLink
            to={props.reference.path}
            onClick={() => props.setCurrentTab(props.reference.name)}
            className={props.className ? props.className : 'dropdown-item'}
        >
            {props.reference.displayName}
        </NavLink>
    );
}
