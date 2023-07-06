$("#employeeadd").on("click",function(){
    console.log("hello")
    $("#staticBackdrop").modal("show")
})

$(document).ready(function() {
    $("#addEmployeeForm").submit(function(e) {
        e.preventDefault();
        console.log("cdcdbu")

        $.ajax({
            url: employeeAddUrl,
            type: "POST",
            data: $(this).serialize(),
            success: function(response) {
                // Redirect to the desired page
                window.location.href = employeeRedirectURL;
            },
            error: function(message) {
                console.log("error=========",message.responseJSON.message
)
                var errorMessage = message.responseJSON.message;
                $("#errorMessage").text(errorMessage);
            }
        });
    });
});