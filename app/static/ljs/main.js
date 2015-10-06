$(document).ready(function () {

    // You can delete this function, it's only used for demo purposes to get a future date
    function futureDate() {
        var futureDate = new Date();
        futureDate.setDate(futureDate.getDate() + 6);

        dd = futureDate.getDate();
        mm = futureDate.getMonth() + 1;
        y = futureDate.getFullYear();

        futureFormattedDate = mm + '/'+ dd + '/'+ y;

        return futureFormattedDate;
    }


    // Change the 'date' variable value to your desierd future date
    $('#countdown').downCount({
        date: "2015-05-07"+'12:00:00', // CHANGE THE DATE
        offset: -4 // CHANGE UTC OFFSET
    });

    // This is a subscribe form action
    $('#subscribe button').on('click', function (e) {
        var error = 0;
        e.preventDefault();

        $('#subscribe input').each(function () {
            if($(this).val().length > 0) {
                $(this).parents('div').removeClass('error');
            } else {
                $(this).parents('div').addClass('error');
                error = 1;
            }
        });

        if(error == 1) {
            $('.error_alert').fadeIn(function() {
                $(this).delay(1000).fadeOut();
            });
        } else {
            var action = $('#subscribe').attr('action');

            $.ajax({
                url: 'assets/email/'+action,
                type: 'POST',
                data: {
                    name:  $('#subscribe input[name="name"]').val(),
                    email: $('#subscribe input[name="email"]').val()
                },
                success: function(data){
                    $('#subscribe').html("<span>Got it, you've been added to our email list.</span>");
                },
                error: function() {
                    $('.error_alert').fadeIn(function() {
                        $(this).delay(1000).fadeOut();
                    });
                }
            });
        }
    });

});