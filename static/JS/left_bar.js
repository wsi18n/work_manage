$('.list-group-item').on('click', function () {
    if (typeof($(this).attr("href")) !== "undefined") {
        window.location.href = $(this).attr("href")
    }
    $(this).siblings().removeClass('active');
    $(this).siblings('.sub-list').slideUp(250);
    if ($(this).hasClass("active")) {
        $(this).removeClass('active');
        $(this).next('.sub-list').slideUp(250);
    }
    else {
        $(this).addClass('active');
        $(this).next('.sub-list').slideDown(250);
    }
})