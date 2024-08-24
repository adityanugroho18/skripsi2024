// CURRENCY FORMAT
function formatRupiah(number, precision = 0) {
    const numberParts = Number(Math.abs(number)).toFixed(precision).split('.');
    const integerPart = numberParts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    const decimalPart = numberParts[1] || '0';

    if (precision == 0) {
        return `${number < 0 ? '-' : ''}${integerPart}`;
    }
    else {
        return `${number < 0 ? '-' : ''}${integerPart},${decimalPart}`;
    }
}

function clearFormatRupiah(number) {
    var result = number.replaceAll('.', '')
    result = result.replaceAll(',', '.')

    return parseFloat(result)
}

$(document).on('input', '.currency-input', function(event) {
    // Allow only numbers, period, and comma
    const charCode = (event.which) ? event.which : event.keyCode;
    if (charCode !== 44 && charCode !== 46 && (charCode < 48 || charCode > 57)) {
        return false;
    }

    let value = $(this).val();

    // Remove any character that is not a digit, period, or comma
    value = value.replace(/[^0-9.,]/g, '');

    // Split into integer and decimal parts
    let parts = value.split(',');
    let integerPart = parts[0];
    let decimalPart = parts.length > 1 ? parts[1] : '';

    // Remove periods from the integer part
    integerPart = integerPart.replace(/\./g, '');

    // Add periods as thousand separators
    integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

    // Limit decimal part to two digits
    if (decimalPart.length > 2) {
        decimalPart = decimalPart.substring(0, 2);
    }

    if (value.includes(',')) {
        // Combine the integer and decimal parts
        value = integerPart + ',' + decimalPart;

    }
    else {
        //value = integerPart;
        value = integerPart
    }

    $(this).val(value);
});

function currencyInput(input) {
    // Allow only numbers, period, and comma
    const charCode = (event.which) ? event.which : event.keyCode;
    if (charCode !== 44 && charCode !== 46 && (charCode < 48 || charCode > 57)) {
        return false;
    }

    let value = input.value;

    // Remove any character that is not a digit, period, or comma
    value = value.replace(/[^0-9.,]/g, '');

    // Split into integer and decimal parts
    let parts = value.split(',');
    let integerPart = parts[0];
    let decimalPart = parts.length > 1 ? parts[1] : '';

    // Remove periods from the integer part
    integerPart = integerPart.replace(/\./g, '');

    // Add periods as thousand separators
    integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

    // Limit decimal part to two digits
    if (decimalPart.length > 2) {
        decimalPart = decimalPart.substring(0, 2);
    }

    if (value.includes(',')) {
        // Combine the integer and decimal parts
        value = integerPart + ',' + decimalPart;

    }
    else {
        //value = integerPart;
        value = integerPart
    }

    input.value = value
}
// END CURRENCY FORMAT

// Allow only numeric characters on keypress
$('.numeric-input').on('keypress', function(e) {
    var charCode = (e.which) ? e.which : e.keyCode;
    if (charCode < 48 || charCode > 57) {
        e.preventDefault();
    }
});

// Prevent pasting non-numeric content
$('.numeric-input').on('paste', function(e) {
    var clipboardData = e.originalEvent.clipboardData || window.clipboardData;
    var pastedData = clipboardData.getData('text');
    if (!/^\d+$/.test(pastedData)) {
        e.preventDefault();
    }
});

// Optionally handle input event to filter out any non-numeric characters
$('.numeric-input').on('input', function() {
    this.value = this.value.replace(/[^0-9]/g, '');
});

function numericInput(selector) {
    $(document).on('keypress', selector, function(event) {
        // Allow only numbers, period, and comma
        const charCode = (event.which) ? event.which : event.keyCode;
        if (charCode !== 44 && charCode !== 46 && (charCode < 48 || charCode > 57)) {
            event.preventDefault();
        }
    });

    $(document).on('input', selector, function() {
        this.value = this.value.replace(/[^0-9]/g, '');
    });

    $(document).on('paste', selector, function(e) {
        var clipboardData = e.originalEvent.clipboardData || window.clipboardData;
        var pastedData = clipboardData.getData('text');

        // Prevent the default paste behavior
        e.preventDefault();
    });
}