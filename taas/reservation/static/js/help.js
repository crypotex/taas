var paidAnon;
var unpaidAnon;
var paidOwn;
var unpaidOwn;

$(document).ready(function () {
    $('#anon').tooltipster({
        theme: 'tooltipster-light',
        offsetX: -189,
        offsetY: 12,
        content: paidAnon
    });

    $('#own').tooltipster({
        theme: 'tooltipster-light',
        offsetX: -189,
        offsetY: 12,
        content: paidOwn
    });

    $('#unpaid-own').tooltipster({
        theme: 'tooltipster-light',
        offsetX: -189,
        offsetY: 12,
        content: unpaidOwn
    });

    $('#unpaid-others').tooltipster({
        theme: 'tooltipster-light',
        offsetX: -189,
        offsetY: 12,
        content: unpaidAnon
    });
});