$("#employeeadd").on("click",function(){
    console.log("hello")
    $("#staticBackdrop").modal("show")
})

$(".close_btn").on("click",function(){
    $("#staticBackdrop").modal("hide")
})

$(document).ready(function() {
    $("#addEmployeeForm").submit(function(e) {

        e.preventDefault();
        $.ajax({
            url: employeeAddURL,
            type: "POST",
            data: $(this).serialize(),
            success: function(response) {
                window.location.href = employeeRedirectURL;
            },
            error: function(message) {
                var errorMessage = message.responseJSON.message;
                $("#errorMessage").text(errorMessage);
            }
        });
    });
});
