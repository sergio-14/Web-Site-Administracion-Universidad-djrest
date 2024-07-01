(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    

    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });


})(jQuery);


/*
 Sirve para probar si se esta cargando el js.
(function ($) {
    "use strict";

    alert("main.js esta siendo cargado!");

})(jQuery);
*/