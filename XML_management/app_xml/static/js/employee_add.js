$(document).ready(function() {
    $("#addEmployeeForm").submit(function(e) {
        e.preventDefault();
        console.log("cdcdbu")
        
        $.ajax({
            url: "/add-employee/",
            type: "POST",
            data: $(this).serialize(),
            success: function(response) {
                // Redirect to the desired page
                window.location.href = response.redirect_url;
            },
            error: function(xhr) {
                console.log("error=========",xhr)
                var errorMessage = xhr.responseJSON.error_message;
                $("#errorMessage").text(errorMessage);
            }
        });
    });
});