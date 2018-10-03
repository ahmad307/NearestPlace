// Enable google autocomplete with location selection
var onLoaded = function() {
    var location_input = document.getElementById('city');
    var autocomplete = new google.maps.places.Autocomplete(location_input);
};

$(document).ready(function () {
    // Get user's location (longitude and magnitude) and post it to server
    $('#add_location_btn').on('click', function () {
        $('#loader').attr('hidden', false);    // Show loading sign
        if ($('#code').val().length === 0) {
            window.alert('Enter a valid code!');
        } else {
            getLocation().then(function (data) {
                postLocation(data);
                $('#loader').attr('hidden', true);  // Hide loading sign
            });
        }
    });

    // Get user's location synchronously.
    function getLocation() {
        return new Promise(function (resolve, reject) {
            var pos;
            // Get user's current location
            if (navigator.geolocation) {
              navigator.geolocation.getCurrentPosition(function(position) {
                pos = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude
                };
                if (pos) resolve(pos);
              });
            } else {
                console.log('Location access denied!');
            }
        });
    }

    /**
     * Posts user's location co-ordinates to the server.
     * @param {Dict} data   Location dict of user's longitude and latitude.
     */
    function postLocation(data) {
        var pos = data;
        $.ajax({
            url:'/locations/add_location/',
            type:'POST',
            data:{
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'code':$('#code').val(),
                'lng':pos.lng,
                'lat':pos.lat
            },

            success: function (json) {
                $('#code').val('');
                if (json['message'] === 'Incorrect Code'){
                    window.alert('This code does not exist!');
                } else {
                    window.alert('Location Saved!');
                }
            },
            error: function (e) {
                console.log('Sending Location Failed!');
            }
        })
    }

    // Prevent form submission when enter is pressed with location selection
    $('#city').keydown(function (event) {
        if (event){
            if (event.which === 13 && $('.pac-container:visible').length)
                return false;
        }
    });

    // Post session info to be saved in DB
    $('#new_meeting_btn').on('click', function (e) {
        if ($('#meeting_name').val().length == 0 || $('#city').val().length == 0 || $('#place_type').val().length == 0){
            window.alert('Enter valid info for your meeting!');
        }
        else{
            $.ajax({
                url:'/locations/create_session/',
                type:'POST',
                data:{
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
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
                        $('#code_title').attr('hidden', false);
                        $('#code_msg').attr('hidden', false);
                        $('#meeting_code').text(json['code']);
                    }
                },
                error: function () {
                    console.log('Session Creation Failed');
                }
            });
        }
    });
});