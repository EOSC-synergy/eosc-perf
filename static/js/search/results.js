import { search_page, init_search_page } from './result/searchPage.mjs';

/**
 * Create search page object on page load
 */
window.addEventListener('load', function () {
    init_search_page();
    search_page.onload();
});
