var paidAnon;
var unpaidAnon;
var paidOwn;
var unpaidOwn;

$(document).ready(function () {
    $('.anon').tooltipster({
        theme: 'tooltipster-light',
        touchDevices: true,
        trigger: 'hover',
        content: paidAnon,
        position: 'top'
    });

    $('.own').tooltipster({
        theme: 'tooltipster-light',
        content: paidOwn,
        trigger: 'hover',
        touchDevices: true,
        position: 'top'
    });

    $('.unpaid-own').tooltipster({
        theme: 'tooltipster-light',
        content: unpaidOwn,
        trigger: 'hover',
        touchDevices: true,
        position: 'top'
    });

    $('.unpaid-others').tooltipster({
        theme: 'tooltipster-light',
        content: unpaidAnon,
        trigger: 'hover',
        touchDevices: true,
        position: 'top'
    });
});