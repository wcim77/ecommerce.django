jQuery(function() {
    // Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
        e.stopPropagation();
    });

    $('.js-check :radio').on('change', function () {
        var checkAttrName = $(this).attr('name');
        var $this = $(this);
        $('input[name=' + checkAttrName + ']').closest('.js-check').removeClass('active');
        if ($this.is(':checked')) {
            $this.closest('.js-check').addClass('active');
        }
    });

    $('.js-check :checkbox').on('change', function () {
        $(this).closest('.js-check').toggleClass('active', $(this).is(':checked'));
    });

    // Bootstrap tooltip
    $('[data-toggle="tooltip"]').tooltip();

    // Fade out message
    setTimeout(function() {
        $('#message').fadeOut('slow');
    }, 4000);
});
