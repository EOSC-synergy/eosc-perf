function _fill_report_item(item, data) {
    item.id = data.uuid;
    item.classList.add("list-group-item", "list-group-item-action", "flex-column", "align-items-start");

    let headingDiv = document.createElement("div");
    headingDiv.classList.add("d-flex","w-100", "justify-content-between");
    let heading = document.createElement("h5");
    heading.classList.add("mb-1");
    heading.textContent = data.type;
    headingDiv.appendChild(heading);
    let headingExtra = document.createElement("small");
    headingExtra.textContent = data.uuid;
    headingDiv.appendChild(headingExtra);
    item.appendChild(headingDiv);

    let messageParagraph = document.createElement("p");
    messageParagraph.classList.add("mb-1");
    messageParagraph.textContent = data.message;
    item.appendChild(messageParagraph);

    let footerDiv = document.createElement("div");
    footerDiv.classList.add("d-flex", "w-100", "justify-content-between");

    let submitterSmall = document.createElement("small");
    submitterSmall.textContent = data.submitter;
    let statusSmall = document.createElement("small");
    let statusSpan = document.createElement("span");
    statusSpan.classList.add("badge");
    if (data.verdict === "accepted") {
        statusSpan.classList.add("bg-success");
    }
    else if (data.verdict === "rejected") {
        statusSpan.classList.add("bg-danger");
    }
    else {
        statusSpan.classList.add("bg-secondary");
    }
    statusSpan.textContent = data.verdict;
    statusSmall.appendChild(statusSpan);

    footerDiv.appendChild(submitterSmall);
    footerDiv.appendChild(statusSmall);

    item.appendChild(footerDiv);

    if (data.type === "result") {
        item.onclick = function() {
            window.location.href = '/view_report?uuid=' + encodeURI(data.uuid);
        }
    }
    else if (data.type === "site") {
        item.onclick = function() {
            window.location.href = '/site_review?uuid=' + encodeURI(data.uuid);
        }
    }
    else if (data.type === "benchmark") {
        item.onclick = function() {
            window.location.href = '/benchmark_review?uuid=' + encodeURI(data.uuid);
        }
    }
}

window.addEventListener("load", function () {
    $.ajax('/fetch_reports').done(function (data) {
        let list = document.getElementById("reportListGroup");
        if (data.reports.length === 0) {
            let warning = document.createElement("div");
            warning.textContent = "No reports found!";
            list.appendChild(warning);
        }
        for (const report of data.reports) {
            let report_entry = document.createElement("div");
            _fill_report_item(report_entry, report);
            list.appendChild(report_entry);
        }
    });
});
