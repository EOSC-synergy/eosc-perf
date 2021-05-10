/**
 * Helping wrapper to manage dropdown buttons for any needed json path input fields (filter suggestions, chart axis, ?)
 *
 * TODO: search field?
 */
import { search_page } from './searchPage.mjs';

export class JSONValueInputPrompt {
    /**
     * Create new JSON keypath selection prompt
     * @param dropdownButton the button that opens the prompt
     * @param inputBox the textbox to put selected values into
     */
    constructor(dropdownButton, inputBox) {
        this.button = dropdownButton;
        this.button.dataset.toggle = 'dropdown';

        this.button.setAttribute('aria-haspopup', 'true');
        this.button.setAttribute('aria-expanded', 'false');

        this.inputBox = inputBox;

        this.dropdown = document.createElement('div');
        this.dropdown.classList.add('dropdown-menu', 'dropdown-menu-right', 'scrollable-dropdown');
        this.button.parentNode.insertBefore(this.dropdown, this.button);

        let jsonValueInputPrompt = this;
        // TODO: find better visual design than bootstrap list groups
        $(dropdownButton.parentElement).on('shown.bs.dropdown', function () {
            const keys = search_page.get_notable_keys();
            clear_element_children(jsonValueInputPrompt.dropdown);
            let list = document.createElement('ul');
            list.classList.add('list-group');
            for (const key of keys) {
                let item = document.createElement('li');
                item.textContent = key;
                item.classList.add('list-group-item');
                item.onclick = function () {
                    jsonValueInputPrompt.set_value(key);
                };
                list.appendChild(item);
            }
            if (keys.length === 0) {
                let item = document.createElement('li');
                item.textContent = 'No notable keys found!';
                item.classList.add('list-group-item', 'text-muted');
                item.disabled = true;
                list.appendChild(item);
            }
            jsonValueInputPrompt.dropdown.appendChild(list);
        });

        $(this.button).dropdown();
    }

    /**
     * Callback to set the value to the input box
     * @param value
     */
    set_value(value) {
        this.inputBox.value = value;

        // call change callback if it exists
        if (this.inputBox.onchange !== undefined) {
            this.inputBox.onchange();
        }
    }
}
