$(document).ready(function() {

    // Set the CSRF token so that we are not rejected by server
    var csrf_token = $('meta[name=csrf-token]').attr('content');
    // Configure ajaxSetupso that the CSRF token is added to the header of every request
  $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    // Attach a function to trigger when users click on the like button.
    $(".like-button").on("click", function() {
        var postId = $(this).data("post-id");

        // This is the actual call which sends data to the server. It captures the data we need in order to update the vote count: the ID of the idea which was clicked, and which count to incrememnt.
        $.ajax({
            url: '/like/' + postId,
            type: 'POST',
            success: function(response){
                console.log(response);
                console.log("Selector:", "#like-count-" + postId);
                var buttonSelector = "#like-button-" + postId;
                $("#like-count-" + postId).text(response.like_count);
                $(buttonSelector).css("background-color", "#50C99A");
                //$("#title").text(response.like_count);
            },
            error: function(error)
            {
                console.log(error);
            }
        });
    });

    // Add your new function here
    $("#follow-button").on("click",function(){
        console.log("Clicked");
        var userId = $(this).data("user-id"); 
        var followButton = "#follow-button";

        $.ajax({
            url: "/follow/" + userId,
            type: 'POST',
            success: function(data) {
                console.log(data);
                // Update UI based on the response
                if (data.status == "OK") {
                    if (data.action == 'Follow')
                    {   
                        console.log("Followed");
                        // Perform The Follow Action
                        $(followButton).text("Unfollow"); 
                        // Example: Update button text
                    }
                    else
                    {   
                        console.log("Unfollowed");
                        // Perform the Unfollow Action
                        $(followButton).text("Follow"); 
                        // Example: Update button text
                    }   
                }
            },
            error: function(error) {
                console.error("Error:", error);
            }
        });
    });
});