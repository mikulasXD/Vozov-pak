
$(document).ready(function() {
    
    $('#spz').on('blur', function() {
        var spz = $(this).val().toUpperCase();
        
        if (spz.length > 0) {
            $.ajax({
                url: '/ajax/kontrola-spz',
                data: {'spz': spz},
                method: 'GET',
                success: function(data) {
                    if (data.exists) {
                        $('#spz').addClass('is-invalid');
                        $('#spzFeedback').text('Tato SPZ již existuje v databázi!');
                        $('button[type="submit"]').prop('disabled', true);
                    } else {
                        $('#spz').removeClass('is-invalid');
                        $('#spzFeedback').text('');
                        $('button[type="submit"]').prop('disabled', false);
                    }
                },
                error: function() {
                    console.log('AJAX chyba - kontrola SPZ nefunguje');
                }
            });
        }
    });
    
   
    $('#spz').on('input', function() {
        $(this).val($(this).val().toUpperCase());
    });
});