// Enable google autocomplete with location selection
var onLoaded = function() {
    var location_input = document.getElementById('city');
    var autocomplete = new google.maps.places.Autocomplete(location_input);
};

$(document).ready(function () {
    function showLoader(pos) {
        return new Promise(function (resolve, reject) {
            if ($('#addlocation_loader').attr('hidden', false))
                resolve(pos);
        });
    }
    // Get user's location (longitude and magnitude) and post it to server
    $('#add_location_btn').on('click', function () {
        if ($('#code').val().length === 0) {
            window.alert('Please enter a valid code!');
        } else {
            const $loader = $('#addlocation_loader');
            getLocation().then(function (pos) {
                $loader.attr('hidden', false);  // Show loading sign
                return pos;
            }).then(function (pos) {
                return postLocation(pos);
            }).then(function () {
               $loader.attr('hidden', true);  // Hide loading sign
            });
        }
    });

    // Get user's location synchronously using Promise.
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
     * @param {JSON} pos  Location dictionary of user's longitude and latitude.
     */
    function postLocation(pos) {
        // Send user location to server
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

    // Prevent form submission when 'Enter' is pressed with location selection
    $('#city').keydown(function (event) {
        if (event){
            if (event.which === 13 && $('.pac-container:visible').length)
                return false;
        }
    });

    // Post meeting info to be saved in DB
    $('#new_meeting_btn').on('click', function (e) {
        if ($('#meeting_name').val().length == 0 || $('#city').val().length == 0
            || $('#place_type').val().length == 0){
            window.alert('Enter valid info for your meeting!');
        }
        else{
            $('#addmeeting_loader').attr('hidden', false);  // Show loading sign
            // Send meeting data to create meeting session in DB
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
                    $('#addmeeting_loader').attr('hidden', true);   // Hide loading sign
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
                    $('#addmeeting_loader').attr('hidden', true);  // Hide loading sign
                    console.log('Session Creation Failed');
                }
            });
        }
    });

    // Return Nearest Place given meeting code
    $('#getlocation_btn').on('click', function () {
        $('#getlocation_loader').attr('hidden', false);  // Show loading sign
        if ($('#getlocation_code').val().length === 0){
            window.alert('Please enter a valid code!');
        } else {
            // Get meeting location from server
            $.ajax({
                url: '/locations/get_location/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                    'code': $('#getlocation_code').val()
                },

                success: function (json) {
                    // Display place data
                    $('#place_name').text(json['name']);
                    $('#place_address').text(json['address']);
                    $('#place_rating').text(json['rating']);
                    $('#getlocation_loader').attr('hidden', true);  // Hide loading sign
                },
                error: function (error) {
                    $('#getlocation_loader').attr('hidden', true);  // Hide loading sign
                    console.log('Sending Location Failed!');
                }
            });
        }
    })
});