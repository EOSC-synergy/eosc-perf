import { JSONValueInputPrompt } from './jsonValueInputPrompt.mjs';

export class Filter {
    /**
     * Create a new filter entry
     * @param searchPage reference to owning object / search page
     */
    constructor(searchPage) {
        this.searchPage = searchPage;

        // add line for the filter
        this.element = document.createElement('li');
        this.element.classList.add('form-inline');

        // Remove this filter
        let deleteButton = document.createElement('button');
        deleteButton.type = 'button';
        deleteButton.classList.add('close');
        deleteButton.setAttribute('aria-label', 'Close');
        // label
        {
            let remove_filter_label = document.createElement('span');
            remove_filter_label.setAttribute('aria-hidden', 'true');
            remove_filter_label.textContent = '×';
            deleteButton.appendChild(remove_filter_label);
        }
        let filter = this;
        deleteButton.addEventListener('click', function () {
            filter.remove();
        });
        this.element.appendChild(deleteButton);

        // filter type selection
        this.filterType = document.createElement('select');
        for (let filter in Filter.TYPES) {
            // skip uploader filter option if not admin
            if (filter === 'UPLOADER' && !isAdmin()) {
                continue;
            }
            let type = document.createElement('OPTION');
            type.value = Filter.TYPES[filter];
            type.textContent = Filter.TYPES[filter];
            this.filterType.appendChild(type);
        }
        this.element.appendChild(this.filterType);

        // On change callback
        this.filterType.addEventListener('change', function () {
            filter.inputBox.placeholder = Filter.HINTS.get(filter.filterType.value);
            filter.jsonTypeHelp.dataset.content = Filter.HELPS.get(filter.filterType.value);

            // hide extra json input on other filters
            filter.suggestionsButton.disabled = true;
            filter.extraJsonInput.style.visibility = 'hidden';
            if (filter.filterType.value.localeCompare(Filter.TYPES.JSON) === 0) {
                filter.suggestionsButton.disabled = false;
                filter.extraJsonInput.style.visibility = 'visible';
            }
        });
        this.filterType.classList.add('custom-select');

        // Primary input
        let input = document.createElement('div');
        input.classList.add('input-group');
        // textbox
        this.inputBox = document.createElement('input');
        this.inputBox.type = 'text';
        this.inputBox.placeholder = 'Filter Value';
        this.inputBox.classList.add('form-control');
        input.appendChild(this.inputBox);

        // suggestions & info
        {
            let inputExtras = document.createElement('div');
            inputExtras.classList.add('input-group-append');

            // Info button
            {
                this.jsonTypeHelp = document.createElement('input');
                this.jsonTypeHelp.type = 'button';
                this.jsonTypeHelp.classList.add('btn', 'btn-outline-warning');
                this.jsonTypeHelp.value = '?';
                this.jsonTypeHelp.dataset.toggle = 'popover';
                this.jsonTypeHelp.title = 'Format Description';
                this.jsonTypeHelp.dataset.content =
                    'You find some Tips for the expected input values here.';
                this.jsonTypeHelp.dataset.placement = 'right';
                inputExtras.appendChild(this.jsonTypeHelp);
            }

            {
                this.suggestionsButton = document.createElement('button');
                this.suggestionsButton.disabled = true;
                this.suggestionsButton.classList.add(
                    'btn',
                    'btn-outline-secondary',
                    'dropdown-toggle',
                    'dropdown-toggle-split'
                );

                {
                    let suggestionsButtonScreenreaderHint = document.createElement('span');
                    suggestionsButtonScreenreaderHint.classList.add('sr-only');
                    suggestionsButtonScreenreaderHint.textContent = 'Toggle Dropdown';
                    this.suggestionsButton.appendChild(suggestionsButtonScreenreaderHint);
                }
                inputExtras.appendChild(this.suggestionsButton);
                this.jsonSuggestor = new JSONValueInputPrompt(
                    this.suggestionsButton,
                    this.inputBox
                );
            }

            input.appendChild(inputExtras);
        }
        this.element.appendChild(input);

        // Extra JSON input
        this.extraJsonInput = document.createElement('div');
        this.extraJsonInput.classList.add('input-group');
        this.extraJsonInput.style.visibility = 'hidden';
        // comparison mode dropdown
        {
            let jsonMode = document.createElement('div');
            jsonMode.classList.add('input-group-prepend');
            {
                this.jsonModeButton = document.createElement('button');
                this.jsonModeButton.classList.add(
                    'btn',
                    'btn-outline-secondary',
                    'dropdown-toggle'
                );
                this.jsonModeButton.type = 'button';
                this.jsonModeButton.dataset.toggle = 'dropdown';
                this.jsonModeButton.setAttribute('aria-haspopup', 'true');
                this.jsonModeButton.setAttribute('aria-expanded', 'false');
                this.jsonModeButton.value = JSON_MODES.GREATER_THAN;
                this.jsonModeButton.textContent = JSON_MODE_SYMBOLS.get(JSON_MODES.GREATER_THAN);
                jsonMode.appendChild(this.jsonModeButton);

                let jsonModeDropdown = document.createElement('div');
                jsonModeDropdown.classList.add('dropdown-menu');
                for (let mode in JSON_MODES) {
                    mode = JSON_MODES[mode];
                    let jsonModeOption = document.createElement('a');
                    jsonModeOption.classList.add('dropdown-item');
                    jsonModeOption.value = mode;
                    jsonModeOption.textContent = JSON_MODE_SYMBOLS.get(mode);
                    jsonModeOption.addEventListener('click', function () {
                        filter.jsonModeButton.value = mode;
                        filter.jsonModeButton.textContent = JSON_MODE_SYMBOLS.get(mode);
                    });
                    jsonModeDropdown.appendChild(jsonModeOption);
                }
                jsonMode.appendChild(jsonModeDropdown);
            }
            this.extraJsonInput.appendChild(jsonMode);
        }
        // json value input
        {
            this.jsonValue = document.createElement('input');
            this.jsonValue.classList.add('form-control');
            this.extraJsonInput.appendChild(this.jsonValue);
        }
        this.element.appendChild(this.extraJsonInput);

        document.getElementById('filters').appendChild(this.element);

        // prepare initial contents as if user just selected it
        let changeEvent = document.createEvent('HTMLEvents');
        changeEvent.initEvent('change', false, true);
        this.filterType.dispatchEvent(changeEvent);

        // Activate popover.
        $(this.element).popover({
            html: true,
        });
    }

    /**
     * Delete the filter
     */
    remove() {
        this.element.parentNode.removeChild(this.element);
        this.searchPage.remove_filter(this);
    }

    /**
     * Get the type of filter
     * @returns {string} one of Filter.TYPES
     */
    getType() {
        return this.filterType.value;
    }

    /**
     * Get the current value being compared against
     * @returns {string} value from text box
     */
    getValue() {
        return this.inputBox.value;
    }

    /**
     * Get the current comparison mode
     * @returns {string} one of JSON_MODES
     */
    getJsonMode() {
        return this.jsonModeButton.value;
    }

    /**
     * Get the json value being compared against.
     * @returns {string} value from text box
     */
    getJsonValue() {
        return this.jsonValue.value;
    }
}

Filter.TYPES = Object.freeze({
    SITE: 'Site',
    TAG: 'Tag',
    UPLOADER: 'Uploader',
    JSON: 'JSON-Key',
});

Filter.KEYS = new Map([
    [Filter.TYPES.SITE, 'site'],
    [Filter.TYPES.TAG, 'tag'],
    [Filter.TYPES.UPLOADER, 'uploader'],
    [Filter.TYPES.JSON, 'json'],
]);

Filter.HINTS = new Map([
    [Filter.TYPES.SITE, 'site identifier'],
    [Filter.TYPES.TAG, 'tag_name'],
    [Filter.TYPES.UPLOADER, 'user@example.com'],
    [Filter.TYPES.JSON, 'path.to.value'],
]);

Filter.HELPS = new Map([
    [
        Filter.TYPES.SITE,
        "This field requires the site's identifier, which is a form of identifier. Sites can be found in the <i>Site</i> column in the result table below.",
    ],
    [
        Filter.TYPES.TAG,
        'A tag is a short bit of text containing one or multiple keywords, such as <code>tensor</code> or <code>gpu_bound</code>.',
    ],
    [
        Filter.TYPES.UPLOADER,
        "The Uploader is described by the uploader's email. Different uploaders can be found in the table below in the <i>Uploader</i> column.",
    ],
    [
        Filter.TYPES.JSON,
        'The search value has to describe the exact path within the JSON, separated with a dot.<br/>\
        <b>Example:</b><br/> \
        <code>{"example":{"nested":{"json":"value"},"different":{"path":{"to":"otherValue"}}}</code><br/> \
        <b>Correct:</b><br/> \
        example.nested.json or different.path.to \
        <b>Wrong:</b><br/> \
        json or example.nested or different:path:to',
    ],
]);

export const JSON_MODES = {
    LESS_THAN: 'lesser_than',
    LESS_OR_EQUALS: 'less_or_equals',
    EQUALS: 'equals',
    GREATER_OR_EQUALS: 'greater_or_equals',
    GREATER_THAN: 'greater_than',
};

export const JSON_MODE_SYMBOLS = new Map([
    [JSON_MODES.LESS_THAN, '<'],
    [JSON_MODES.LESS_OR_EQUALS, '≤'],
    [JSON_MODES.EQUALS, '='],
    [JSON_MODES.GREATER_OR_EQUALS, '≥'],
    [JSON_MODES.GREATER_THAN, '>'],
]);
