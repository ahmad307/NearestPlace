// Enable google autocomplete with location selection
var onLoaded = function() {
    var location_input = document.getElementById('city');
    var autocomplete = new google.maps.places.Autocomplete(location_input);
};

// Prevent form submission when enter is pressed with location selection
$('#city').keydown(function (event) {
    if (event){
        if (event.which === 13 && $('.pac-container:visible').length)
            return false;
    }
});

// Post session info to saved in DB
$('#new_meeting_btn').on('click', function (e) {
    if ($('#meeting_name').val().length == 0 || $('#city').val().length == 0 || $('#place_type').val().length == 0){
        window.alert('Enter valid info for your meeting!');
    }
    else{
        $.ajax({
            url:'/locations/create_session/',
            type:'POST',
            data:{
                'csrfmiddlewaretoken':'{{ csrf_token }}',
                'meeting_name':$('#meeting_name').val(),
                'city':$('#city').val(),
                'place_type':$('#place_type').val()
            },

            success: function (json) {
                // Prompt the user if the session wasn't created in the DB
                if (json['message'] === 'ValidationError'){
                    window.alert('Please try again!');
                } else {
                    // Remove entered data
                    $('#city').val('');
                    $('#place_type').val('');
                    $('#meeting_name').val('');

                    // Display result
                    $('#message1').show();
                    $('#message2').show();
                    $('#meeting_code').text(json['code']);
                }
            },
            error: function () {
                console.log('Session Creation Failed');
            }
        });
    }
});
