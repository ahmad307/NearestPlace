// Get user's location (longitude and magnitude) and post it to server
$('#add_location_btn').on('click', function () {
    $('#loader').toggle();    // Show loading sign
    if ($('#code').val().length === 0) {
        window.alert('Enter a valid code!');
    } else {
        getLocation().then(function (data) {
            postLocation(data);
            $('#loader').toggle();  // Hide loading sign
        });
    }
});

// Get the 'Nearest Place' for the meeting with given code
$('#place_btn').on('click', function () {
    $('#loader').toggle();    // Not having an effect for some reason
    if ($('#code').val().length === 0) {
        window.alert('Enter valide code for your meeting!');
    } else {
        // Post meeting code to server & receive Nearest Place
        $.ajax({
            url:'/locations/get_location/',
            type:'POST',
            data:{'csrfmiddlewaretoken':'{{ csrf_token }}', 'code':$('#code').val()},

            success: function (json) {
                if (json['message'] == 'Incorrect Code')
                    window.alert('Please enter an existing code!');
                else
                    $('#result_place').text(json['place']);
            },
            error: function () {
                console.log('Failed to get nearest place!');
            }
        })
    }
    $('#loader').toggle();
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
            'csrfmiddlewaretoken':'{{ csrf_token }}',
            'code':$('#code').val(),
            'lng':pos.lng,
            'lat':pos.lat
        },

        success: function (json) {
            window.alert('Location Saved!');
        },
        error: function (e) {
            console.log('Sending Location Failed!');
        }
    })
}
