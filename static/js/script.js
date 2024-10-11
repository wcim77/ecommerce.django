// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
        e.stopPropagation();
        $(this).css('background-color', '#f0f0f0'); // Change background color to make it more noticeable
        $(this).find('a').css('color', '#ff0000'); // Change link color to red
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name="' + check_attr_name + '"]').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
            // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        var $closestCheck = $(this).closest('.js-check');
        if ($(this).is(':checked')) {
            $closestCheck.addClass('active');
            // Optionally, you can add some visual feedback or additional actions here
        } else {
            $closestCheck.removeClass('active');
            // Optionally, you can add some visual feedback or additional actions here
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if




    
}); 
// jquery end

$(document).ready(function() {
    // Existing jQuery code...

    setTimeout(function() {
        $('#message').fadeOut('slow');
    }, 4000);
});