import { search_page } from './searchPage.mjs';

export class PageNavigation {
    /**
     * Set up page navigation handler.
     */
    constructor() {
        this.current_page = 0;
        this.results_per_page = 10;
        this.page_count = 1;
        this.result_count = 0;
    }

    /**
     * Update pagination buttons.
     */
    update() {
        // clear away all page buttons
        let it = document.getElementById('prevPageButton');
        it = it.nextElementSibling;
        while (it.id !== 'nextPageButton') {
            let it_next = it.nextElementSibling;
            it.parentElement.removeChild(it);
            it = it_next;
        }
        // (re-)add them as needed
        let next_page_button = document.getElementById('nextPageButton');
        for (let i = 0; i < this.page_count; i++) {
            // link box
            let new_page_link_slot = document.createElement('li');
            new_page_link_slot.classList.add('page-item');
            // page link button
            let new_page_link = document.createElement('a');
            new_page_link.textContent = (i + 1).toString();
            new_page_link.classList.add('page-link');
            new_page_link.addEventListener('click', function () {
                search_page.get_paginator().set_page(i);
            });
            // highlight current page
            if (i === this.current_page) {
                new_page_link_slot.classList.add('active');
            }
            new_page_link_slot.appendChild(new_page_link);
            it.parentElement.insertBefore(new_page_link_slot, next_page_button);
        }

        if (this.current_page === 0) {
            document.getElementById('prevPageButton').classList.add('disabled');
        } else {
            document.getElementById('prevPageButton').classList.remove('disabled');
        }
        if (this.current_page === this.page_count - 1) {
            document.getElementById('nextPageButton').classList.add('disabled');
        } else {
            document.getElementById('nextPageButton').classList.remove('disabled');
        }
    }

    /**
     * Update the number of pages
     */
    update_page_count() {
        this.page_count = Math.max(Math.ceil(this.result_count / this.results_per_page), 1);
        if (this.current_page >= this.page_count) {
            this.current_page = this.page_count - 1;
        }
    }

    /**
     * Update the current number of results.
     * @param result_count The new number of results.
     */
    set_result_count(result_count) {
        this.result_count = result_count;
        this.update_page_count();
        this.update();
    }

    /**
     * Go to the previous page.
     */
    prev_page() {
        this.current_page = Math.max(0, this.current_page - 1);
        this.update();
        search_page.update();
    }

    /**
     * Go to the specified page.
     * @param page page number
     */
    set_page(page) {
        this.current_page = Math.max(0, Math.min(page, this.page_count - 1));
        this.update();
        search_page.update();
    }

    /**
     * Go to the previous page.
     */
    next_page() {
        this.current_page = Math.min(this.page_count - 1, this.current_page + 1);
        this.update();
        search_page.update();
    }

    /**
     * Get the index of the first result displayed on page.
     * @returns {number} The index of the first result displayed on page.
     */
    get_start_index() {
        return this.current_page * this.results_per_page;
    }

    /**
     * Get the index of one past the last result displayed on page.
     * @returns {number} The index of one past the last result displayed on page.
     */
    get_end_index() {
        return (this.current_page + 1) * this.results_per_page;
    }

    /**
     * Update the number of results displayed per page.
     */
    update_page_result_count() {
        this.results_per_page = document.getElementById('results_on_page').value;
        // Restart at page 1;
        this.current_page = 0;
        this.update_page_count();
        this.update();
        search_page.update();
    }
}
